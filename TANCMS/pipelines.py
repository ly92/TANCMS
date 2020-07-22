# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from TANCMS.libs.ES import index
import time


class TancmsPipeline:
    def process_item(self, item, spider):
        body = {
            'programId': 1,
            'url': item['url'],
            'author': item['author'],
            'source': '微信公众号',
            'title': item['title'],
            'content': item['content'],
            'creationTime': int(item['time']),
            'addTime': int(time.time())
        }
        result = index('temp_document', body)
        print('--------------------')
        print(result)
        # {'_index': 'temp_document', '_type': '_doc', '_id': 'CCrHdXMBiOj1K8cb4WpR', '_version': 1, 'result': 'created',
        #  '_shards': {'total': 2, 'successful': 2, 'failed': 0}, '_seq_no': 0, '_primary_term': 1}

        print('--------------------')

        return item
