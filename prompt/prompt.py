from typing import List, Dict


class PromptTemplate:
    """提示词模板管理类"""

    @staticmethod
    def get_qa_prompt(context: str, question: str) -> str:
        """生成基础问答的提示词模板

        Args:
            context: 召回的上下文信息
            question: 用户问题
        """
        return f"""请基于以下信息回答用户问题。如果无法从给定信息中得到答案，请说"我无法从提供的信息中找到相关答案"。

相关信息:
{context}

用户问题: {question}

回答:"""

    @staticmethod
    def get_rerank_prompt(question: str, doc: str) -> str:
        """生成重排序的提示词模板

        Args:
            question: 用户问题
            doc: 待评估文档
        """
        return f"""请评估以下文档与问题的相关性，返回0-10的分数。10分表示完全相关，0分表示完全不相关。

问题: {question}
文档: {doc}

相关性分数(0-10):"""

    @staticmethod
    def get_system_prompt() -> str:
        """系统角色设定的提示词"""
        return """你是一个专业、严谨的AI助手。在回答问题时:
1. 如果确定答案，请直接给出
2. 如果不确定，要明确说明
3. 回答要简洁、准确
4. 必要时可以列出信息来源"""