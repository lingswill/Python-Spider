import requests
import time
import random
import parsel
import jieba
import imageio
import wordcloud


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


page_count = 0
comment_types = ('h', 'm', 'l')
for c_type in comment_types:
    for page in range(0, 481, 20):
        page_count += 1
        print(
            f'=====================正在读取第{page_count}页短评数据====================='
        )
        url = f'https://movie.douban.com/subject/34841067/comments?percent_type={c_type}&start={page}&limit=20&status=P&sort=new_score'
        header = get_user_agent()
        response = requests.get(url=url, headers=header)
        html_data = response.text

        # 数据的解析
        # 转换数据类型
        selector = parsel.Selector(html_data)
        comments_list = selector.xpath(
            '//span[@class="short"]/text()').getall()

        # 数据的保存
        with open(r'.\HiMom\resources\HiMom_comments.txt',
                  mode='a',
                  encoding='utf-8') as f:
            for comment in comments_list:
                f.write(comment.replace('\n', ''))
                f.write('\n')

        time.sleep(10)

with open(r'.\HiMom\resources\HiMom_comments.txt', mode='r',
          encoding='utf-8') as f:
    txt = f.read()

with open(r'.\HiMom\resources\cn_stopwords.txt', mode='r',
          encoding='utf-8') as f:
    stopwords = f.readlines()

stopwords_list = []
for k in stopwords:
    stopwords_list.append(k.strip())

# 中文分词
text_list = jieba.lcut(txt)
comment_string = ''.join(text_list)

# 词云制作
img = imageio.imread(r'.\resources\lihuanying.png')
comment_wordclooud = wordcloud.WordCloud(width=1080,
                                         height=675,
                                         background_color='white',
                                         font_path='msyh.ttc',
                                         mask=img,
                                         scale=15,
                                         stopwords=stopwords_list)

# 给词云图输入文字
comment_wordclooud.generate(comment_string)
comment_wordclooud.to_file('hiMom_wordCloud.png')