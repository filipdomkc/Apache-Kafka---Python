Replication in a multi-broker Apache Kafka cluster is a crucial feature that ensures data durability, fault tolerance, and scalability. A multi-broker Kafka cluster consists of multiple Kafka broker nodes working together to provide fault tolerance, data redundancy, and scalability. This architecture ensures that Kafka can handle large volumes of data and continue to function even if some broker nodes fail. Replication is the process of duplicating data across multiple broker nodes within a Kafka cluster. It offers several benefits, including:

1. *__Data Durability__* : Replicated data is stored on multiple broker nodes, so even if one or more brokers fail, the data remains available.
2. *__Fault Tolerance__* : If a broker node goes down, the data can still be retrieved from the replicas on other broker nodes.
3. *__Scalability__* : Replication allows for the horizontal scaling of Kafka clusters. New broker nodes can be added to distribute the load and increase capacity.

The replication factor specifies how many copies (replicas) of each partition should be maintained across the cluster. A common replication factor is three, meaning each partition is replicated on three different broker nodes.
In a replicated Kafka topic, one of the replicas is designated as the "leader," and the others are "followers." The leader is responsible for handling read and write operations for the partition. If the leader fails, one of the followers is elected as the new leader. When a producer publishes a message to a Kafka topic, it is written to the leader replica. The leader then replicates the message to its followers. This ensures that data is distributed and available on multiple broker nodes. Consumers read data from any of the available replicas. Kafka clients are aware of the leader-follower model and can automatically switch to a new leader if the current leader fails, ensuring uninterrupted data access.

__EXAMPLE__ 

Start Kafka-server:
    
    kafka_2.12-3.6.0/bin/windows/kafka-server-start.bat
    kafka_2.12-3.6.0/config/server1.properties

    kafka_2.12-3.6.0/bin/windows/kafka-server-start.bat
    kafka_2.12-3.6.0/config/server2.properties

    kafka_2.12-3.6.0/bin/windows/kafka-server-start.bat
    kafka_2.12-3.6.0/config/server3.properties

Create a topic:

    
    kafka_2.12-3.6.0/bin/windows/kafka-topics.bat --create --topic demo-topic --bootstrap-server localhost:9092, localhost:9093, localhost:9094 --replication-factor 3 --partitions 7
    
Now run this command to see which server holds which partitions (and which of those partitions are leaders or replicas)
    
    kafka_2.12-3.6.0/bin/windows/kafka-topics.bat --bootstrap-server localhost:9092, localhost:9093, localhost:9094 --describe --topic demo-topic
    

You will see something like this:

    Topic: demo-topic       TopicId: O4Qk1DTsRKCdss-EMFezEw PartitionCount: 7       ReplicationFactor: 3    Configs:
    Topic: demo-topic       Partition: 0    Leader: 1       Replicas: 1,0,2 Isr: 1,0,2
    Topic: demo-topic       Partition: 1    Leader: 0       Replicas: 0,2,1 Isr: 0,2,1
    Topic: demo-topic       Partition: 2    Leader: 2       Replicas: 2,1,0 Isr: 2,1,0
    Topic: demo-topic       Partition: 3    Leader: 1       Replicas: 1,2,0 Isr: 1,2,0
    Topic: demo-topic       Partition: 4    Leader: 0       Replicas: 0,1,2 Isr: 0,1,2
    Topic: demo-topic       Partition: 5    Leader: 2       Replicas: 2,0,1 Isr: 2,0,1
    Topic: demo-topic       Partition: 6    Leader: 1       Replicas: 1,0,2 Isr: 1,0,2