
import requests
from TANCMS.libs.ES import index, query


if __name__ == '__main__':



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
    result = query('temp_document', body)
    if result['hits']['total']['value'] > 0:
        print(result['hits']['total']['value'])
    else:
        print('ooo')

