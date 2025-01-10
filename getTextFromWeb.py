import requests
from bs4 import BeautifulSoup

zhangjie_number = 156997
page_number = 2
is_first_page = True
is_last_page = False
last_zhangjie_number = 157001
juan_number = "第10.5卷"
global_text_title = "第10.5卷 长谷栞奈突如其来的教育旅行"
has_text_title = True
is_retying = False
is_first_page_connected_success = True

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
	"referer": "https://www.wenkuchina.com/lightnovel/2081/catalog",
}

# 定义需要删除的特殊字符和特定文本
special_char = '  '
failed_urls = {}
max_attempts = 3
#让一章的总标题在一章内只会在这一章的开头出现一次。
specific_text = ['上一章点赞目录+书签下一页','上一章点赞目录+书签下一章','上一页点赞目录+书签下一章',
                '上一页点赞目录+书签下一页','轻之文库轻小说-懂阅读更懂创作的轻小说平台-发现和创造有趣的故事-日本动漫轻小说在线阅读',
                '当前位置:轻之文库轻小说-懂阅读更懂创作的轻小说平台-',juan_number]

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
    response = requests.get(url=urls, headers=headers, timeout=3.5)

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
                specific_text.remove(juan_number)  # 使只有第一章，第一页有标题。
                has_text_title = True
            elif not is_first_page_connected_success:
                specific_text.remove(juan_number)  # 使只有第一章，第一页有标题。
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
        text_path = f'back\\小说\\{global_text_title}{zhangjie_number}章1.txt' if is_first_page else f'back\\小说\\{global_text_title}{zhangjie_number}章{page_number}.txt'
        with open(text_path, 'a', encoding='utf-8') as f:
            f.write(cleaned_text)
            if is_first_page:
                print(f"{global_text_title} 第{zhangjie_number} 章 第1 页 已保存")
            else:
                print(f"{global_text_title} 第{zhangjie_number} 章 第{page_number} 页 已保存")
        return
    else:
        print('Failed to retrieve the webpage')
        return

def start_requests(current_url,attempts=0):
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
        failed_urls[current_url] = (zhangjie_number,page_number)
        return False
    return True

if __name__ == '__main__':

    while True:
        # 目标网站的URL
        first_page_url = f'https://www.wenkuchina.com/lightnovel/2081/{zhangjie_number}.html'
        url = f'https://www.wenkuchina.com/lightnovel/2081/{zhangjie_number}_{page_number}.html'
        if is_first_page:
            if not start_requests(first_page_url):
                is_first_page_connected_success = False
            else:
                is_first_page_connected_success = True
            is_first_page = False

        else:
            if not is_last_page:
                start_requests(url)
                page_number += 1
            else:
                if zhangjie_number == last_zhangjie_number:
                    break
                else:
                    page_number = 2
                    text_piece = 1
                    zhangjie_number += 1
                    is_last_page = False
                    is_first_page = True

    while failed_urls:
        is_retying = True
        url_page_pair = failed_urls.popitem()
        failed_url = url_page_pair[0]
        page_number = url_page_pair[1][1]
        zhangjie_number = url_page_pair[1][0]
        start_requests(failed_url)
        print(f"正重新尝试失败的链接... 剩余链接：{len(failed_urls)}")
    print("\n" "Failed URLs:", failed_urls)