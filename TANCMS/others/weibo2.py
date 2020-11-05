import scrapy



class Weibo2Spider(scrapy.Spider):
    name = 'weibo2'

    base_url = 'https://weibo.com/1730726637/JenFzvV5o?ref=feedsdk&type=comment#_rnd1596622832186'
    word = ''
    page = 1

    cankao = 'https://zhuanlan.zhihu.com/p/65500202'
    cankao2 = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=核酸检测'

    def start_requests(self):
        yield scrapy.Request(url=self.base_url, callback=self.parse)
        pass

    def parse(self, response):
        print(response.text)
        pass

    def account_requests(self, name):
        print(name)
        return 123
        pass


    # 获取账户信息
    def parse_account(self, response):
        print(4)
        pass


