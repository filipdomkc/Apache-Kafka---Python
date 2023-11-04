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

        Topic: demo-topic       TopicId: wKCd_g5GRQ6__GwEl1V_6g PartitionCount: 7       ReplicationFactor: 3    Configs:
        Topic: demo-topic       Partition: 0    Leader: 1       Replicas: 1,2,0 Isr: 1,2,0
        Topic: demo-topic       Partition: 1    Leader: 0       Replicas: 0,1,2 Isr: 0,1,2
        Topic: demo-topic       Partition: 2    Leader: 2       Replicas: 2,0,1 Isr: 2,0,1
        Topic: demo-topic       Partition: 3    Leader: 1       Replicas: 1,0,2 Isr: 1,0,2
        Topic: demo-topic       Partition: 4    Leader: 0       Replicas: 0,2,1 Isr: 0,2,1
        Topic: demo-topic       Partition: 5    Leader: 2       Replicas: 2,1,0 Isr: 2,1,0
        Topic: demo-topic       Partition: 6    Leader: 1       Replicas: 1,2,0 Isr: 1,2,0

This output table provides information about the topic's configuration, partitioning, and the brokers involved. Here's a breakdown of the information in the table:

__1.Topic Information__
 - Topic Name: demo-topic
 - TopicId: This appears to be an internal unique identifier for the topic.
 - Partition Count: There are 7 partitions for this topic.
 - Replication Factor: The replication factor is 3, which means there are three replicas of each partition.

 __2. Partition Details__
 - For each partition (0 to 6), the following information is provided:
    - Partition Number: The partition number within the topic.
    - Leader: The broker ID that is currently the leader for that partition.
    - Replicas: The list of broker IDs that serve as replicas for this partition. Replicas are responsible for storing copies of the data.
    - Isr (In-Sync Replicas): The list of broker IDs that are currently in sync for this partition. In-sync replicas are replicas that are up-to-date with the leader.

Now start producer with:
    
    /kafka_2.12-3.6.0/bin/windows/kafka-console-producer.bat --bootstrap-server localhost:9092, localhost:9093, localhost:9094 --topic demo-topic

and start consumer with:

    /kafka_2.12-3.6.0/bin/windows/kafka-console-consumer.bat --bootstrap-server localhost:9092, localhost:9093, localhost:9094 --from-beginning --topic demo-topic

and start producing some messages to the console, and consumer will get those messages.

Example:

    >hi
    >this is 2nd massage
    >3rd letter
    >4th
    >monday
    >fridaj
    >saturday
    >sunday
    >9th message
    >10th message
    >11th message
    >12th message

From previous table we can see that leader for partition 0 (1st partition) is broker with id 1, so we can go to server1_logs in our *kafka_logs* folder and find which messages got stored in broker 1.

Now what we will do is we will terminate our consumer process by pressing ctrl + c. Next we will stop broker 1 (*server1*). Now start consumer again and you will see that we can still see all the messages (even though one server is down). This is because of replications. If we didnt have replication , we could not see messages stored in server which crushed.

Here is how our describe table looks now:

     D:/kafka_2.12-3.6.0/bin/windows/kafka-topics.bat --bootstrap-server localhost:9092, localhost:9093, localhost:9094 --describe --topic demo-topic
    Topic: demo-topic       TopicId: wKCd_g5GRQ6__GwEl1V_6g PartitionCount: 7       ReplicationFactor: 3    Configs:
            Topic: demo-topic       Partition: 0    Leader: 2       Replicas: 1,2,0 Isr: 2,0
            Topic: demo-topic       Partition: 1    Leader: 0       Replicas: 0,1,2 Isr: 0,2
            Topic: demo-topic       Partition: 2    Leader: 2       Replicas: 2,0,1 Isr: 2,0
            Topic: demo-topic       Partition: 3    Leader: 0       Replicas: 1,0,2 Isr: 0,2
            Topic: demo-topic       Partition: 4    Leader: 0       Replicas: 0,2,1 Isr: 0,2
            Topic: demo-topic       Partition: 5    Leader: 2       Replicas: 2,1,0 Isr: 2,0
            Topic: demo-topic       Partition: 6    Leader: 2       Replicas: 1,2,0 Isr: 2,0

