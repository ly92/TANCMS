import scrapy
import re
import time
from ..items import ArticleItem
from ..libs.ES import isExitByUrl
from TANCMS.libs.redisHelper import cacheGet


class TianyaSpider(scrapy.Spider):
    name = 'tianya'
    # base_url = 'https://search.tianya.cn/bbs?q={}&pn={}&s=4'
    # word = '核酸检测'
    page = 1
    last_time = int(time.time())
    have_more = True
    base_url = cacheGet('tianya_url')
    word = cacheGet('tianya_keyWord')

    def start_requests(self):

        url = self.base_url.format(self.word, self.page)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        ul = response.xpath('//*[@class="searchListOne"]/ul/li')
        for li in ul:
            try:
                url = li.xpath('./div/h3/a/@href').extract_first()
                if isExitByUrl(url):
                    continue
                title = li.xpath('./div/h3/a').get()
                title = title.replace('<span class="kwcolor">', '').replace('</span>', '')
                title = re.findall('target="_blank">(.*?)</a>', title, re.S)[0]
                author = li.xpath('./p/a[2]/text()').extract_first()
                time_str = li.xpath('./p/span[1]/text()').extract_first()
                timeArray = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                timeStamp = int(time.mktime(timeArray))
                item = ArticleItem()
                item['title'] = title
                item['url'] = url
                item['htmlContent'] = ''
                item['content'] = ''
                item['source'] = '天涯论坛'
                item['author'] = author
                item['time'] = timeStamp
                self.last_time = timeStamp
                yield scrapy.Request(url=url, callback=self.parse_content, meta={'item': item})
            except:
                pass
            time.sleep(2)

        if len(ul) > 0 and int(time.time()) - self.last_time < 86400 * 30:
            self.page = self.page + 1
            url = self.base_url.format(self.word, self.page)
            time.sleep(3)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_content(self, response):
        contents = response.xpath('//*[@class="bbs-content clearfix"]/text()').extract()
        content = "\\n".join(contents)
        content = content.replace('\\u3000', ' ').replace('\\n', '').replace('\\t', '')
        item = response.meta['item']
        item['content'] = content
        yield item
