import scrapy
import re

from TANCMS.items import ArticleItem

class ArticleSpider(scrapy.Spider):
    name = "article"
    allowed_domains = ["mp.weixin.qq.com"]
#     start_urls = [
#         'https://mp.weixin.qq.com/s?src=11&timestamp=1595380912&ver=2475&signature=FQ19As8jwwNNdmOBZPtCFGUvNzAszaTve9c7oCiYmE5xTzAIzNrK1HiQxcPq57av2qG1hvtgbF6WZrgmI4E0RN0SSMaIi*ZlE5Wadot5LjqHr2t3E0sbvB95gn4FMSwG&new=1',
# 'https://mp.weixin.qq.com/s?src=11&timestamp=1595380912&ver=2475&signature=mFNO9u3V8pK02jb4axnpc9Q8qM5hqxnLkg*xIZla-nLACMbMLMR6XpnCwGdj7TfPPtXh1RBdfickm0y*q-38CMfQcdw-f9*gwcB3XqJuZk5RKUmjy0IVHz4N8CjGZ3yy&new=1',
# 'https://mp.weixin.qq.com/s?src=11&timestamp=1595380912&ver=2475&signature=iZdx1JMTZ0W35QknV*QvxvSLvfJBo*xHop708anUeyaMJXI0lxIzCb9g-sHMb5apNjkr7glXakUP-uIHeO6Nff1NSlJkcktyhFeLvqdCSUsst5eLMsMfFyLwmP7JUuhU&new=1',
# 'https://mp.weixin.qq.com/s?src=11&timestamp=1595380912&ver=2475&signature=0urGvIQ5CEbFbjmgXLeeGNBwK0yom*t2kv6oykFdhn8L0IFGWuChZ1vVRXIGh3kpuKRQjNahJLg6k2FIoInazTsqI5CGvhWzoOxVpuZwzdyMzzEzXGA6uK9jabSd*EUp&new=1',
# 'https://mp.weixin.qq.com/s?src=11&timestamp=1595380912&ver=2475&signature=0urGvIQ5CEbFbjmgXLeeGNBwK0yom*t2kv6oykFdhn*z2uNXGiz2XOn87qdyDUkRijTK6ikS5JQRBhnQwzcOY8d95daQF3gBVtb82e8ZJJYRRuUK-HYtCDYTau-qtUjU&new=1',
# 'https://mp.weixin.qq.com/s?src=11&timestamp=1595380912&ver=2475&signature=4giUnjPieXIDFQLEVqsJTkMdftSYsRl02SrYvmaKWstu5Qy6PjmusXDttrVBpPtRGRQWb*JvrkMb*2lrQu0vnKhlfZWVh9l64YnoIZPM684bOEdGf3CQc8doHq3cLvO8&new=1',
# 'https://mp.weixin.qq.com/s?src=11&timestamp=1595380912&ver=2475&signature=ZamHFf3WBKmYRVDfeY-pYspZGARoFFwcY3MCb4c5QjjHJGucNScNhBXKBo-H0J5*znWdicw-Fi9o3cGJQZNzcTHK3y3FVhZ9puSnkLFkmLFH19VUErPhP50UQhp99t7o&new=1',
# 'https://mp.weixin.qq.com/s?src=11&timestamp=1595380912&ver=2475&signature=2J2uGMzgaDdfZhLrmD2Yg2RoCHWi6-sqL1yRNDqh6F19-syZL9TQndA7m4gFwm*TlsHvmP6YEIjZ09c87gyvlpxwsY*0jhaolaluimYzD3TUuxmlEJZyaqyz1R9*lhz0&new=1',
# 'https://mp.weixin.qq.com/s?src=11&timestamp=1595380912&ver=2475&signature=oDXd6HO-C*qZ8-UNm14*n2Dn5pnzkxZEQajTZWQnJPItRDkrHnPjvpn7QDKFq3xdpf1vDRPjiMfG1ueOM9gWVnx*UhalXWh1oLlI7HiQKLCGVmLZz*1vxALtm34nzgLb&new=1',
# 'https://mp.weixin.qq.com/s?src=11&timestamp=1595380912&ver=2475&signature=rlCTjgNvE-Lkk5luRE7UZGI95WxARwp1h4K3CaT8GZdYjPsH3xxdPDCc1Ev585bieYfxRYB9tZFQUVy-tlxkyBVX1PA6Kca2aPSPT*9zgUheBJrPENbc7QYbBC8kJ*8h&new=1'
#     ]
    start_urls = [
'https://mp.weixin.qq.com/s?src=11&timestamp=1595471613&ver=2477&signature=B8SmKrlQPKoriiEZG8tTvIgZO1l8dAF**revwMkWsRBGwL7NYwy92M2OVtlL6efWKRtrMPzXp-wFHkTNUIGvlHTEQKB*nhSoALDJ*ejd1bbHkPi0Lp-HqU0skhDhUvF7&new=1'    ]

    def getTime(self, response):
        ct = re.findall('var ct = (.*?);', response.text, re.S)[0]
        ct = ct.replace('"', '')
        return ct

    def parse(self, response):
        content = response.xpath('//div[@id="js_content"]')
        text_lines = content.xpath('.//span')

        results = ''

        for i, text_line in enumerate(text_lines):
            if text_line:
                span_text = text_line.xpath('.//text()').extract_first()
                if span_text:
                    results = results + "\n" + span_text.strip()
        print(results)

        return

        item = GzhItem()
        item['title'] = response.xpath('//h2[@id="activity-name"]/text()').extract_first().strip()
        item['url'] = response.url
        item['content'] = response.xpath('//div[@id="js_content"]').extract_first()
        item['author'] = response.xpath('//*[@id="js_name"]/text()').extract_first().strip()
        item['time'] = self.getTime(response)
        print(item)
        pass