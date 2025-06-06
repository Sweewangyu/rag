from prompt import PromptTemplate
from chunk import TextChunker
from Retrieval.retrieval import Retriever
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

