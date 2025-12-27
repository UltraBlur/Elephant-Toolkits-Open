import os
import re

# ================= 配置区域 =================
# 在这里修改你的输入文件路径
INPUT_SRT_PATH = r'/Users/gaohuyuchen/Downloads/AoKeLiDui_Sub.srt' 

# 输出目录，默认在输入文件的同级目录下创建一个 "split_srt" 文件夹
OUTPUT_DIR = os.path.join(os.path.dirname(INPUT_SRT_PATH), "split_srt")
# ===========================================

def split_srt(input_path, output_folder):
    if not os.path.exists(input_path):
        print(f"错误：找不到文件 {input_path}")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    # 使用两个换行符分割每一个字幕块
    blocks = re.split(r'\n\s*\n', content)
    
    zh_blocks = []
    en_blocks = []

    for block in blocks:
        lines = block.split('\n')
        if len(lines) < 3:
            continue
            
        index = lines[0]        # 序号
        timestamp = lines[1]    # 时间轴
        text_lines = lines[2:]  # 字幕文本内容

        # 根据你的需求：第一行中文，第二行英文
        # 如果一个块内有多行，这里默认取第一行为中文，后续所有行为英文
        zh_text = text_lines[0]
        en_text = " ".join(text_lines[1:]) if len(text_lines) > 1 else ""

        # 构建新的字幕块
        zh_blocks.append(f"{index}\n{timestamp}\n{zh_text}\n")
        en_blocks.append(f"{index}\n{timestamp}\n{en_text}\n")

    # 生成文件名
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    zh_output = os.path.join(output_folder, f"{base_name}_ZH.srt")
    en_output = os.path.join(output_folder, f"{base_name}_EN.srt")

    # 保存文件
    with open(zh_output, 'w', encoding='utf-8') as f:
        f.write("\n".join(zh_blocks))
    
    with open(en_output, 'w', encoding='utf-8') as f:
        f.write("\n".join(en_blocks))

    print(f"处理完成！")
    print(f"中文保存至: {zh_output}")
    print(f"英文保存至: {en_output}")

if __name__ == "__main__":
    split_srt(INPUT_SRT_PATH, OUTPUT_DIR)