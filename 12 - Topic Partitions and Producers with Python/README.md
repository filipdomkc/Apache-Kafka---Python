## Exploring Kafka Producer Internals using Python

In Kafka, the producer can control to which partition a record will be sent using either a specified partition or a key. The partition is the unit of parallelism in Kafka, and messages within a topic are distributed across partitions. The decision of which partition a message goes to can be influenced by the producer in the following ways:

**1. Specifying Partition**

When producing a message, the producer can explicitly specify the target partition to which the message should be sent. This is done by providing the partition number as an argument when creating a ProducerRecord.

    
```python
producer.produce('your_topic', partition=2, key='key', value='value')
```


In these examples, the message is directed to partition 2 of the specified topic.

**2. Using a Key**
If a key is specified when sending a message, Kafka uses the key to determine the target partition. The default partitioning strategy is to hash the key and assign the message to a partition based on the result. The hash-based approach ensures that messages with the same key always go to the same partition, maintaining order for messages with the same key.

```python
producer.produce('your_topic', key='key', value='value')
```

In these examples, Kafka will use the hash of the key to determine the partition.

**3. Default Partitioning Strategy**
If neither a partition nor a key is provided, Kafka uses a default partitioning strategy. The default strategy is to choose a partition in a round-robin fashion, distributing messages evenly across all partitions.

**4. Custom Partitioning Strategy**
For more advanced use cases, you can implement a custom partitioning strategy by implementing the org.apache.kafka.clients.producer.Partitioner interface in Java or the confluent_kafka.partitioner.Partitioner interface in Python. This allows you to define your logic for assigning messages to partitions.

Understanding and controlling how records are partitioned is essential for optimizing performance and ensuring that related messages end up in the same partition for processing in order.

## Examples 

Firstly we will start zookeper with:

    kafka_2.12-3.6.0\bin\windows\zookeeper-server-start.bat  kafka_2.12-3.6.0\config\zookeeper.properties

,then we'll start Kafka broker (server):

    kafka_2.12-3.6.0\bin\windows\kafka-server-start.bat kafka_2.12-3.6.0\config\server.properties 

We will also create 4 different topics and for each topic we will apply different partitioning strategy and inspect how each strategy reflects on storing data into different partitions.

    kafka_2.12-3.6.0/bin/windows/kafka-topics.bat --create --topic hello-world-1 --bootstrap-server localhost:9092--replication-factor 1 --partitions 3
    kafka_2.12-3.6.0/bin/windows/kafka-topics.bat --create --topic hello-world-2 --bootstrap-server localhost:9092--replication-factor 1 --partitions 3
    kafka_2.12-3.6.0/bin/windows/kafka-topics.bat --create --topic hello-world-3 --bootstrap-server localhost:9092--replication-factor 1 --partitions 3
    kafka_2.12-3.6.0/bin/windows/kafka-topics.bat --create --topic hello-world-4 --bootstrap-server localhost:9092--replication-factor 1 --partitions 3

Now you can open python console in terminal or you can run python script with code bellow as a producer:

**EXAMPLE 1**
```python

from time import sleep
from json import dumps
from kafka import KafkaProducer

#Lab 1: Write message to a partition

topic_name = "hello-world-1"
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer= lambda x: dumps(x).encode('utf-8'))

data1 = {'number' : 1}
data2 = {'number' : 2}
data3 = {'number' : 3}
data4 = {'number' : 4}
data5 = {'number' : 5}
data6 = {'number' : 6}

producer.send(topic_name, value=data1, partition=1)
producer.send(topic_name, value=data2, partition=1)
producer.send(topic_name, value=data3, partition=1)
producer.send(topic_name, value=data4, partition=2)
producer.send(topic_name, value=data5, partition=2)
producer.send(topic_name, value=data6, partition=0)
producer.close()

```

Start a consumer with:

    kafka_2.12-3.6.0/bin/windows/kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic hello-world-1 --from-beginning

Now go check into your Kafka server logs directory and check how data records are stored in partitions according to producer instructions.

**EXAMPLE 2**
```python

from time import sleep
from json import dumps
from kafka import KafkaProducer

#Lab 2: Pass key-value pair

topic_name = "hello-world-2"
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
producer.send(topic_name, key=b'foo', value=b'bar') #the 'b' character before a string is used to specify the string as a “byte string“ so that is why we dont need to specify value_serializer
producer.send(topic_name, key=b'foo', value=b'bar')
producer.close()

```
Now we have to inspect 3 partitions for this topic to find in which partition data records are stored (we dont know yet what is the outcome of the hashing algorithm), but we know that both records should be written on the same partition because they share identic key.

Start a consumer with:

    kafka_2.12-3.6.0/bin/windows/kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic hello-world-2 --from-beginning

**EXAMPLE 3**
```python

from time import sleep
from json import dumps
from kafka import KafkaProducer

#Lab 3: Pass key-value pair

topic_name = "hello-world-3"
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], key_serializer=str.encode, value_serializer= lambda x: dumps(x).encode('utf-8'))

data1 = {'number' : 1}
data2 = {'number' : 2}
data3 = {'number' : 3}
data4 = {'number' : 4}
data5 = {'number' : 5}
data6 = {'number' : 6}

producer.send(topic_name, key='ping', value=data1)
producer.send(topic_name, key='ping', value=data2)
producer.send(topic_name, key='ping', value=data3)
producer.send(topic_name, key='pong', value=data4)
producer.send(topic_name, key='pong', value=data5)
producer.send(topic_name, key='pong', value=data6)
producer.close()

```
We expect that all messages with 'ping' key go to the same partition as well as we expect all the messages that have 'pong' key to go to the same partition
Start a consumer with:

    kafka_2.12-3.6.0/bin/windows/kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic hello-world-3 --from-beginning


**EXAMPLE 4**
```python

from time import sleep
from json import dumps
from kafka import KafkaProducer

#Lab 4: Customize a partitioner

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

topic_name = "hello-world-4"
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], partitioner=custom_partitioner)

producer.send(topic_name, key=b'3', value=b'Hello Partitioner') # this message will go to the partition 0, we know because 3%3 = 0 (our custom partitioner)
producer.send(topic_name, key=b'2', value=b'Hello Partitioner 2') # this message will go to the partition 2, we know because 2%3 = 2 (our custom partitioner)
producer.send(topic_name, key=b'369', value=b'Hello Partitioner 3') # this message will go to the partition 0, we know because 369%3 = 2 (our custom partitioner)
producer.send(topic_name, key=b'301', value=b'Hello Partitioner 4') # this message will go to the partition 1, we know because 301%3 = 1 (our custom partitioner)
producer.close()

```
We can check if our partitioner works as expectet by inspecting our server logs directory for our topic 'hello-world-4'.
