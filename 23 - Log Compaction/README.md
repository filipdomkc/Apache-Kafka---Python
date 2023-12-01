# Log Compaction

**Log compaction** is a feature that helps to ensure that a compacted topic retains only the latest value for each key. This is particularly useful for scenarios where you want to maintain a compact representation of the state of a set of keys over time. It is commonly used in scenarios such as maintaining the latest state of a key-value store.

Here's a simple explanation of log compaction with an example:

**Log Compaction Overview**:
In Kafka, data is stored in topics, and each topic is divided into partitions. Each partition maintains an ordered sequence of records known as a log. Log compaction is a process in which Kafka ensures that for each key, only the latest record (based on the offset) is retained in the log.

**Example Scenario**:
Let's consider a scenario where we have a topic named "user-activity" with the following records:

Key: "user-1", Value: "login", Offset: 1
Key: "user-2", Value: "logout", Offset: 2
Key: "user-1", Value: "update-profile", Offset: 3
Key: "user-3", Value: "login", Offset: 4
After log compaction, the log would retain only the latest record for each key:

Key: "user-2", Value: "logout", Offset: 2
Key: "user-1", Value: "update-profile", Offset: 3
Key: "user-3", Value: "login", Offset: 4
In this example, only the latest records for each key are retained, and redundant records are removed during log compaction.

**Configuring Log Compaction:**
To enable log compaction for a topic, you need to set the cleanup.policy configuration to "compact" when creating the topic.

For example, using the Kafka command line tools:
```bin/kafka-topics.sh --create --topic user-activity --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1 --config cleanup.policy=compact
```

**Use Cases:**
Log compaction is beneficial in scenarios where you want to maintain the latest state of a set of keys, such as maintaining user profiles, configuration settings, or any use case where you are interested in only the most recent value for each key.

Keep in mind that log compaction is not suitable for all scenarios, and its effectiveness depends on the use case and data patterns.

## Code example