
import requests
from TANCMS.libs.ES import es_query
import re

from TANCMS.others.weibo2 import Weibo2Spider
from TANCMS.spiders.tieba import TiebaSpider




def weibo():
    url = 'http://sinanews.sina.cn/interface/type_of_search.d.html?keyword=核酸检测&page=1&type=siftWb&size=40&newpage=0&chwm=&imei=&token=&did=&from=&oldchwm='
    res = requests.get(url).json()
    # print(res)
    data = res['data']['feed1']
    for item in data:
        print(item['url'])
        print(item['title'])





def es():
    title = '核酸检测成敛财神器？笑话'
    querys = {
        'match_phrase': {
            'title': title
        }
    }
    source = ['title']
    body = {
      "_source": "hits",
      "query": {
          "match_phrase": {
          "title": "核酸检测成敛财神器？笑话"
        }
      }
    }
    result = es_query('temp_document', body)
    if result['hits']['total']['value'] > 0:
        print(result['hits']['total']['value'])
    else:
        print('ooo')


def toutiao():
    url = 'https://www.toutiao.com/a6789420137695937036/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'}
    cookies = {'Cookie': 'tt_webid=6852555023949055502; SLARDAR_WEB_ID=17e68dd5-413f-4a53-985a-74741b5787fb; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6852555023949055502; ttcid=e6d60e08fd274878a5f2e5f36d59d14423; csrftoken=77e3e4ab4ed91bd489c90fe75b8dda75; __ac_nonce=05f20d64a00614f7f5901; __ac_signature=_02B4Z6wo00f01TLEMKAAAIBDQUf9Twicr5kywTQAABOTbepHoCWGpcEaPwtZzjgUd68tRwa.y7naKHmHC7FpKhMw2qBuANc44gFElv8.XgqAOK6phJwTykLb2vJ3b-ybh.HzFXFgBLF4SW1-96; s_v_web_id=verify_kd6prq0z_7QFabeh0_kdX4_4iV3_8ckT_jJFuyRBC8GJ7; __tasessionId=gi8o8fjf71595987533418; tt_scid=ZucU8KVk8KZJe8LtNSyh00rjkQ3SXsZywUSueVPLg-D0.I1rRchyHtdpO6XAzt8ia929'}
    response = requests.get(url, headers=headers, cookies=cookies)

    print(response.status_code)
    print(response.text)

    print('--------------------')



    articleInfo = re.findall('articleInfo: {(.*?)groupId', response.test, re.S)[0]

    content = re.findall('content:(.*?)', articleInfo, re.S)[0]

    print(content)


def weibo2():
    weibo = Weibo2Spider()

    r = weibo.account_requests('00000')
    print(r)


def tieba():
    tieba = TiebaSpider('核酸检测', '庄河')
    # tieba = TiebaSpider()

    print(tieba.ba_requests())


if __name__ == '__main__':
    es()


