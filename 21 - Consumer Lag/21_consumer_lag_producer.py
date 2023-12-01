from time import sleep
from json import dumps
from kafka import KafkaProducer

def custom_partitioner(key, all_partitions, available):
    """
    Custom Kafka partitioner to get the partition corresponding to key
    :param key: partitioning key
    :param all_partitions: list of all partitions sorted by partition ID
    :param available: list of available partitions in no particular order
    :return: one of the values from all_partitions or available
    """
    print("The key is :{}".format(key))
    print("All partitions : {}".format(all_partitions))
    print("After decoding of the key : {}".format(key.decode('UTF-8')))
    return int(key.decode('UTF-8'))%len(all_partitions)

topic_name = "consumer_lag"
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer= lambda x: dumps(x).encode('UTF-8'), partitioner=custom_partitioner)

for e in range (1,1000):
    data = {'number': e}
    producer.send(topic_name,key=str(e).encode(),value=data)
    sleep(0.4)