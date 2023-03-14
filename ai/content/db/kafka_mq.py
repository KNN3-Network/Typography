from kafka import KafkaProducer,KafkaConsumer
from kafka.errors import kafka_errors
import traceback
from content.configs.global_configs import KafkaConfigs as cfg
import json

urls = cfg.urls
def default_callback(data):
    print(data)

class Producer():

    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=urls,
            value_serializer=lambda v: json.dumps(v).encode(encoding='utf-8'),api_version=(0, 10, 2))

    def send(self,topic,data):
        self.producer.send(topic,value=data)  # 向分区1发送消息

        # try:
        #     result = future.get(timeout=10)  # 监控是否发送成功
        #     print(result.topic, result.partition, result.offset)
        # except kafka_errors:  # 发送失败抛出kafka_errors
        #     traceback.format_exc()

class Consumer():

    def __init__(self,topic):
        self.consumer = KafkaConsumer(topic,bootstrap_servers=urls,enable_auto_commit=True,api_version=(0, 10, 2))

    def listening(self,callback=default_callback):
        for msg in self.consumer:
            data = json.loads(msg.value.decode())
            callback(data)

