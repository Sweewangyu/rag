import pymupdf4llm
import pathlib
import os

# --- 请修改以下两个路径 ---

# 1. 设置包含所有PDF文件的文件夹路径
#    请确保路径字符串前有一个 'r'，以防止转义字符问题。
input_folder_path = "../A_document"

# 2. 设置用于存放转换后的Markdown文件的文件夹路径
#    建议使用一个新文件夹，脚本会自动创建它（如果不存在）。
output_folder_path = "../A_document_markdown"


# --- 修改结束 ---


def batch_convert_pdfs_to_markdown(input_dir, output_dir):
    """
    批量将指定文件夹中的所有PDF文件转换为Markdown格式。

    参数:
    input_dir (str): 包含PDF文件的输入文件夹路径。
    output_dir (str): 用于保存输出Markdown文件的文件夹路径。
    """
    # 将字符串路径转换为pathlib对象，以便更好地处理路径
    input_path = pathlib.Path(input_dir)
    output_path = pathlib.Path(output_dir)

    # 如果输出文件夹不存在，则创建它
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"正在从以下文件夹中查找PDF文件: {input_path}")
    print(f"转换后的Markdown文件将保存在: {output_path}")
    print("-" * 30)

    # 使用 .glob('*.pdf') 查找所有以 .pdf 结尾的文件
    pdf_files = list(input_path.glob("*.pdf"))

    if not pdf_files:
        print("未在输入文件夹中找到任何PDF文件。请检查路径是否正确。")
        return

    # 遍历找到的每个PDF文件
    for pdf_file in pdf_files:
        print(f"正在处理: {pdf_file.name} ...")

        try:
            # 执行转换
            md_text = pymupdf4llm.to_markdown(str(pdf_file))

            # 构建输出文件的完整路径
            # pdf_file.stem 会获取不带扩展名的文件名 (例如 "AF01")
            output_filename = pdf_file.stem + ".md"
            output_file_path = output_path / output_filename

            # 将转换后的文本以UTF-8编码写入文件
            output_file_path.write_bytes(md_text.encode("utf-8"))

            print(f"  ✅ 成功转换 -> {output_file_path}")

        except Exception as e:
            # 如果转换过程中出现错误，打印错误信息
            print(f"  ❌ 处理文件 {pdf_file.name} 时发生错误: {e}")

    print("-" * 30)
    print("所有PDF文件处理完毕！")


# --- 运行主程序 ---
if __name__ == "__main__":
    # 检查输入路径是否存在
    if not os.path.exists(input_folder_path):
        print(f"错误：输入文件夹路径不存在，请检查路径: {input_folder_path}")
    else:
        batch_convert_pdfs_to_markdown(input_folder_path, output_folder_path)