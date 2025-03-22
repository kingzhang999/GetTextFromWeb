import re

def process_file(input_file, output_file):
    # 定义两个正则表达式
    vol_pattern = re.compile(r'第.*卷\s+.*')
    article_pattern = re.compile(r'.*篇\s+.*')

    # 用于存储已经遇到的词汇
    seen_vols = set()
    seen_articles = set()

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(output_file, 'w', encoding='utf-8') as file:
        for line in lines:
            vol_match = vol_pattern.search(line)
            article_match = article_pattern.search(line)

            if vol_match:
                vol_text = vol_match.group()
                if vol_text not in seen_vols:
                    seen_vols.add(vol_text)
                    file.write(line)
            elif article_match:
                article_text = article_match.group()
                if article_text not in seen_articles:
                    seen_articles.add(article_text)
                    file.write(line)
            else:
                file.write(line)
import os

def get_all_txt_files(folder_path: str) -> list[str]:
    """
    获取指定文件夹下所有txt文件的绝对路径。
    :param folder_path: 文件夹的绝对路径。
    :return: 包含所有txt文件绝对路径的列表
    """
    txt_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                absolute_path = os.path.abspath(os.path.join(root, file))
                txt_files.append(absolute_path)
    return txt_files

def remove_repetition_title(folder_path: str):
    txt_files = get_all_txt_files(folder_path)
    for file_path in txt_files:
        process_file(file_path, file_path)
        print(f"处理文件 {file_path} 完成")
if __name__ == '__main__':
    folder_path = '小说/完整小说'  # 替换为实际的文件夹路径
    remove_repetition_title(folder_path)
