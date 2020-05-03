---
author: "Kürşat Kutlu Aydemir"
title: "Creating a Messaging App Using Spring for Apache Kafka, Part 2"
tags: java, spring, frameworks, kafka, spring-kafka-series
gh_issue_number: 1624
---

![Spring pasture](/blog/2020/04/29/messaging-app-spring-kafka-pt-two/spring-pasture.jpg)

This article is part of a [series](/blog/tags/spring-kafka-series).

In this part I’ll walk through Kafka’s servers and processes, the basics of spring-kafka producers and consumers, persistence, and caching configurations.

### Kafka Servers

Kafka uses [Apache ZooKeeper](https://zookeeper.apache.org/) as the distributed coordination server. You can download the Apache Kafka with ZooKeeper bundle [here](https://kafka.apache.org/downloads).

When you download and untar the Kafka bundle Kafka’s console scripts can be found in the `bin` directory. To enable Kafka connectivity and prepare the Kafka configuration let’s start the Kafka servers and see how to create Kafka topics and test console producers and consumers.

#### ZooKeeper

To start ZooKeeper with the default properties run the following command:

```shell
bin/zookeeper-server-start.sh config/zookeeper.properties
```

#### Kafka Server

A single Kafka server with the default properties can be started with following command:

```shell
bin/kafka-server-start.sh config/server.properties
```

### Kafka Topics

#### Creating Kafka Topics

Let’s create a test Kafka topic:

```shell
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic myTestTopic
```

#### List Topics

To list all previously created Kafka topics:

```shell
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

#### Start a Producer

To start a console producer run the following command and send some messages from console:

```shell
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic myTestTopic
> This is a message
> This is another message
```

#### Start a Consumer

```shell
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic myTestTopic --from-beginning
```

When you run the consumer on the console with the from-beginning parameter you’ll see all the messages sent previously shown in the console.

Here we ran Kafka as a single server. You’ll need to optimize and scale the Kafka clusters for production and large-scale distributed systems. So far, we’ve become familiar with some Kafka components but for further Kafka configuration you can refer to the corresponding tutorials.

### spring-kafka Configuration

#### Consumer Configuration

In the Spring Boot project let’s put the lines below in the `application.properties` to configure the Spring Kafka consumer:

```properties
#Consumer
spring.kafka.consumer.bootstrap-servers=localhost:9092
spring.kafka.consumer.group-id=foo
spring.kafka.consumer.auto-offset-reset=earliest
spring.kafka.consumer.key-deserializer=org.apache.kafka.common.serialization.StringDeserializer
spring.kafka.consumer.value-deserializer=org.apache.kafka.common.serialization.StringDeserializer
```

A simple Kafka consumer is defined as a Spring `@KafkaListener` annotated method like this:

```java
@Configuration
public class MyKafkaConsumer {

    @KafkaListener(topics = "myTestTopic")
    public void listenTopic(ConsumerRecord<String, String> kafkaMessage) {
        System.out.print(String.format("Received a message: %s", kafkaMessage.value()));
    }

}
```

We are going to define different Kafka consumer methods listening to different topics for different purposes in our messaging app.

#### Producer Configuration

For producer configuration let’s add the following lines in the `application.properties` in our Spring Kafka project.

```properties
#Producer
spring.kafka.producer.bootstrap-servers=localhost:9092
spring.kafka.producer.key-serializer=org.apache.kafka.common.serialization.StringSerializer
spring.kafka.producer.value-serializer=org.apache.kafka.common.serialization.StringSerializer
```

A very simple Kafka producer could be configured like below. Spring `KafkaTemplate` provides a producer model and methods for sending messages to specified Kafka topics.

```java
@Configuration
public class MyKafkaProducer {

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    public void sendMessage(String topic, String message) {
        System.out.println(String.format("Message is being sent to topic %s", topic));
        kafkaTemplate.send(topic, message);
    }

}
```

So far we have configured Kafka in a Spring Boot project and seen simple consumer and producer examples. Before going further with Kafka configuration, let’s configure the persistence and cache repositories.

### Persistence Configuration

As I mentioned in the [first part](/blog/2020/04/08/messaging-app-spring-kafka-pt-one) of this blog series, I’m going to use [PostgreSQL](https://www.postgresql.org/) as a persistence environment and Spring data configuration will be like below in the `application.properties`:

```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/epmessagingdb
spring.datasource.username=epmessaging
spring.datasource.password=epmessagingdb_password
spring.datasource.driver-class-name=org.postgresql.Driver
spring.datasource.configuration.maximum-pool-size=30
spring.jpa.database-platform=PostgreSQL
# The SQL dialect makes Hibernate generate better SQL for the chosen database
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
# Hibernate ddl auto (create, create-drop, validate, update)
spring.jpa.hibernate.ddl-auto=none
```

In the properties we set the `spring.jpa.hibernate.ddl-auto` [Spring JPA](https://spring.io/projects/spring-data-jpa) property to `none` to avoid [Hibernate](https://hibernate.org/) populating the schema automatically. In some cases it can be useful to allow auto-population. We leave the base configuration here for now as it is, in the next part we’ll create our Spring Data models in the project.

### Caching Configuration

I also mentioned that we’re going to use [Redis](https://redis.io/) as the cache environment. Redis is developed using [C](https://en.wikipedia.org/wiki/C_(programming_language)) and a very fast in-memory cache.

Let’s put the following lines in `application.properties` to enable Redis configuration in our Spring Kafka project.

```properties
cache.redis.host=localhost
cache.redis.port=6379
cache.redis.timeout=5000
cache.redis.password=
```

#### Redis Pooling Factory

We’re going to use [Jedis](https://github.com/xetorthio/jedis) as the Redis client in our project. So let’s create a Jedis pooling factory class in our project called `JedisFactory` like below:

```java
package com.endpoint.SpringKafkaMessaging.cache;

import org.springframework.beans.factory.annotation.Value;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

public class JedisFactory {

    @Value("${cache.redis.host}")
    private static String host;

    @Value("${cache.redis.port}")
    private static Integer port;

    @Value("${cache.redis.timeout}")
    private static Integer timeout;

    @Value("${cache.redis.password}")
    private static String password;

    // hide the constructor
    private JedisFactory() {

    }

    private static JedisPool jedisPool;

    static {
        JedisPoolConfig poolConfig = new JedisPoolConfig();
        poolConfig.setMaxTotal(128);

        jedisPool = new JedisPool(
            poolConfig,
            host,
            port,
            timeout,
            password
        );
    }

    public static Jedis getConnection() {
        return jedisPool.getResource();
    }
}
```

We’ll create a persistence model, repository, controllers, and a cache repository in the next part of this blog series.
