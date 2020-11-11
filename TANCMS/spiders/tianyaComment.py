import scrapy
import re
from ..libs.timeHelper import strToTimeStamp
import time
from TANCMS.libs.redisHelper import cacheGet
from ..items import CommentItem
from urllib import parse
from ..libs.ES import isOldComment


class TianyacommentSpider(scrapy.Spider):
    name = 'tianyaComment'

    base_url = ''
    blogs = cacheGet('tianyaComment_blogs')
    blog_id = ''
    page = 1
    start_urls = [
        # 'https://www.toutiao.com/a6841348279796498958',
        'https://www.toutiao.com/a6844326277470487048'
        # 'https://www.toutiao.com/a6882623302062309902'
        # 'https://www.toutiao.com/a6830715574046163464'
    ]

    def start_requests2(self):
        for blog in self.blogs:
            url = blog['url']
            self.blog_id = blog['blog_id']
            self.base_url = url + '?&pn={}'
            yield scrapy.Request(url=url, callback=self.parse_content)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_content)

    def parse_content(self, response):

        title = response.xpath('/html/body/div[1]/div/div[2]/div[1]/div[2]/article/p[1]').extract_first()
        print(title)

        # title_h = response.xpath('/html/body/div[1]/div/div[2]/div[1]/div[2]/h1').extract_first()
        # print(title_h)
        # print(response.text)
        # spans = response.xpath('//*[@class="article-meta"]/span')
        # for span in spans:
        #     print(span.xpath('./text()'))

        pass


    def get_content(self, text):
        articleInfos = re.findall('articleInfo: {(.*?)groupId', text, re.S)
        if len(articleInfos) > 0:
            contents = re.findall('content: (.*?)slice', articleInfos[0], re.S)
            if len(contents) > 0:
                content = contents[0]
                content = content.replace('&nbsp;', ' ').replace('\\u003C', '<').replace('\\u003E', '>').replace(
                    '&amp;', '&').replace('&quot;', '').replace('\\u002F', '/').replace('<br>', '').replace('收藏 举报', '')
                ps = re.findall('<p>(.*?)</p>', content, re.S)
                content = "\n".join(ps)
                return content
        else:
            return ''

