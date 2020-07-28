
import requests
from TANCMS.libs.ES import es_index, es_query
import random
import time
import urllib.request
import re
import json




def weibo():
    url = 'http://sinanews.sina.cn/interface/type_of_search.d.html?keyword=核酸检测&page=1&type=siftWb&size=40&newpage=0&chwm=&imei=&token=&did=&from=&oldchwm='
    res = requests.get(url).json()
    # print(res)
    data = res['data']['feed1']
    for item in data:
        print(item['url'])
        print(item['title'])





def es():
    title = '核酸检测成敛财神器？笑话'
    querys = {
        'match_phrase': {
            'title': title
        }
    }
    source = ['title']
    body = {
      "_source": "hits",
      "query": {
          "match_phrase": {
          "title": "核酸检测成敛财神器？笑话"
        }
      }
    }
    result = es_query('temp_document', body)
    if result['hits']['total']['value'] > 0:
        print(result['hits']['total']['value'])
    else:
        print('ooo')


def toutiao():
    # url = 'https://www.toutiao.com/a6789420137695937036/'
    # # 如何redis中已经存在爬过的url则自动跳过
    # response = urllib.request.urlopen(url)
    # print(response.read().decode('utf-8'))

    test = '''<!DOCTYPE html><html><head><meta charset=utf-8><meta http-equiv=x-dns-prefetch-control content=on><meta name=renderer content=webkit><link rel=dns-prefetch href=//s3.pstatp.com/ ><link rel=dns-prefetch href=//s3a.pstatp.com/ ><link rel=dns-prefetch href=//s3b.pstatp.com><link rel=dns-prefetch href=//p1.pstatp.com/ ><link rel=dns-prefetch href=//p3.pstatp.com/ ><meta http-equiv=Content-Type content="text/html; charset=utf-8"><meta http-equiv=X-UA-Compatible content="IE=edge,chrome=1"><meta name=viewport content="width=device-width,initial-scale=1,maximum-scale=1,minimum-scale=1,user-scalable=no,minimal-ui"><meta name=360-site-verification content=b96e1758dfc9156a410a4fb9520c5956><meta name=360_ssp_verify content=2ae4ad39552c45425bddb738efda3dbb><meta name=google-site-verification content=3PYTTW0s7IAfkReV8wAECfjIdKY-bQeSkVTyJNZpBKE><meta name=shenma-site-verification content=34c05607e2a9430ad4249ed48faaf7cb_1432711730><meta name=baidu_union_verify content=b88dd3920f970845bad8ad9f90d687f7><meta name=domain_verify content=pmrgi33nmfuw4ir2ej2g65lunfqw6ltdn5wselbcm52wszbchirdqyztge3tenrsgq3dknjume2tayrvmqytemlfmiydimddgu4gcnzcfqrhi2lnmvjwc5tfei5dcnbwhazdcobuhe2dqobrpu><link rel="shortcut icon" href=//sf3-dycdn-tos.pstatp.com/obj/eden-cn/uhbfnupkbps/toutiao_favicon.ico type=image/x-icon><!--[if lt IE 9]>
  <p>您的浏览器版本过低，请<a href="http://browsehappy.com/">升级浏览器</a></p>
<![endif]--><meta http-equiv=Content-Security-Policy content=upgrade-insecure-requests><link rel=alternate media="only screen and (max-width: 640px)" href=//m.toutiao.com/a6839663324880175628/ ><title>新冠病毒核酸与抗体检测知多少？检测结果如何解读？</title><meta name=keywords content=><meta name=description content=Ig M  和IgG，意味着近期感染了新冠病毒，并且感染新冠病毒的时间不长，应该在两周左右以内的急性期，这种情况需要结合核酸检测的结果，如果核酸结果为阳性确诊新冠病毒，需要采取相应的隔离和治疗措施，即使核酸检查结果为阴性，也不能麻痹大意，需要隔离，并且建议连续多次检测核酸。><script>(function (i, s, o, g, r, a, m) { i["SlardarMonitorObject"] = r; i[r] = i[r] || function () { (i[r].q = i[r].q || []).push(arguments) }, i[r].l = 1 * new Date; a = s.createElement(o), m = s.getElementsByTagName(o)[0]; a.async = 1; a.src = g; m.parentNode.insertBefore(a, m); i[r].globalPreCollectError = function () { i[r]('precollect', 'error', arguments); }; if (typeof i.addEventListener === 'function') { i.addEventListener('error', i[r].globalPreCollectError, true) } })(window, document, "script", "https://i.snssdk.com/slardar/sdk.js?bid=toutiao_pc", "Slardar");</script><script>window.Slardar && window.Slardar('config', {
      sampleRate: 1,
      bid: 'toutiao_pc',
      pid: 'article_detail_new',
      ignoreAjax: [/\/action_log\//],
      ignoreStatic: [/\.tanx\.com\//, /\.alicdn\.com\//, /\.mediav\.com/, /\.cnzz\.com/]
    });</script><script src=//unpkg.pstatp.com/byted/sec_sdk_build/2.0.2/dist/captcha.js></script><script src=//sf1-ttcdn-tos.pstatp.com/obj/rc-web-sdk/acrawler.js></script><script>window.byted_acrawler && window.byted_acrawler.init({
      aid: 24,
      dfp: true
    });</script><link rel=stylesheet href=//s3.pstatp.com/toutiao/static/css/page/index_node/index.32a0ae4c4c6bded7ac72e12f05cc56e6.css><script>!function(e){function t(a){if(c[a])return c[a].exports;var o=c[a]={exports:{},id:a,loaded:!1};return e[a].call(o.exports,o,o.exports,t),o.loaded=!0,o.exports}var a=window.webpackJsonp;window.webpackJsonp=function(r,n){for(var p,s,f=0,l=[];f<r.length;f++)s=r[f],o[s]&&l.push.apply(l,o[s]),o[s]=0;for(p in n)Object.prototype.hasOwnProperty.call(n,p)&&(e[p]=n[p]);for(a&&a(r,n);l.length;)l.shift().call(null,t);if(n[0])return c[0]=0,t(0)};var c={},o={0:0};t.e=function(e,a){if(0===o[e])return a.call(null,t);if(void 0!==o[e])o[e].push(a);else{o[e]=[a];var c=document.getElementsByTagName("head")[0],r=document.createElement("script");r.type="text/javascript",r.charset="utf-8",r.async=!0,r.src=t.p+"static/js/"+e+"."+{1:"2d3afb07f22d990072bf",2:"9fe9c5218f2f206b14e2",3:"62d3a605bc9f625457f2",4:"78b09cd367e70a5a5eb4",5:"c6eb2c57c2a06f60cde0"}[e]+".js",c.appendChild(r)}},t.m=e,t.c=c,t.p="/toutiao/",t.p="//s3.pstatp.com/toutiao/"}([]);</script></head><body><div id=app></div><script src=//s3.pstatp.com/inapp/lib/raven.js crossorigin=anonymous></script><script>;(function(window) {
    // sentry
    window.Raven && Raven.config('//key@m.toutiao.com/log/sentry/v2/96', {
      whitelistUrls: [/pstatp\.com/],
      sampleRate: 0.5,
      shouldSendCallback: function(data) {
        var ua = navigator && navigator.userAgent;
        var isDeviceOK = !/Mobile|Linux/i.test(navigator.userAgent);
        if (data.message && data.message.indexOf('p.tanx.com') !== -1) {
          return false;
        }
        return isDeviceOK;
      },
      tags: {
        bid: 'toutiao_pc',
        pid: 'article_detail_new'
      },
      autoBreadcrumbs: {
        'xhr': false,
        'console': true,
        'dom': true,
        'location': true
      }
    }).install();
  })(window);</script><script>var PAGE_SWITCH = {"adScriptQihu":false,"adScriptTB":false,"anti_spam":false,"migScriptUrl":"\u002F\u002Fs3a.pstatp.com\u002Ftoutiao\u002Fpicc_mig\u002Fdist\u002Fimg.min.js","nineteen":"","picVersion":"20180412_01","qihuAdShow":false,"taVersion":"20171221_1","ttAdShow":false};</script><script>var BASE_DATA = {
    userInfo: {
      id: 0,
      userName: '',
      avatarUrl: '',
      isPgc: false,
      isOwner: false
    },
    headerInfo: {
      id: 0,
      isPgc: false,
      userName: '',
      avatarUrl: '',
      isHomePage: false,
      chineseTag: '健康',
      crumbTag: 'ch/news_health/',
      hasBar: true
    },
    articleInfo: {
      title: '&quot;新冠病毒核酸与抗体检测知多少？检测结果如何解读？&quot;'.slice(6, -6),
      content: '123',
      groupId: '6839663324880175628',
      itemId: '6839663324880175628',
      type: 1,
      subInfo: {
        isOriginal: true,
        source: '好大夫在线',
        time: '2020-06-18 22:48:00'
      },
      tagInfo: {
        tags: [{"name":"IGG"},{"name":"肺炎"},{"name":"传染病"},{"name":"英雄联盟S8"}],
        groupId: '6839663324880175628',
        itemId: '6839663324880175628',
        repin: 0,
      },
      has_extern_link: 1,
      coverImg: 'http://p9.pstatp.com/list/300x196/pgc-image/bea0c151da8540c5b7b9de2067f4f15b.jpg'
    },
    commentInfo: {
      groupId: '6839663324880175628',
      itemId: '6839663324880175628',
      comments_count: 1,
      ban_comment: 0
    },
    mediaInfo: {
      uid: '4059683471',
      name: '好大夫在线',
      avatar: '//p1-dy.bytexservice.com/large/pgc-image/d3af28b68d7e401aa7b4ad8eceb3a7b5',
      openUrl: '/c/user/4059683471/',
      follow: false
    },
    pgcInfo: [{"item_id":"6852219612872835597","url":"\u002Fitem\u002F6852219612872835597","title":"身体出现这6个信号，酒精肝已“恶化”成“肝硬化”"},{"item_id":"6851909388110660100","url":"\u002Fitem\u002F6851909388110660100","title":"一人得病，全家传染！幽门螺旋杆菌到底该如何防？"},{"item_id":"6851908559802728974","url":"\u002Fitem\u002F6851908559802728974","title":"我国超一亿人群患有干眼症！经常熬夜刷手机，小心干眼症找上门"},{"item_id":"6850374972804694540","url":"\u002Fitem\u002F6850374972804694540","title":"宝宝多大开始刷牙？怎么给宝宝正确刷牙？"}],
    feedInfo: {
      url: '/toutiao/api/pc/feed/',
      category: '__all__',
      initList: []
    },
    shareInfo: {
      shareUrl: 'https://m.toutiao.com/group/6839663324880175628/',
      abstract: '&quot;Ig M  和IgG，意味着近期感染了新冠病毒，并且感染新冠病毒的时间不长，应该在两周左右以内的急性期，这种情况需要结合核酸检测的结果，如果核酸结果为阳性确诊新冠病毒，需要采取相应的隔离和治疗措施，即使核酸检查结果为阴性，也不能麻痹大意，需要隔离，并且建议连续多次检测核酸。&quot;'.slice(6, -6).replace(/<br \/>/ig, ''),
      commentCount: '1',
      ban_comment: 0
    }
  };</script><script>var imgUrl = '/c/hw5uxykusuj8xxvu48f2t56jzpcckmkp3p2rgbsxr8i9fvl/';</script><script></script><script type=text/javascript crossorigin=anonymous src=//s3a.pstatp.com/toutiao/static/js/vendor.78b09cd367e70a5a5eb4.js></script><script type=text/javascript crossorigin=anonymous src=//s3b.pstatp.com/toutiao/static/js/page/index_node/index.62d3a605bc9f625457f2.js></script><script type=text/javascript crossorigin=anonymous src=//s3.pstatp.com/toutiao/static/js/ttstatistics.c6eb2c57c2a06f60cde0.js></script><style>a[href*='//www.cnzz.com/stat'] {
      display: none!important;
  }</style><script>(function(win, export_obj) {
      win['TeaAnalyticsObject'] = export_obj;
      if (!win[export_obj]) {
          function _collect() {
              _collect.q.push(arguments);
          }
          _collect.q = _collect.q || [];
          win[export_obj] = _collect;
      }
      win[export_obj].l = +new Date();
  })(window, 'collectEvent');</script><script async src=https://s3.pstatp.com/pgc/tech/collect/collect-v.3.2.14.js></script><script>// Init tea log
  window.collectEvent('init', {
    app_id: 2256,
    channel: 'cn',
    log: false, // 开启调试日志
  });
  window.collectEvent('start');
  window.collectEvent('pageview', {
    'from': 'detail',
  });

  if (window.ttAnalysis) {
    ttAnalysis.setup({
      c: 'detail_article'
    });
    ttAnalysis.send('pageview', {});
  }</script><script>document.getElementsByTagName('body')[0].addEventListener('click', function(e) {
    var target = e.target,
        ga_event,
        ga_category,
        ga_label,
        ga_value;
    while(target && target.nodeName.toUpperCase() !== 'BODY') {
      ga_event = target.getAttribute('ga_event');
      ga_category = target.getAttribute('ga_category') || 'detail_article';
      ga_label = target.getAttribute('ga_label') || '';
      ga_value = target.getAttribute('ga_value') || 1;
      ga_event && window.ttAnalysis && ttAnalysis.send('event', { ev: ga_event });
      target = target.parentNode;
    }
});</script></body></html>'''

    articleInfo = re.findall('articleInfo: {(.*?)groupId', test, re.S)[0]

    print(articleInfo)


    content = re.findall('content:(.*?)groupId', test, re.S)[0]


    print(content)


if __name__ == '__main__':
    toutiao()


