import scrapy
import json
from ..libs.ES import isOldComment
from ..libs.timeHelper import strToTimeStamp
from ..items import CommentItem
import time
from TANCMS.libs.redisHelper import cacheGet


class WeibocommentSpider(scrapy.Spider):
    name = 'weiboComment'

    list_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type={}'
    blogs = cacheGet('weiboComment_blogs')

    blog_id = ''
    max_id = ''
    max_id_type = '0'

    def start_requests(self):
        for blog in self.blogs:
            self.blog_id = blog['blog_id'];
            url = self.list_url.format(self.blog_id, self.blog_id, self.max_id, self.max_id_type)
            time.sleep(5)  # 获取下一页文章前停留一会
            yield scrapy.Request(url=url, meta={
                'dont_redirect': True,
                'handle_httpstatus_list': [302]
            }, callback=self.parse)
        pass

    def parse(self, response):
        res = json.loads(response.text)
        if res['ok']:
            self.max_id = res['data']['max_id']
            self.max_id_type = res['data']['max_id_type']
            data = res['data']['data']
            for item in data:
                comment = CommentItem()
                comment['time'] = item['created_at']
                if not isOldComment(self.blog_id, comment['time']):
                    comment['blog_id'] = self.blog_id
                    comment['id'] = item['id']
                    comment['content'] = item['text']
                    comment['author'] = item['user']['screen_name']
                    comment['author_url'] = 'https://m.weibo.cn/u/' + item['user']['id']
                    comment['auth_id'] = item['user']['id']
                    yield comment

                    url = self.list_url.format(self.blog_id, self.blog_id, self.max_id, self.max_id_type)
                    time.sleep(5)  # 获取下一页文章前停留一会
                    yield scrapy.Request(url=url, meta={
                        'dont_redirect': True,
                        'handle_httpstatus_list': [302]
                    }, callback=self.parse)
