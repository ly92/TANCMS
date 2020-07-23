
import requests
from TANCMS.libs.ES import es_index, es_query




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


if __name__ == '__main__':
    weibo()


