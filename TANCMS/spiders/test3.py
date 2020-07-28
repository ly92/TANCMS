import requests
import time
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from urllib.parse import quote
import re



article_url_list = [
"https://www.toutiao.com/a6839663324880175628",
"https://www.toutiao.com/a6844326277470487048",
"https://www.toutiao.com/a6851892844526764552",
"https://www.toutiao.com/a6789420137695937036",
"https://www.toutiao.com/a6830715574046163464",
"https://www.toutiao.com/a6820727747896148487",
"https://www.toutiao.com/a6839671456377340431",
"https://www.toutiao.com/a6839695666277515783",
"https://www.toutiao.com/a6851341292123881991",
"https://www.toutiao.com/a6799087725220725251",
"https://www.toutiao.com/a6850682198123610631",
"https://www.toutiao.com/a6851721201509728782",
"https://www.toutiao.com/a6825798946305081863",
"https://www.toutiao.com/a6841008552430010887",
"https://www.toutiao.com/a6841564474437009923",
"https://www.toutiao.com/a6839706696772747790",
"https://www.toutiao.com/a6824841230841545220",
"https://www.toutiao.com/a6843321916363637256",
"https://www.toutiao.com/a6854083935069012480",
"https://www.toutiao.com/a6840433779157238285",
"https://www.toutiao.com/a6843633723502494219",
"https://www.toutiao.com/a6839837878588015112",
"https://www.toutiao.com/a6839491653925863943",
"https://www.toutiao.com/a6841035878735806984",
"https://www.toutiao.com/a6819609973044019723",
"https://www.toutiao.com/a6845050852307108360",
"https://www.toutiao.com/a6853788005262590476",
"https://www.toutiao.com/a6841520596384219660",
"https://www.toutiao.com/a6819622573316243982",
"https://www.toutiao.com/a6846634006302327307",
"https://www.toutiao.com/a6838915054977417742",
"https://www.toutiao.com/a6851847108102717966",
"https://www.toutiao.com/a6840631007717097997",
"https://www.toutiao.com/a6839288470242853383",
"https://www.toutiao.com/a6839081876615856655",
"https://www.toutiao.com/a6840998791298941448",
"https://www.toutiao.com/a6841400778775593479",
"https://www.toutiao.com/a6799812696314216974",
"https://www.toutiao.com/a6818009718531817992",
"https://www.toutiao.com/a6820977414303121928",
"https://www.toutiao.com/a6851167913513222670",
"https://www.toutiao.com/a6815565787923743235",
"https://www.toutiao.com/a6834003899276329472",
"https://www.toutiao.com/a6821299947074224653",
"https://www.toutiao.com/a6852894410007380493",
"https://www.toutiao.com/a6820314114590507532",
"https://www.toutiao.com/a6818156248580489736",
"https://www.toutiao.com/a6852712029287875086",
"https://www.toutiao.com/a6821027605894922759",
"https://www.toutiao.com/a6843298757463769607",
"https://www.toutiao.com/a6820647949194756620",
"https://www.toutiao.com/a6818001392515416583",
"https://www.toutiao.com/a6832905281857389071",
"https://www.toutiao.com/a6841348279796498958",
"https://www.toutiao.com/a6851890411007705604",
"https://www.toutiao.com/a6852265543357956622",
"https://www.toutiao.com/a6843318310684066318",
"https://www.toutiao.com/a6841698870842360327",
"https://www.toutiao.com/a6840408504507826703",
"https://www.toutiao.com/a6841778429390488071",
"https://www.toutiao.com/a6841387365815026189",
"https://www.toutiao.com/a6841512776322515464",
"https://www.toutiao.com/a6841512882102862344"
]




page_urls = ["http://dev.kdlapi.com/testproxy",
             "https://dev.kdlapi.com/testproxy",
             ]
ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5'
# 隧道服务器
tunnel_host = "tps189.kdlapi.com"
tunnel_port = "15818"

# 隧道用户名密码
tid = "t17888082960619"
password = "gid72p4o"

proxies = {
    "http": "http://%s:%s@%s:%s/" % (tid, password, tunnel_host, tunnel_port),
    "https": "https://%s:%s@%s:%s/" % (tid, password, tunnel_host, tunnel_port)
}

# 防止重复
constract_list = []

# 获取到一个页面内所有的article url

def request_AND_storage(name):
    options = Options()
    options.add_argument('-headless')
    driver = Firefox(executable_path='/usr/local/Cellar/geckodriver/0.26.0/bin/geckodriver', firefox_options=options)
    time.sleep(2)
    for url in article_url_list:
        print(url)
        try:
            driver.get(url)
            time.sleep(1)
            text_res = driver.find_element_by_xpath(
                '//div[@class="article-box"]')
            text_res = text_res.text
            print(text_res)
        except:
            print('--------------')
            continue
    driver.close()

def request_detail(url):

    print(url)

    # 这里替换成你自己的浏览器信息
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    # 头条图片搜索需要滑动验证，因此简单处理，先手动验证，然后设置cookie
    cookie = 'tt_webid=6696746174420534791; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16b0805ea6f31d-02830a8210d05a-37627e03-1fa400-16b0805ea705fd; tt_webid=6696746174420534791; __tasessionId=znvodagrm1559207733945; csrftoken=7201998104473d4e2ad8302bb74ae401; s_v_web_id=600eabfd649cb7a70f3d80b981411bfc; CNZZDATA1259612802=1444442826-1559202415-%7C1559207815'
    headers = {
        'Host': 'www.toutiao.com',
        'Referer': 'https://www.toutiao.com/search/?keyword=核酸检测',
        'User-Agent': user_agent,
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': cookie
    }
    try:
        # 这里需要使用session的方式，否则会因为重定向次数太多而报错
        session = requests.Session()
        session.headers['User-Agent'] = headers['User-Agent']
        resp = session.get(url)
        if resp.status_code == 200:
            articleInfos = re.findall('articleInfo: {(.*?)groupId', resp.text, re.S)
            if len(articleInfos) > 0:
                contents = re.findall('content:(.*?)groupId', articleInfos[0], re.S)
                if len(contents) > 0:
                    print(contents)
                else:
                    print(1)
            else:
                print(2)

            # soup = BeautifulSoup(resp.text, 'lxml')
            # result = soup.find_all(name='script')[6]
            # regex = '.*?img src&#x3D;&quot;(.*?)&quot;.*?'
            # items = re.findall(regex, resp.text, re.S)
            # if items:
            #     for item in items:
            #         print(item)
            # else:
            #     print(2)
        else:
            print('1')
    except requests.ConnectionError:
        print('Get image fail.')



if __name__ == '__main__':
    # for url in article_url_list:
    #     request_detail(url)
    #     time.sleep(5)
    try:
        request_AND_storage('武汉疫情')
        article_url_list = []
        time.sleep(10)
    except Exception as e:
        print(e)
        article_url_list = []
        time.sleep(1)
