import requests
from bs4 import BeautifulSoup
import xlwt
import json
import random
import time

comment_list = []


def get_user_agent():
    first_num = random.randint(55, 76)
    third_num = random.randint(0, 3800)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)',
        '(X11; Linux x86_64)', '(Macintosh; Intel Mac OS X 10_14_5)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num,
                                                fourth_num)
    user_agent = ' '.join([
        'Mozilla/5.0',
        random.choice(os_type), 'AppleWebKit/537.36', '(KHTML, like Gecko)',
        chrome_version, 'Safari/537.36'
    ])
    headers = {"User-Agent": user_agent}
    return headers


def request_douban(url, headers, params, proxy=None):
    try:
        response = requests.get(url,
                                headers=headers,
                                params=params,
                                proxies=proxy)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        print("-----网络请求出错-----")
        return None


def get_movies(page_start):
    top_params = {
        'type': 'movie',
        'tag': '热门',
        'sort': 'recommend',
        'page_limit': '20',
        'page_start': page_start
    }
    movies_url = 'https://movie.douban.com/j/search_subjects'
    headers = get_user_agent()
    douban_json = request_douban(movies_url, headers, top_params)
    if douban_json is None:
        return None
    movies_msg = json.loads(douban_json)
    movies = movies_msg["subjects"]
    return movies


def get_comments(start, movie_id):
    params = {
        'sort': 'new_score',
        'status': 'P',
        'limit': '20',
        'start': start
    }
    comment_url = 'https://movie.douban.com/subject/' + movie_id + '/comments'
    html = request_douban(comment_url, get_user_agent(), params)
    soup = BeautifulSoup(html, "html.parser")
    comment_items = soup.find_all('div', class_="comment-item")
    try:
        for item in comment_items:
            item_name = item.div.a.get('title')
            item_comment = item.find('span', class_="short").getText()
            movie_comment = {'user_name': item_name, 'comment': item_comment}
            comment_list.append(movie_comment)
    except:
        print('-----获取短评失败-----')
    return comment_list


def write_excel_xls(path, value):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("短评")
    i = 0
    for item in value:
        sheet.write(i, 0, item.get('user_name'))
        sheet.write(i, 1, item.get('comment'))
        i += 1
    workbook.save(path)
    comment_list.clear()
    print("-----xls表格数据写入成功-----")


def main(topNum):
    movies = get_movies(topNum)
    if movies is None:
        print("-----获取电影信息失败-----")
        return
    for movie in movies:
        print("正在获取电影<%s>短评信息..." % movie["title"])
        for i in range(0, 200, 20):
            get_comments(i, movie["id"])
            time.sleep(10)
        path = movie["title"] + ".xls"
        write_excel_xls(path, comment_list)


if __name__ == '__main__':
    #获取热门电影豆瓣短评
    main(0)
