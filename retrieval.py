from typing import List, Dict
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

class Retriever:
    """文档检索类"""

    def __init__(self,
                 embedding_model_name: str = "BAAI/bge-large-zh",
                 rerank_model_name: str = "BAAI/bge-reranker-large",
                 index_type: str = "faiss-flat",
                 top_k: int = 5):
        """
        Args:
            embedding_model_name: 向量化模型名称
            rerank_model_name: 重排序模型名称
            index_type: 向量索引类型
            top_k: 召回数量
        """
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.rerank_tokenizer = AutoTokenizer.from_pretrained(rerank_model_name)
        self.rerank_model = AutoModelForSequenceClassification.from_pretrained(rerank_model_name)
        self.top_k = top_k

        # 初始化FAISS索引
        self.dimension = self.embedding_model.get_sentence_embedding_dimension()
        if index_type == "faiss-flat":
            self.index = faiss.IndexFlatL2(self.dimension)
        elif index_type == "faiss-ivf":
            nlist = 100  # 聚类中心数量
            quantizer = faiss.IndexFlatL2(self.dimension)
            self.index = faiss.IndexIVFFlat(quantizer, self.dimension, nlist)
            self.index.train(np.random.random((1000, self.dimension)).astype('float32'))

    def add_documents(self, documents: List[str]):
        """添加文档到索引"""
        embeddings = self.embedding_model.encode(documents)
        self.index.add(np.array(embeddings).astype('float32'))
        self.documents = documents

    def retrieve(self, query: str) -> List[Dict]:
        """检索相关文档

        Args:
            query: 用户查询

        Returns:
            检索结果列表，每个元素包含文档内容和相似度分数
        """
        # 1. 向量检索
        query_embedding = self.embedding_model.encode([query])
        scores, indices = self.index.search(query_embedding, self.top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:  # 有效索引
                results.append({
                    "content": self.documents[idx],
                    "score": float(score)
                })

        # 2. 交叉编码重排序
        if len(results) > 1:
            rerank_scores = []
            for result in results:
                inputs = self.rerank_tokenizer(
                    query,
                    result["content"],
                    truncation=True,
                    max_length=512,
                    return_tensors="pt"
                )
                with torch.no_grad():
                    scores = self.rerank_model(**inputs).logits
                rerank_scores.append(float(scores[0][1]))  # 取positive score

            # 重新排序
            sorted_results = sorted(zip(results, rerank_scores),
                                    key=lambda x: x[1],
                                    reverse=True)
            results = [item[0] for item in sorted_results]

        return results