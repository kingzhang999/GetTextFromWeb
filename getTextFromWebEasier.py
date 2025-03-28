import os

import requests
from bs4 import BeautifulSoup
import merge_novel_txt_files as merge_txt
from removeRepetitionTitle import remove_repetition_title

novel_title = "义妹生活第十二卷"#"樱花庄的宠物女孩短篇集"
juan_number = "第十二卷"#"短篇"
global_text_title = "第10.5卷 长谷栞奈突如其来的教育旅行"
root_page_test_url = 'https://www.wenkuchina.com/lightnovel/181/catalog' #'https://www.wenkuchina.com/lightnovel/3180/catalog'
first_zhangjie_number = 0#156997
page_number = 2
last_zhangjie_number = 157001
novel_text_piece = 1
is_first_get_novel_websites_root_page = True
is_first_page = True
is_last_page = False
has_text_title = True
is_retying = False
is_first_page_connected_success = True

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
	"referer": "https://www.wenkuchina.com/lightnovel/2081/catalog",
}

# 定义需要删除的特殊字符和特定文本
special_char = ' '
failed_urls = {}
max_attempts = 3
#让一章的总标题在一章内只会在这一章的开头出现一次。
specific_text = ['上一章点赞目录+书签下一页','上一章点赞目录+书签下一章','上一页点赞目录+书签下一章',
                '上一页点赞目录+书签下一页','轻之文库轻小说-懂阅读更懂创作的轻小说平台-发现和创造有趣的故事-日本动漫轻小说在线阅读',
                '当前位置:轻之文库轻小说-懂阅读更懂创作的轻小说平台-',juan_number]

def write_result_to_file(result, text_path):
    if not os.path.exists(f"小说\\{novel_title}"):
        os.makedirs(f"小说\\{novel_title}")
    with open(text_path, 'a', encoding='utf-8') as f:
        f.write(result)
        if is_first_page:
            print(f"{novel_text_piece} {global_text_title} 第{first_zhangjie_number} 章 第1 页 已保存")
        else:
            print(f"{novel_text_piece} {global_text_title} 第{first_zhangjie_number} 章 第{page_number} 页 已保存")

def is_special_text_in_line(line, specific_texts):
    for specific_text1 in specific_texts:
        if specific_text1 in line:
            if '下一章' in line:
                global is_last_page
                is_last_page = True
                return True
            return True
    return False

def get_text_from_web(urls):
    # 发送GET请求
    response = requests.get(url=urls, headers=headers, timeout=3.5, verify=False)

    # 检查请求是否成功
    if response.status_code == 200:
        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取网页上的所有文字内容
        text = soup.get_text()

        # 删除每一行中的所有特殊字符并保留换行符
        lines = [line.replace(special_char, '') for line in text.splitlines()]

        global specific_text
        if not is_retying:
            global has_text_title
            if is_first_page and is_first_page_connected_success:
                try:
                    specific_text.remove(juan_number)  # 使只有第一章，第一页有标题。
                except ValueError:
                    pass
                has_text_title = True
            elif not is_first_page_connected_success:
                try:
                    specific_text.remove(juan_number)# 使只有第一章，第一页有标题。
                except ValueError:
                    pass
                has_text_title = True
            elif has_text_title:
                specific_text.append(juan_number)
                has_text_title = False
        else:
            try:
                specific_text.remove(juan_number)
            except ValueError:
                pass


        # 移除包含特定文本的行
        lines1 = [line for line in lines if not is_special_text_in_line(line, specific_text)]

        # 移除空白行
        lines2 = [line for line in lines1 if line.strip() != '']

        # 获取小说的标题并防止标题为空
        global global_text_title
        if not is_retying:
            if is_first_page:
                text_title = [title for title in lines2 if juan_number in title].pop()
                global_text_title = text_title
            elif not is_first_page_connected_success:
                text_title = [title for title in lines2 if juan_number in title].pop()
                global_text_title = text_title

        else:
            text_title = [title for title in lines2 if juan_number in title].pop()
            global_text_title = text_title

        # 将处理后的行重新组合成一个字符串，其中保留了原始的换行符
        cleaned_text = '\n'.join(lines2)

        # 打印或处理获取到的文字内容
        #print(cleaned_text)
        text_path = f'小说\\{novel_title}\\{novel_text_piece} {global_text_title}{first_zhangjie_number}章1.txt' if is_first_page else f'小说\\{novel_title}\\{novel_text_piece} {global_text_title}{first_zhangjie_number}章{page_number}.txt'
        write_result_to_file(cleaned_text, text_path)
        return
    else:
        print('Failed to retrieve the webpage')
        return

