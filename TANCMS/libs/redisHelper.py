import redis
import json
from kafka import KafkaConsumer

topic = 'tancms_iyanshan'
host = '127.0.0.1:9092'


def cacheSet(key, value):
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, decode_responses=True, charset='UTF-8', encoding='UTF-8')
    return r.set(key, value, 43200) # 保留0.5天

def cacheGet(key):
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, decode_responses=True, charset='UTF-8', encoding='UTF-8')
    return r.get(key)



def allDataConsumer():
    consumer = KafkaConsumer(topic, auto_offset_reset='earliest', bootstrap_servers=[host])
    count = 0
    for msg in consumer:
        item_dict = msg.value.decode('utf-8')
        print(item_dict)
        if len(item_dict) > 100:
            try:
                item = json.loads(item_dict)
                print(item)
                count += 1
                # indexData(item)
            except:
                pass
            finally:
                print(count)


if __name__ == '__main__':
    allDataConsumer()
    # print(cacheSet('test', '哈哈hell——123'))
    # print(cacheGet('test'))