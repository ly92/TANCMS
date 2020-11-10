
## 更新

- 第一次请求详情页面时，生成 `__ac_signature`，之后的请求共用该值；
- `__ac_signature` 的时效性为 30 分钟，30分钟后需要重新生成一次。


## 介绍

爬取今日头条新闻详情页内容，Nodejs 本地动态生成 Cookies 中 key 为 `__ac_signature` 的值



## 目录结构

- sign.js（生成 `__ac_signature` 文件）
- web_server.js（web_server 文件）
- ../../spiders/toutiao.py（爬虫文件）



## __ac_signature 生成需要的参数

```
__ac_nonce	# 第一次请求新闻详情页时，response cookies中获取
url			# 当前新闻详情页 url
userAgent	# 请求头
```



## 环境依赖库

### Python

- requests


### NodeJS

- express



## 使用说明

1.  使用 `Nodejs` 运行 `web_server.js`，启动 `web`服务；

    `node TANCMS/libs/toutiao/web_server.js`
2.  执行 `toubiao.py`开始爬取。