def start_requests(current_url, attempts=0):
    while attempts < max_attempts:
        try:
            get_text_from_web(current_url)
            break
        except requests.exceptions.Timeout:
            print(f"{current_url} Connection timed out. Attempting again...")
            attempts += 1

        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            attempts += 1

    if attempts == max_attempts:
        if is_first_page:
            failed_urls[current_url] = (first_zhangjie_number, 1,novel_text_piece)
        else:
            failed_urls[current_url] = (first_zhangjie_number, page_number,novel_text_piece)
        return False
    return True

def download_novel_easier(download_url: str):
    global is_first_page
    global is_last_page
    global is_first_page_connected_success
    global first_zhangjie_number
    global page_number
    global last_zhangjie_number
    global novel_text_piece

    while True:
        # 目标网站的URL
        first_page_url = download_url
        url = f'{download_url.split(".html")[0]}_{page_number}.html'
        if is_first_page:
            if not start_requests(first_page_url):
                is_first_page_connected_success = False
            else:
                is_first_page_connected_success = True
            is_first_page = False
            novel_text_piece += 1

        else:
            if not is_last_page:
                start_requests(url)
                page_number += 1
                novel_text_piece += 1
            else:
                if first_zhangjie_number == last_zhangjie_number:
                    break
                else:
                    #切换到下一张时，重置页码号
                    page_number = 2
                    is_last_page = False
                    is_first_page = True
                    break

def retry_failed_urls():
    global is_retying
    global failed_urls
    global first_zhangjie_number
    global page_number
    global novel_text_piece

    while failed_urls:
        is_retying = True
        url_page_pair = failed_urls.popitem()
        failed_url = url_page_pair[0]
        first_zhangjie_number = url_page_pair[1][0]
        page_number = url_page_pair[1][1]
        novel_text_piece = url_page_pair[1][2]
        # if url_page_pair[1][1] == 1:
        #     page_number = 2
        #     is_first_page = True
        # else:
        #     is_first_page = False
        #     page_number = url_page_pair[1][1]
        start_requests(failed_url)
        print(f"正重新尝试失败的链接... 剩余链接：{len(failed_urls)}")

def main():
    global first_zhangjie_number
    global last_zhangjie_number
    import urllib3
    urllib3.disable_warnings()# 禁用警告信息

    urls_list = delete_pictures_url(get_novel_websites_root_page(root_page_test_url))
    print(urls_list)
    last_zhangjie_number = urls_list[-1][0].split('/')[5].split('.')[0]
    for url_title_pair in urls_list:
        first_zhangjie_number = url_title_pair[0].split('/')[5].split('.')[0]
        download_novel_easier(url_title_pair[0])
    retry_failed_urls()
    print("下载完成！")

    merge_mode = input("是否合并小说？（y/n）")
    if merge_mode == 'y':
        merge_novel_and_remove_repetition_title_of_novel()
    else:
        print("不合并小说！")

def get_novel_websites_root_page(root_page_url):
    global is_first_get_novel_websites_root_page
    try:
        url_list = []
        can_start_collect = False
        # 发送GET请求
        response = requests.get(url=root_page_url, headers=headers, timeout=3.5, verify=False)

        # 检查请求是否成功
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_list = [strs for strs in str(soup).splitlines()]
            for text_line in text_list:
                if juan_number in text_line and is_first_get_novel_websites_root_page:
                    can_start_collect = True
                    is_first_get_novel_websites_root_page = False
                    continue

                if can_start_collect:
                    if '<div class="volume">' in text_line or '</ul>' in text_line:
                        return url_list
                    if '<a href="' in text_line:
                        text_url = text_line.split('href="')[1].split('"')[0]
                        text_title = text_line.split('">')[2].split('</a>')[0]
                        url_list.append((text_url, text_title))
        else:
            print('Failed to retrieve the webpage')
    except requests.exceptions.Timeout:
        get_novel_websites_root_page(root_page_url)


def delete_pictures_url(url_list):
    for tup in url_list:
        if '插图' in tup:
            url_list.remove(tup)
    return url_list

def merge_novel_and_remove_repetition_title_of_novel():
    global novel_title
    print(f"开始合并小说：{novel_title}")
    target_path = f"小说\\{novel_title}"
    output_path = f"小说\\完整小说\\{novel_title}.txt"
    merge_txt.find_and_merge_txt_files(target_path, output_path)
    #删除重复的标题
    input_and_output_path = f"小说/完整小说"
    remove_repetition_title(input_and_output_path)

    print(f"合并完成！")

if __name__ == '__main__':
    main()
