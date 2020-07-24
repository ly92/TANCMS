# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from TANCMS.libs.ES import *
import time


class TancmsPipeline:
    def process_item(self, item, spider):
        should_add = True
        if item['source'] == '微信公众号':
            if isExitByTitle(item['title']):
                should_add = False
        if item['source'] == '新浪新闻' or item['source'] == '微博':
            if isExitByUrl(item['url']):
                should_add = False
        if should_add:
            body = {
                'programId': 1,
                'url': item['url'],
                'author': item['author'],
                'source': item['source'],
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


