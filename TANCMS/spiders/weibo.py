import requests
from TANCMS.libs.ES import es_index, es_query
import time


def weibo(word, page):
    url = 'http://sinanews.sina.cn/interface/type_of_search.d.html?keyword={}&page={}&type=siftWb&size=40&newpage=0&chwm=&imei=&token=&did=&from=&oldchwm='.format(word, page)
    res = requests.get(url).json()
    # print(res)
    data = res['data']['feed1']
    for item in data:
        url2 = item['url']
        if isExit(url2) == False:
            body = {
                'programId': 1,
                'url': item['url'],
                'author': item['user']['name'],
                'source': '微博',
                'title': item['title'],
                'content': item['title'],
                'htmlContent': '',
                'creationTime': int(time.time()),
                'addTime': int(time.time())
            }
            result = es_index('temp_document', body)
            print('--------------------')
            print(result)
            # {'_index': 'temp_document', '_type': '_doc', '_id': 'EC74enMBiOj1K8cbkNND', '_version': 1,
            #  'result': 'created', '_shards': {'total': 2, 'successful': 2, 'failed': 0}, '_seq_no': 342,
            #  '_primary_term': 1}

            print('--------------------')

def isExit(url):
    body = {
        "_source": "title",
        "query": {
            "match_phrase": {
                "url": url
            }
        }
    }
    result = es_query('temp_document', body)
    if result['hits']['total']['value'] > 0:
        return True
    else:
        return False

if __name__ == '__main__':
    word = '核酸检测'
    for i in range(1, 11):
        weibo(word, i)
    print('-------------' + str(i))
    time.sleep(10)