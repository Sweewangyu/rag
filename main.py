from typing import List, Dict
import torch
from prompt import PromptTemplate
from chunk import TextChunker
from retrieval import Retriever
from openai import OpenAI
API_KEY = "sk-b31b21a0de2240118273137745f5d396"  # 在这里填入您的API密钥
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "qwen2.5-72b-instruct"
def call_llm(system_prompt, user_text):
    """
    调用大语言模型API。
    """
    try:
        client = OpenAI(
            api_key=API_KEY,
            base_url=BASE_URL,
        )
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_text}
            ],
            temperature=0.2, # 降低随机性，使输出更稳定和可预测
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"  ❌ 调用API时发生错误: {e}")
        return None
class RAGSystem:
    """RAG系统主类"""

    def __init__(self,
                 chunk_size: int = 512,
                 retrieval_top_k: int = 5,
                 system_prompt: str = "<UNK>",
                 user_text:str = "",):
        """
        Args:
            llm_model_name: 大语言模型名称
            chunk_size: 文本分块大小
            retrieval_top_k: 检索返回数量
        """
        # 初始化组件
        self.chunker = TextChunker(chunk_size=chunk_size)
        self.retriever = Retriever(top_k=retrieval_top_k)
        self.prompt_template = PromptTemplate()

        # 初始化大语言模型
        self.llm = call_llm(system_prompt,user_text)

    def add_documents(self, documents: List[str]):
        """添加文档到知识库

        Args:
            documents: 文档列表
        """
        # 1. 文本分块
        chunks = []
        for doc in documents:
            chunks.extend(self.chunker.split_by_semantic(doc))

        # 2. 添加到检索系统
        self.retriever.add_documents(chunks)

    def answer(self, question: str) -> str:
        """回答问题

        Args:
            question: 用户问题

        Returns:
            答案
        """
        # 1. 检索相关文档
        retrieved_docs = self.retriever.retrieve(question)

        # 2. 构建提示词
        context = "\n\n".join([doc["content"] for doc in retrieved_docs])
        prompt = self.prompt_template.get_qa_prompt(context, question)
        system_prompt = self.prompt_template.get_system_prompt()

        # 3. 生成答案
        inputs =
        return answer.split("回答:")[-1].strip()


# 使用示例
if __name__ == "__main__":
    # 初始化RAG系统
    rag = RAGSystem()


    # 提问并获取答案
    question = "什么是RAG技术？"
    answer = rag.answer(question)
    print(f"问题：{question}")
    print(f"答案：{answer}")