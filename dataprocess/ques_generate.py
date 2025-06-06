import os
import pathlib
from openai import OpenAI

# --- 1. 请在此处配置您的API密钥和模型信息 ---
# 警告：直接在代码中写入API密钥存在安全风险。建议使用环境变量等更安全的方式。
API_KEY = "sk-b31b21a0de2240118273137745f5d396"  # 在这里填入您的API密钥
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "qwen2.5-72b-instruct"

# --- 2. 请修改以下两个文件夹路径 ---

# 输入路径：存放上一步骤中转换好的Markdown文件的文件夹
# 这应该是上一个脚本中的 'output_folder_path'
markdown_folder_path = "../A_document_markdown"

# 输出路径：用于存放生成的Q&A结果文件
# 脚本会自动创建此文件夹
qna_output_folder_path = "../A_document_QnA"


# --- Prompt设计 ---
# 这是指导LLM生成高质量Q&A的关键指令
SYSTEM_PROMPT = """
你是一位专业的数据分析师和文档总结专家。你的任务是根据我提供的文本内容，生成3个具有深度和洞察力的问题，并提供答案和答案在原文中的依据。

请严格遵守以下要求：
1.  **生成3个问题**：问题应该涵盖文本中的核心概念、关键数据、重要结论或潜在的应用。避免过于简单或表面化的问题,一个问题中不应包含多个问题
2.  **提供精确答案**：每个问题的答案都必须完全基于我提供的文本内容，不允许从外部知识库获取信息。
3.  **标注答案来源**：在每个答案后面，必须附上一个名为**来源：**的部分，并精确引用支撑该答案的原文句子。
4.  **使用简体中文**：所有问题、答案和标签都必须使用简体中文。
5.  **输出格式**：请严格按照下面的Markdown格式输出，以便于解析：

**问题1：** [这里写第一个问题]
**答案：** [这里写第一个问题的答案]
**来源：** "[这里引用原文中支撑答案的一句或多句话]"

**问题2：** [这里写第二个问题]
**答案：** [这里写第二个问题的答案]
**来源：** [这里引用原文中支撑答案的一句或多句话]

**问题3：** [这里写第三个问题]
**答案：** [这里写第三个问题的答案]
**来源：** [这里引用原文中支撑答案的一句或多句话]

现在，请准备接收原文并开始分析。
"""

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

def process_markdown_files(input_dir, output_dir):
    """
    遍历Markdown文件，为每个文件生成Q&A并保存。
    """
    input_path = pathlib.Path(input_dir)
    output_path = pathlib.Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"正在读取Markdown文件来源: {input_path}")
    print(f"Q&A结果将保存至: {output_path}")
    print("-" * 30)

    markdown_files = list(input_path.glob("*.md"))
    if not markdown_files:
        print("未在输入文件夹中找到任何Markdown文件。请检查路径。")
        return

    for md_file in markdown_files:
        print(f"正在处理文件: {md_file.name} ...")

        # 读取Markdown文件的内容
        content = md_file.read_text(encoding="utf-8")

        # 调用LLM生成Q&A
        qna_result = call_llm(SYSTEM_PROMPT, content)

        if qna_result:
            # 构建输出文件名
            output_filename = md_file.stem + "_QnA.txt"
            output_file_path = output_path / output_filename

            # 保存结果
            try:
                output_file_path.write_text(qna_result, encoding="utf-8")
                print(f"  ✅ 成功生成Q&A -> {output_file_path}")
            except Exception as e:
                print(f"  ❌ 保存Q&A结果时出错: {e}")

    print("-" * 30)
    print("所有文件处理完毕！")


# --- 运行主程序 ---
if __name__ == "__main__":
    if not os.path.exists(markdown_folder_path):
        print(f"错误：Markdown输入文件夹不存在，请检查路径: {markdown_folder_path}")
    else:
        process_markdown_files(markdown_folder_path, qna_output_folder_path)