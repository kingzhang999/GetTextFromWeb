import os


# 新增的函数：查找并拼接文件名格式为 '1 xxx.txt' 的所有 txt 文件
def find_and_merge_txt_files(directory, output_file):
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    # 根据文件名中的数字进行排序
    sorted_files = sorted(txt_files, key=lambda x: int(x.split('.')[0].split()[0]))
    # 合并文件
    merge_txt_files(directory, sorted_files, output_file)

def merge_txt_files(directory, sorted_files, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file in sorted_files:
            file_path = os.path.join(directory, file)
            with open(file_path, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read() + '\n')