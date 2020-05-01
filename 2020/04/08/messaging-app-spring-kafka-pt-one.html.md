---
author: "Kürşat Kutlu Aydemir"
title: "Creating a Messaging App Using Spring for Apache Kafka, Part 1"
tags: spring, java, frameworks, kafka, spring-kafka-series
gh_issue_number: 1619
---

![spring-kafka](/blog/2020/04/08/messaging-app-spring-kafka-pt-one/banner.jpg)
[Photo](https://unsplash.com/photos/7J90Bxj-vtI) by [Click and Learn Photography](https://unsplash.com/@clickandlearnphotography) at [Unsplash](https://unsplash.com/)

This article is part of a [series](/blog/tags/spring-kafka-series).

[Spring](https://spring.io) is a popular Java application framework. [Apache Kafka](https://kafka.apache.org) is a fault-tolerant, fast, and horizontally scalable distributed stream-message broker. [Spring for Apache Kafka](https://spring.io/projects/spring-kafka) applies the overall concepts of Spring to Java applications based on Kafka.

Since Kafka can establish a fast and fault-tolerant stream data pipeline it can be used as an orchestrator. In this article I’ll explain how to create a spring-kafka project, add dependencies and use Kafka to create a messaging app.

### Initialize Spring project

Spring projects can be built from scratch using [Spring Initializr](https://start.spring.io). I like to keep the default options. Most Spring projects use [Maven](https://maven.apache.org/). I set the group id as `com.endpoint` and the artifact as `SpringKafkaMessaging` which makes the base package name `com.endpoint.SpringKafkaMessaging`.

![Spring Initializr](/blog/2020/04/08/messaging-app-spring-kafka-pt-one/springinitializr.png)

When we are done with the initial project setup we press the “GENERATE” button to download an empty Spring Boot project in a zip file. You can then use your favorite IDE to open and start developing your project. I prefer [Eclipse](https://www.eclipse.org/) for Java projects. Here’s what it looks like when I open the project up:

![Eclipse](/blog/2020/04/08/messaging-app-spring-kafka-pt-one/eclipse_springproject.png)

I won’t address detailed configuration or adding dependencies of Spring and Maven projects in this post. If you are not familiar with Spring and Maven, I recommend that you have a look at the [Spring documentation](https://docs.spring.io/spring/docs/current/spring-framework-reference/) first.

### Design and architecture

Before adding the dependencies, including Kafka, we need to make a high-level design of this simple project and figure out how to proceed with development. Messaging apps seem simple at first glance but the architecture behind them can be quite complex.

There are different kinds of technology stacks you can choose from. Which base protocol we choose (XMPP, SIP, or WebSocket) depends on what our app’s aim is. Sometimes multiple protocols can be used and interconnected to provide more features; XMPP is mostly used for chatting, SIP is designed for VoIP and media transfer. We’ll use WebSocket to communicate with Kafka over TCP.

By understanding the architectural model of Kafka, you’ll get an understanding of how Kafka is going to maintain most of the backend processes.

Kafka, as I mentioned previously, is horizontally scalable, and Kafka clusters can grow to span several data sources. Message producers and message consumers (all client messaging apps are both producers and consumers) produce and consume messages through Kafka topics.

So, taking into account the principles for designing the architecture of such a client–server-based messaging app, here are the components and their communication directions:

* Kafka Cluster
* Spring Boot REST API, which will handle user authentication and login
* Persistence (here I chose PostgreSQL)
* Cache (Redis) for fast read-write cache operations
* WebSocket for messaging app clients

### spring-kafka dependencies

After creating a model and components let’s add our dependencies to the `pom.xml` file to finish creating our project. Below we add `spring-boot-starter`, `spring-boot-starter-web`, `spring-kafka`, `spring-boot-starter-jdbc`, and `redis.clients:jedis` for the corresponding REST, Kafka, Persistent (JDBC), and Redis components.

```xml
<dependencies>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter</artifactId>
  </dependency>

  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
  </dependency>

  <dependency>
    <groupId>org.springframework.kafka</groupId>
    <artifactId>spring-kafka</artifactId>
  </dependency>

  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jdbc</artifactId>
  </dependency>

  <dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
  </dependency>

  <dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
  </dependency>

  <dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
  </dependency>

  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
    <exclusions>
      <exclusion>
        <groupId>org.junit.vintage</groupId>
        <artifactId>junit-vintage-engine</artifactId>
      </exclusion>
    </exclusions>
  </dependency>

  <dependency>
      <groupId>org.springframework.kafka</groupId>
      <artifactId>spring-kafka-test</artifactId>
      <scope>test</scope>
  </dependency>
</dependencies>
```

Continued in [Part 2](/blog/2020/04/29/messaging-app-spring-kafka-pt-two)!
