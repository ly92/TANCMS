from kafka import KafkaConsumer, KafkaProducer
from TANCMS.libs.redisHelper import cacheGet
import json
import time
from TANCMS.libs.timeHelper import formatTime
from TANCMS.libs.ES import es_multi_index
from TANCMS.libs.async_call import async_call


topic = 'tancms_iyanshan'
host = '127.0.0.1:9092'


def productMessage(msg):
    producer = KafkaProducer(bootstrap_servers=host)
    msg = msg.encode('utf-8')
    producer.send(topic, msg)
    producer.close()


def consumerMessage():
    consumer = KafkaConsumer(topic, bootstrap_servers=[host])
    actions = []
    for msg in consumer:
        item_dict = msg.value.decode('utf-8')

        item = json.loads(item_dict)
        if len(item_dict) > 100:
            try:
                item = json.loads(item_dict)
                # print(item)
                indexData(item)
            except:
                pass
            finally:
                pass


actions = []
def indexData(item):
    program_id = cacheGet('program_id')
    if not program_id:
        return
    program_title = cacheGet('program_title')
    if not program_title:
        return

    if item['type_name'] == 'BlogItem':
        obj = {
            "_op_type": "index",
            "_index": "temp_blog",
            "_source": {
                "blog_comments_relation": {
                    "name": "blog"
                },
                "author": item['author'],
                "author_url": item['author_url'],
                "author_id": item.get('author_id', ''),
                "blog_id": item['blog_id'],
                "content": item['content'],
                "bar": item.get('bar', ''),
                "bar_url": item.get('bar_url', ''),
                "programs": [
                    {
                        "programId": program_id,
                        "programTitle": program_title
                    }
                ],
                "htmlContent": item.get('htmlContent', ''),
                "source": item['source'],
                "title": item['title'],
                "url": item['url'],
                # "creationTime": item['time'],
                "creationTime": '2020-11-11T10:39:46.316+0800',
                "addTime": formatTime(time.time())
            }
        }
        actions.append(obj)
    elif item['type_name'] == 'ArticleItem':
        obj = {
            "_op_type": "index",
            "_index": "temp_document",
            "_source": {
                "author": item['author'],
                "author_url": item['author_url'],
                "content": item['content'],
                "programs": [
                    {
                        "programId": program_id,
                        "programTitle": program_title
                    }
                ],
                "htmlContent": item['htmlContent'],
                "source": item['source'],
                "title": item['title'],
                "url": item['url'],
                # "creationTime": item['time'],
                "creationTime": '2020-11-11T10:39:46.316+0800',
                "addTime": formatTime(time.time())
            }
        }
        actions.append(obj)
    elif item['type_name'] == 'CommentItem':
        pass

    if len(actions) == 10:
        result = es_multi_index(actions)
        print(result)
        actions.clear()
    else:
        print(len(actions))




def allDataConsumer():
    consumer = KafkaConsumer(topic, auto_offset_reset='earliest', bootstrap_servers=[host])
    for msg in consumer:
        item_dict = msg.value.decode('utf-8')
        print(item_dict)
        if len(item_dict) > 100:
            try:
                item = json.loads(item_dict)
                # print(item)
                # indexData(item)
            except:
                pass
            finally:
                pass



if __name__ == '__main__':
    # productMessage()
    consumerMessage()
    # allDataConsumer()
    # indexData('23')
