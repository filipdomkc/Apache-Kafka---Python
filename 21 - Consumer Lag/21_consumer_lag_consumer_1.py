from kafka import KafkaConsumer
from kafka import TopicPartition , OffsetAndMetadata
from time import sleep


import json


consumer = KafkaConsumer ('consumer_lag',bootstrap_servers = ['localhost:9092'],
value_deserializer=lambda m: json.loads(m.decode('utf-8')),group_id='my-group',auto_offset_reset='earliest', enable_auto_commit =False)


for message in consumer:
    print(message)
    tp = TopicPartition(message.topic, message.partition)
    om = OffsetAndMetadata(message.offset + 1, message.timestamp)
    consumer.commit({tp: om})
    sleep(0.8) 