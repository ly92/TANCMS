import scrapy

from ..items import ImageItem

class CarLogoSpider(scrapy.Spider):
    name = 'carLogo'
    # startUrl = ['http://mark.mycar168.com/']

    base_url = 'http://mark.mycar168.com/'

    def start_requests(self):
        yield scrapy.Request(self.base_url, callback=self.parse)

    def parse(self, response):
        items = response.xpath('//*[@class="brands"]')
        for item in items:
            title = item.xpath('./p[1]/a/strong/text()').extract_first()
            url = item.xpath('./a/img/@src').extract_first()
            url = url.replace('?x-oss-process=image/resize,m_fill,w_99,h_90', '')
            item = ImageItem()
            item['title'] = title
            item['url'] = url
            print(item)
            # yield item
            pass
