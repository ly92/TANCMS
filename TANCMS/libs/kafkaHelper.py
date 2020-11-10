from kafka import KafkaConsumer, KafkaProducer
from TANCMS.libs.redisHelper import cacheGet
import json
import time
from TANCMS.libs.timeHelper import formatTime
from TANCMS.libs.ES import es_multi_index

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
        program_id = cacheGet('program_id')
        program_title = cacheGet('program_title')
        item = json.loads(item_dict)
        if item['type_name'] == 'BlogItem':
            actions.append({
                "_op_type": "index",
                "_index": "temp_blog",
                "_source": {
                    "blog_comments_relation": {
                        "name": "blog"
                    },
                    "author": item['author'],
                    "author_url": item['author_url'],
                    "author_id": item['author_id'],
                    "blog_id": item['blog_id'],
                    "content": item['content'],
                    "bar": item['bar'],
                    "bar_url": item['bar_url'],
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
                    "creationTime": item['time'],
                    "addTime": formatTime(time.time())
                }
            })
        elif item['type_name'] == 'ArticleItem':
            actions.append({
                "_op_type": "index",
                "_index": "temp_document",
                "_source": {
                    "author": item['author'],
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
                    "creationTime": item['time'],
                    "addTime": formatTime(time.time())
                }
            })
        elif item['type_name'] == 'CommentItem':
            pass

        if len(actions) == 100:
            es_multi_index(actions)
            actions = []

if __name__ == '__main__':
    # productMessage()
    consumerMessage()
