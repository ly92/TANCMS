# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from TANCMS.libs.ES import es_index, es_query
import time


class TancmsPipeline:
    def process_item(self, item, spider):
        if self.isExit(item['title']) == False:
            body = {
                'programId': 1,
                'url': item['url'],
                'author': item['author'],
                'source': '微信公众号',
                'title': item['title'],
                'content': item['content'],
                'htmlContent': item['htmlContent'],
                'creationTime': int(item['time']),
                'addTime': int(time.time())
            }
            result = es_index('temp_document', body)
            print('--------------------')
            print(result)
            # {'_index': 'temp_document', '_type': '_doc', '_id': 'CCrHdXMBiOj1K8cb4WpR', '_version': 1, 'result': 'created',
            #  '_shards': {'total': 2, 'successful': 2, 'failed': 0}, '_seq_no': 0, '_primary_term': 1}

            print('--------------------')

        return item

    def isExit(self, title):
        body = {
            "_source": "title",
            "query": {
                "match_phrase": {
                    "title": title
                }
            }
        }
        result = es_query('temp_document', body)
        if result['hits']['total']['value'] > 0:
            return True
        else:
            return False
