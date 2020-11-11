import scrapy
import time
import re
from ..libs.ES import isExitArticleByUrl
import json
# from TANCMS.items import ArticleItem
from TANCMS.libs.redisHelper import cacheGet
from TANCMS.items import BlogItem, ArticleItem, CommentItem
from TANCMS.libs.timeHelper import formatTime

class BjhSpider(scrapy.Spider):
    name = 'bjh'
    end = int(time.time())
    begin = int(time.time()) - 86400 * 1
    pn = 0
    base_url = cacheGet('bjh_url')
    word = cacheGet('bjh_keyWord')
    # word = word.replace(' ', '')

    def start_requests(self):
        url = self.base_url.format(self.word, self.begin, self.end, self.pn)
        # url = 'https://www.baidu.com/s?wd=site%3A(baijiahao.baidu.com)%20%E6%A0%B8%E9%85%B8%E6%A3%80%E6%B5%8B%20%22%E6%A0%B8%E9%85%B8%E6%A3%80%E6%B5%8B%22&pn=590&oq=site%3A(baijiahao.baidu.com)%20%E6%A0%B8%E9%85%B8%E6%A3%80%E6%B5%8B%20%22%E6%A0%B8%E9%85%B8%E6%A3%80%E6%B5%8B%22&tn=baiduadv&ie=utf-8&rsv_pq=8376447d00012935&rsv_t=f417SpYSfphz919Y8r5JmFgQurFxLYlFJFoeRnjLBVKkfWTYzBiYkw1xmnUfe14&gpc=stf%3D1604459975.888%2C1604546375.888%7Cstftype%3D1'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        divs = response.xpath('//*[@class="result c-container new-pmd"]')
        for div in divs:
            url = div.xpath('./h3/a/@href').extract_first()
            title_str = div.xpath('./h3/a').get()
            title_str = title_str.replace('<em>', '').replace('</em>', '')
            title = re.findall('target="_blank">(.*?)</a>', title_str, re.S)[0]
            item = ArticleItem()
            item['title'] = title
            item['url'] = url
            item['htmlContent'] = ''
            item['content'] = ''
            item['source'] = '百家号'
            time.sleep(3)  # 每获取一个文章都停留一会
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_content, meta={'item': item})
        page_inner = response.xpath('//*[@class="page-inner"]/a')
        if len(page_inner) > 0 and self.pn < 400:
            last_a = page_inner[-1]
            if last_a.xpath('./text()').extract_first() == '下一页 >':
                self.pn += 10
                url = self.base_url.format(self.word, self.begin, self.end, self.pn)
                print(url)
                time.sleep(3)  # 获取下一页文章前停留一会
                yield scrapy.Request(url=url, callback=self.parse)

    def parse_content(self, response):
        s_advert = re.findall('var s_advert = (.*?);', response.text, re.S)[0]
        s_advert = json.loads(s_advert)
        url = s_advert['contentUrl']
        if not isExitArticleByUrl(url):
            time_source = response.xpath('//*[@class="author-txt"]')
            t1 = time_source.xpath('./div/span[1]/text()').extract_first()
            t2 = time_source.xpath('./div/span[2]/text()').extract_first()
            year_a = time.localtime(time.time())
            year = time.strftime("%Y-", year_a)
            time_str = year + t1.replace('发布时间：', '') + ' ' + t2
            createTime = formatTime(time_str)
            author = time_source.xpath('./p/text()').extract_first()
            content_p = response.xpath('//*[@class="article-content"]/p')
            content = ''
            try:
                for p in content_p:
                    spans = p.xpath('./span')
                    p_str = ''
                    for span in spans:
                        s = span.xpath('./text()').extract_first()
                        if s:
                            p_str = p_str + s
                    content += p_str + "\n"
            except:
                pass
            item = response.meta['item']
            item['content'] = content
            item['htmlContent'] = response.xpath('//*[@class="article-content"]').get()
            item['time'] = createTime
            item['author'] = author
            item['url'] = url
            yield item




