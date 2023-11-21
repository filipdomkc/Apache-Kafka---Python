from kafka import KafkaConsumer
import json

topic_name = 'offset_commit'

consumer = KafkaConsumer (topic_name, bootstrap_servers=['localhost:9092'], value_deserializer=lambda m: json.loads(m.decode('utf-8')),group_id='group_1', auto_offset_reset='latest')

for message in consumer:
    print(message)