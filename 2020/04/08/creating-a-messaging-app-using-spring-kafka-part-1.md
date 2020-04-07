---
author: "Kursat Aydemir"
title: "Creating a Messaging App using Spring - Kafka (Part 1)"
tags: spring, kafka, message
---

![Spring-Kafka](/blog/2020/04/08/creating-a-messaging-app-using-spring-kafka-part-1/spring-kafka.png)

[Spring]: https://spring.io is a famous Java application framework.  [Kafka]: https://kafka.apache.org is a fault tolerant, fast and horizontally scalable distributed stream - message broker. [Spring for Kafka]: https://spring.io/projects/spring-kafka applies the overall concepts of Spring to Java applications based on Kafka.

Since Kafka can establish a fast and fault tolerant stream data pipeline it can be assumed as an orchestrator. Different kind of usages can be applied such stream brokers and you can find use cases in Kafka's home page. In this article I'd like to explain how to create project Spring-Kafka project, add the dependencies and Kafka use case of a messaging app.



## Initialize Spring Project

First of all, to create a Spring project from scratch can be simply done using the [Spring Initializr]: https://start.spring.io  page. There is a project initializer page introduces here. Most Spring projects use Maven and I keep the options as they are selected by default. I set the group id as `com.endpoint` and artifact as `SpringKafkaMessaging` which makes the base package name `com.endpoint.SpringKafkaMessaging`. 



![Spring Initializr](/blog/2020/04/08/creating-a-messaging-app-using-spring-kafka-part-1/springinitializr.png)



When we are good with the project initial setup by pressing the "GENERATE" button it will download a simple and empty Spring-Boot project in a zipped directory structure. You can then use your favorite IDE to open and start developing your project. My favorite IDE for Java projects is Eclipse and below is what I see when I open this project:



![Eclipse](/blog/2020/04/08/creating-a-messaging-app-using-spring-kafka-part-1/eclipse_springproject.png)

I'm not going to tell the details of configuring and adding dependencies of Spring and Maven projects. If you are not familiar with Spring and Maven, it would better to have a look at the Spring documentation first.



## Design and Architecture

Before adding the dependencies including Kafka, we need to make high level design of this simple project and know how to proceed with the development. The messaging apps seems simple in view but the architecture behind of them can be real complex. And there are different kind of technology stacks you can pick and move. At the very bottom determining the base protocol XMPP, SIP, WebSocket is subject to the aim of the app we are going to develop. Sometimes multiple protocols can be used and interconnected for providing more features. XMPP is mostly used for chatting, SIP is initially designed for VoIP and media transfer. We're going to use WebSocket to communicate with Kafka over TCP.

By giving the architectural model of Kafka, you'll have an understanding of how Kafka is going to maintain the most of the backend processes.

![Kafka Cluster](/blog/2020/04/08/creating-a-messaging-app-using-spring-kafka-part-1/kafka-apis.png)



Kafka, as in definition said, can be horizontally scalable, means Kafka clusters can be increased to be able to span several data sources. Basically message producers and message consumers (literally all client messaging apps are both producer and consumers) are producing and consuming the messages through Kafka topics.

So, taking the principals into account while designing the architecture of such a client-server based messaging app here the components and their communication directions would be:

* Kafka Cluster
* Spring-Boot REST API will handle user authentication and login
* Persistence (here I chose PostgreSQL)
* Cache (Redis) for fast read - write cache operations.
* WebSocket for messaging app clients



## Spring-Kafka Dependencies

After deciding the model and components lets add the dependencies in the `pom.xml` file and finish the first part. Below besides `spring-boot-starter` added `spring-boot-starter-web`, `spring-kafka`, `spring-boot-starter-jdbc` and `redis.clients:jedis` for the corresponding REST, Kafka, Persistent (JDBC) and Redis components.

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