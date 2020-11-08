from scrapy.commands import ScrapyCommand
from scrapy.utils.project import get_project_settings
from TANCMS.libs.redisHelper import cacheGet
import json

class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'run all spiders'

    def run(self, args, opts):
        spider_list = cacheGet('spiders')
        spider_list = json.loads(spider_list)
        for name in spider_list:
            print(name)
            self.crawler_process.crawl(name, **opts.__dict__)
        self.crawler_process.start()

        # spider_list = self.crawler_process.spiders.list()
        # for name in spider_list:
        #     print(name)
        #     self.crawler_process.crawl(name, **opts.__dict__)
        # self.crawler_process.start()