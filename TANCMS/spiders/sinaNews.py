import scrapy
from ..items import *
import re
import time
from ..libs.ES import isExitArticleByUrl
from TANCMS.libs.timeHelper import formatTime
from TANCMS.libs.redisHelper import cacheGet


class SinanewsSpider(scrapy.Spider):
    name = 'sinaNews'
    # base_url = 'https://search.sina.com.cn/?q={}&c=news&from=&col=&range=all&source=&country=&size=10&stime=m-01-01+00%3A00%3A00&etime=m-12-31+23%3A59%3A59&time=m&dpc=0&a=&ps=0&pf=0&page=1'

    base_url = cacheGet('sinaNews_url')
    word = cacheGet('sinaNews_keyWord')
    page = 0

    def start_requests(self):
        yield scrapy.Request(self.base_url.format(self.word, self.page), callback=self.parse)

    def parse(self, response):
        result = response.xpath('//*[@class="box-result clearfix"]')
        for item in result:
            title_a = item.xpath('./h2/a')
            if not title_a:
                title_a = item.xpath('./div/h2/a')
            url = title_a.xpath('./@href').extract_first()
            if 'html?from' in url:
                url_arr = url.split('?')
                if len(url_arr) > 0:
                    url = url_arr[0]
                # url = re.findall('(.*?)from', url, re.S)[0]
            #判断是否已爬取
            if isExitArticleByUrl(url):
                continue

            title = re.findall('target="_blank">(.*?)</a>', title_a.get(), re.S)[0].replace('</font>', '').replace('<font color="red">', '')

            author_time = item.xpath('./h2/span/text()').extract_first()
            if not author_time:
                author_time = item.xpath('./div/h2/span/text()').extract_first()
            author_time = author_time.split(' ')
            author = author_time[0].strip()
            time_str = author_time[1] + ' ' + author_time[2]
            time_date = formatTime(time_str)

            item = ArticleItem()
            item['title'] = title
            item['url'] = url
            # item['htmlContent'] = ''
            # item['content'] = ''
            item['author'] = author
            item['time'] = time_date
            time.sleep(3)  # 每获取一个文章都停留一会
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_content, meta={'item': item})

        page_inner = response.xpath('//*[@class="pagebox"]/a')
        if len(page_inner) > 0 and self.page < 40:
            last_a = page_inner[-1]
            if last_a.xpath('./text()').extract_first() == '下一页':
                self.page = self.page + 1
                url = self.base_url.format(self.word, self.page)
                time.sleep(3)  # 获取下一页文章前停留一会
                yield scrapy.Request(url=url, callback=self.parse)


    # 进入到详情页面 爬取新闻内容
    def parse_content(self, response):

        content = ''.join(response.xpath('//*[@id="artibody" or @id="article"]//p/text()').extract())
        content = re.sub(r'\u3000', '', content)
        content = re.sub(r'[ \xa0?]+', ' ', content)
        content = re.sub(r'\s*\n\s*', '\n', content)
        content = re.sub(r'\s*(\s)', r'\1', content)
        content = ''.join([x.strip() for x in content])

        item = response.meta['item']
        item['htmlContent'] = response.xpath('//*[@id="artibody" or @id="article"]').extract_first()
        item['content'] = content
        item['source'] = '新浪新闻'

        # content_list = response.xpath('//*[@id="artibody" or @id="article"]//p/text()').extract()
        # content = r""
        # for part in content_list:
        #     part = part.strip()
        #     content += part

        yield item
