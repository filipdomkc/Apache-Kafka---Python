## Kafka Broker

A Kafka broker is an individual Kafka server (node) that plays a crucial role in the Kafka ecosystem.Brokers are responsible for storing and managing the topic partitions, which are the basic units of data distribution and replication in Kafka.They receive and store incoming messages (events or records) from producers and serve these messages to consumers.Kafka brokers communicate with one another to replicate data for fault tolerance and to distribute the load among multiple servers.Each Kafka broker has a unique identifier and is part of a Kafka cluster.

## Kafka Cluster

A Kafka cluster is a group of Kafka brokers working together to provide a scalable and fault-tolerant environment for data streaming. A Kafka cluster consists of multiple Kafka brokers, and each broker is responsible for handling a portion of the data, which is organized into topic partitions. Kafka clusters are typically set up to have multiple brokers for redundancy and scalability. If one broker fails, the others can continue to serve data. Kafka clusters can be configured to replicate data across multiple brokers to ensure data durability and fault tolerance. Producers and consumers connect to any broker within the Kafka cluster. The cluster itself manages the distribution of data.

Kafka brokers can store multiple topics. Topics in Kafka are logical channels or categories that help organize and partition the data. Multiple topics can coexist on a single Kafka broker. Each topic is divided into partitions, and those partitions are distributed across the brokers in the Kafka cluster.

### Kafka Single Broker Cluster

To start a single Kafka broker cluster, you need to configure a server.properties file and then start the Kafka server. Here's an example using the terminal:
    
     # Create a properties file for the single broker (e.g., server.properties)
     echo "broker.id=0" > server.properties
     echo "listeners=PLAINTEXT://localhost:9092" >> server.properties
     echo "log.dirs=/tmp/kafka-logs" >> server.properties

     # Start the Kafka broker
     kafka-server-start server.properties
    

### Starting a Multi-Broker Cluster
To start a multi-broker Kafka cluster, you'll need to configure multiple server.properties files, each with a unique broker.id. Here's an example with three brokers:
    
    # Create properties files for the three brokers (e.g., server-0.properties, server-1.properties, server-2.properties)
    echo "broker.id=0" > server-0.properties
    echo "broker.id=1" > server-1.properties
    echo "broker.id=2" > server-2.properties
    echo "listeners=PLAINTEXT://localhost:9092" >> server-0.properties
    echo "listeners=PLAINTEXT://localhost:9093" >> server-1.properties
    echo "listeners=PLAINTEXT://localhost:9094" >> server-2.properties
    echo "log.dirs=/tmp/kafka-logs-0" >> server-0.properties
    echo "log.dirs=/tmp/kafka-logs-1" >> server-1.properties
    echo "log.dirs=/tmp/kafka-logs-2" >> server-2.properties

    # Start the Kafka brokers
    kafka-server-start server-0.properties
    kafka-server-start server-1.properties
    kafka-server-start server-2.properties
    

Partitions are the way Kafka distributes data across brokers. Each partition is replicated for fault tolerance. Kafka uses a partition assignment strategy to allocate partitions to brokers. The default strategy is a round-robin assignment. You can control the partition assignment by specifying a custom assignment strategy. If a broker crashes, Kafka's replication mechanism ensures data availability. Replicas of the failed broker's partitions are automatically promoted to leaders on other brokers. When the crashed broker is back online, it will replicate data from the leader. If a broker crashes, Kafka's replication mechanism ensures data availability. Replicas of the failed broker's partitions are automatically promoted to leaders on other brokers. When the crashed broker is back online, it will replicate data from the leader.
You can manage the configuration of each Kafka broker by modifying the server.properties file for each broker. Here's an example of server properties in a server-0.properties file:
    
    broker.id=0
    listeners=PLAINTEXT://localhost:9092
    log.dirs=/tmp/kafka-logs-0
    
