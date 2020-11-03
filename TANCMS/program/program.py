import requests
import json
import time
import entity

from scrapy import cmdline

# 监控列表
def requestProgram():
    url = "http://iyanshan.com/spider/program/list"
    beginTime = time.time()
    endTime = time.time() + 86400
    data = {"status": "1", "beginTime": beginTime, "endTime": endTime}
    res = request(url, data)
    return res['data']
# 监控详情
def programDetail(id):
    url = "http://iyanshan.com/spider/program/detail"
    data = {"id": id}
    res = request(url, data)
    return res['detail']

# 网站详情
def networkDetail(id):
    url = "http://iyanshan.com/spider/network/detail"
    data = {"id": id}
    res = request(url, data)
    return res['detail']


# 处理请求
def request(url, data):
    response = requests.post(url=url, json=data)
    res = json.loads(response.content)
    if res['code'] == 0:
        return res['content']
    else:
        raise Exception(res['message'])

# 开始爬虫
def startSpider(type):
    print(entity.keyWord)
    # shell = 'scrapy crawl ' + type
    # cmdline.execute(shell.split())

# 准备爬虫
def prepareWork():
    try:
        list = requestProgram()
        for program in list:
            detail = programDetail(program['id'])
            # print(detail)
            # 搜索关键词
            keyWords = detail['keywords']
            key = ''
            for word in keyWords:
                key += ' ' + word['word']
            # print(key)
            entity.keyWord = key

            # 网站
            networks = detail['networks']
            try:
                for item in networks:
                    network = networkDetail(item['network_id'])
                    # print(network)
                    type = network['type']
                    url = network['url']
                    if type == 'gzh':
                        entity.gzh = url
                    elif type == 'sdWindow':
                        entity.sdWindow = url
                    elif type == 'tieba':
                        entity.tieba = url
                    elif type == 'weibo':
                        entity.weibo = url
                    elif type == 'toutiao':
                        entity.toutiao = url
                    elif type == 'sinaNews':
                        entity.sinaNews = url
                    elif type == 'bjh':
                        entity.bjh = url
                    elif type == 'tianya':
                        entity.tianya = url
                    startSpider(type)

                    # print(network)
            except():
                print('-----------')
                continue

            # 开始下一个监控方案前休息1分钟
            # time.sleep(60)
    except():
        print('2222222')
    finally:
        print('123123131')


if __name__ == '__main__':
    prepareWork()