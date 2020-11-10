# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from TANCMS.libs.ES import *
import time
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import json
from TANCMS.libs.kafkaHelper import productMessage

class TancmsPipeline:
    def process_item(self, item, spider):

        type_name = type(item).__name__
        item['type_name'] = type_name
        item_json = json.dumps(item.__dict__['_values'])
        productMessage(item_json)
        return item

        # print('-------------------------------------------11111111111-------')
        # print(type(item).__name__)
        # print(item, item.__dict__['_values'])
        # print(json.dumps(item.__dict__['_values']))
        # print('----2---------------------------------------11111111111-------')


        #
        # should_add = True
        # if item['source'] == '微信公众号':
        #     if isExitByTitle(item['title']):
        #         should_add = False
        # if item['source'] == '新浪新闻' or item['source'] == '微博' or item['source'] == '今日头条':
        #     if isExitByUrl(item['url']):
        #         should_add = False
        # if should_add:
        #     body = {
        #         'programId': 1,
        #         'url': item['url'],
        #         'author': item['author'],
        #         'source': item['source'],
        #         'title': item['title'],
        #         'content': item['content'],
        #         'htmlContent': item['htmlContent'],
        #         'creationTime': int(item['time']),
        #         'addTime': int(time.time())
        #     }
        #     result = es_index('temp_document', body)
        #     print('---------result-----------')
        #     print(result)
        #     # {'_index': 'temp_document', '_type': '_doc', '_id': 'CCrHdXMBiOj1K8cb4WpR', '_version': 1, 'result': 'created',
        #     #  '_shards': {'total': 2, 'successful': 2, 'failed': 0}, '_seq_no': 0, '_primary_term': 1}
        #     print('--------result------------')



# // 下载图片
# class TancmsPipeline(ImagesPipeline):
#
#     def get_media_requests(self, item, info):
#         yield scrapy.Request(url=item['url'], meta={'name': item['title']})
#
#     def file_path(self, request, response=None, info=None):
#         name = request.meta['name'] + '.jpg'
#         return name  # 返回文件名
#
#     def item_completed(self, results, item, info):
#         return item  # 返回给下一个即将被执行的管道类