We can see that, where our broker with id 1 earlier was the leader, now some other broker is the new leader. E.g. for Partition 0 broker with id 1 was leader, but now the leader is broker with id 2. Similarly, for Parrtition 3, broker with id 1 was leader, but new leader is proker with id 0.
Also, we can notice that Isr (In Sync Replicas) are now stored only on server with ids 0 and 2 respectively ( servers which are still running)

We will now terminate server with id 0 and our describe table look like:

    Topic: demo-topic       TopicId: wKCd_g5GRQ6__GwEl1V_6g PartitionCount: 7       ReplicationFactor: 3    Configs:
        Topic: demo-topic       Partition: 0    Leader: 2       Replicas: 1,2,0 Isr: 2
        Topic: demo-topic       Partition: 1    Leader: 2       Replicas: 0,1,2 Isr: 2
        Topic: demo-topic       Partition: 2    Leader: 2       Replicas: 2,0,1 Isr: 2
        Topic: demo-topic       Partition: 3    Leader: 2       Replicas: 1,0,2 Isr: 2
        Topic: demo-topic       Partition: 4    Leader: 2       Replicas: 0,2,1 Isr: 2
        Topic: demo-topic       Partition: 5    Leader: 2       Replicas: 2,1,0 Isr: 2
        Topic: demo-topic       Partition: 6    Leader: 2       Replicas: 1,2,0 Isr: 2

Now, we will start servers that we crushed and after some time our describe table will firstly look like:

    Topic: demo-topic       TopicId: wKCd_g5GRQ6__GwEl1V_6g PartitionCount: 7       ReplicationFactor: 3    Configs:
        Topic: demo-topic       Partition: 0    Leader: 2       Replicas: 1,2,0 Isr: 2,0,1
        Topic: demo-topic       Partition: 1    Leader: 2       Replicas: 0,1,2 Isr: 2,0,1
        Topic: demo-topic       Partition: 2    Leader: 2       Replicas: 2,0,1 Isr: 2,0,1
        Topic: demo-topic       Partition: 3    Leader: 2       Replicas: 1,0,2 Isr: 2,0,1
        Topic: demo-topic       Partition: 4    Leader: 2       Replicas: 0,2,1 Isr: 2,0,1
        Topic: demo-topic       Partition: 5    Leader: 2       Replicas: 2,1,0 Isr: 2,0,1
        Topic: demo-topic       Partition: 6    Leader: 2       Replicas: 1,2,0 Isr: 2,0,1

where we can see that servers are up again (Isr) and leader are still server3 (with id2), but shortly after load is again evenly distributed :

    Topic: demo-topic       TopicId: wKCd_g5GRQ6__GwEl1V_6g PartitionCount: 7       ReplicationFactor: 3    Configs:
        Topic: demo-topic       Partition: 0    Leader: 1       Replicas: 1,2,0 Isr: 2,0,1
        Topic: demo-topic       Partition: 1    Leader: 0       Replicas: 0,1,2 Isr: 2,0,1
        Topic: demo-topic       Partition: 2    Leader: 2       Replicas: 2,0,1 Isr: 2,0,1
        Topic: demo-topic       Partition: 3    Leader: 1       Replicas: 1,0,2 Isr: 2,0,1
        Topic: demo-topic       Partition: 4    Leader: 0       Replicas: 0,2,1 Isr: 2,0,1
        Topic: demo-topic       Partition: 5    Leader: 2       Replicas: 2,1,0 Isr: 2,0,1
        Topic: demo-topic       Partition: 6    Leader: 1       Replicas: 1,2,0 Isr: 2,0,1