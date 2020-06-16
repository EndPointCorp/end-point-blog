---
author: "Kürşat Kutlu Aydemir"
title: "Creating a Messaging App Using Spring for Apache Kafka, Part 3"
tags: java, spring, frameworks, kafka, spring-kafka-series
gh_issue_number: 1630
---

![Spring-Kafka](/blog/2020/05/21/messaging-app-spring-kafka-pt-three/spring-day.jpg)

[Photo](https://unsplash.com/photos/OKolJZ5jos4) by [Pascal Debrunner](https://unsplash.com/@debrupas) on [Unsplash](https://unsplash.com)

This article is part of a [series](/blog/tags/spring-kafka-series).

In this article we’ll create the persistence and cache models and repositories. We’re also going to create our PostgreSQL database and the basic schema that we’re going to map to the persistence model.

### Persistence

#### Database

We are going to keep the persistence model as simple as possible so we can focus on the overall functionality. Let’s first create our PostgreSQL database and schema. Here is the list of tables that we’re going to create:

- **users**: will hold the users who are registered to use this messaging service.
- **access_token**: will hold the unique authentication tokens per session. We’re not going to implement an authentication and authorization server specifically in this series but rather will generate a simple token and store it in this table.
- **contacts**: will hold relationships of existing users.
- **messages**: will hold messages sent to users.

Let’s create our tables:

```sql
CREATE TABLE kafkamessaging.users (
	user_id BIGSERIAL PRIMARY KEY,
	fname VARCHAR(32) NOT NULL,
	lname VARCHAR(32) NOT NULL,
	mobile VARCHAR(32) NOT NULL,
	created_at DATE NOT NULL
);

CREATE TABLE kafkamessaging.access_token (
	token_id BIGSERIAL PRIMARY KEY,	
	token VARCHAR(256) NOT NULL,
	user_id BIGINT NOT NULL REFERENCES kafkamessaging.users(user_id),
	created_at DATE NOT NULL
);

CREATE TABLE kafkamessaging.contacts (
	contact_id BIGSERIAL PRIMARY KEY,
	user_id BIGINT NOT NULL REFERENCES kafkamessaging.users(user_id),
	contact_user_id BIGINT NOT NULL REFERENCES kafkamessaging.users(user_id),
);

CREATE TABLE kafkamessaging.messages (
	message_id BIGSERIAL PRIMARY KEY,
	from_user_id BIGINT NOT NULL REFERENCES kafkamessaging.users(user_id),
	to_user_id BIGINT NOT NULL REFERENCES kafkamessaging.users(user_id),
	message VARCHAR(512) NOT NULL,
	sent_at DATE NOT NULL
);
```

### Model

Before creating the models we’ll add another dependency called [Lombok](https://projectlombok.org/) in `pom.xml` as shown below. Lombok provides very helpful annotations which automatically create getters, setters and many other parts of a class. 

```xml
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
    </dependency>
```

So here are the persistent model classes of the corresponding tables we created in the database. Notice the Lombok and javax.persistence annotations in the model classes:

#### User

```java
package com.endpoint.SpringKafkaMessaging.persistent.model;

import java.io.Serializable;
import java.util.Date;
import java.util.Set;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.OneToMany;
import javax.persistence.Table;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name="users")
public class User implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name="user_id")
    private Long userId;

    @Column
    private String fname;

    @Column
    private String lname;

    @Column
    private String mobile;
    
    @Column(name="created_at")
    private Date createdAt;
    
    @OneToMany(mappedBy = "User", fetch = FetchType.EAGER,
            cascade = CascadeType.ALL)
    private Set<Contact> contacts;

}
```

#### AccessToken

```java
package com.endpoint.SpringKafkaMessaging.persistent.model;

import java.io.Serializable;
import java.util.Date;
import java.util.Map;
import java.util.UUID;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name="access_token")
public class AccessToken implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long token_id;
    
    @Column(name="token")
    private String token;

    @Column(name="user_id")
    private Long userId;

    @Column(name="created_at")
    private Date createdAt;

}
```

#### Contact

```java
package com.endpoint.SpringKafkaMessaging.persistent.model;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name="contacts")
public class Contact implements Serializable {
	
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name="contact_id")
    private Long contactId;
    
    @Column(name="user_id")
    private Long userId;

    @Column(name="contact_user_id")
    private Long contactUserId;
    
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
}
```

#### Message

```java
package com.endpoint.SpringKafkaMessaging.persistent.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name="messages")
public class Message implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name="message_id")
    private String messageId;

    @Column(name="from_user_id")
    private Long fromUserId;

    @Column(name="to_user_id")
    private Long toUserId;

    @Column(name="message")
    private String message;
    
    @Column(name="sent_at")
    private Date sentAt;

}
```

Note also that we didn’t use underscores in the class field names for the corresponding table field names like `userId` for `user_id`.

We’re going to use Spring’s [CrudRepository](https://docs.spring.io/spring-data/commons/docs/current/api/org/springframework/data/repository/CrudRepository.html) interface to create our data repositories. CrudRepository can use keywords to automatically create logic using the given interface method names. Underscores are reserved characters, and even though you can still escape using double underscore in the CrudRepository method names, it doesn’t look good. I chose to use camel case, which also complies with Java convention.

### Repository

Now let’s add the corresponding persistent repositories for each data model:

#### UserRepository

```java
package com.endpoint.SpringKafkaMessaging.persistent.repository;

import java.util.List;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import com.endpoint.SpringKafkaMessaging.persistent.model.User;

@Repository
public interface UserRepository extends CrudRepository<User, Long> {

	List<User> findAll();

	User findByUserId(Long userId);
	
	User findByMobile(String mobile);
	
	User findByFname(String fname);
	
	User findByLname(String lname);

	void deleteById(Long userId);

}
```

#### ContactRepository

```java
package com.endpoint.SpringKafkaMessaging.persistent.repository;

import java.util.List;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import com.endpoint.SpringKafkaMessaging.persistent.model.Contact;

@Repository
public interface ContactRepository extends CrudRepository<Contact, Long> {

	List<Contact> findAllByUserId(Long userId);
	
	Contact findByContactUserId(Long contactUserId);

	void deleteByContactUserId(Long contactUserId);
}
```

#### AccessTokenRepository

```java
package com.endpoint.SpringKafkaMessaging.persistent.repository;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import com.endpoint.SpringKafkaMessaging.persistent.model.AccessToken;

@Repository
public interface AccessTokenRepository extends CrudRepository<AccessToken, Long> {

	AccessToken findByUserId(Long userId);

	void deleteByUserId(Long userId);

}
```

#### MessageRepository

```java
package com.endpoint.SpringKafkaMessaging.persistent.repository;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import com.endpoint.SpringKafkaMessaging.persistent.model.Message;
@Repository
public interface MessageRepository extends CrudRepository<Message, Long> {
	
}
```

### Cache

We’re not going to integrate the cache environment as Spring persistent data, so we won’t be using the CrudRepository implementation for the cache repository. Instead, let’s create the cache repository interface and create an implementation of it. Caching is going to be used for quick activation and authentication responses. To achieve this we’re going to store and query simple key-value pairs with Redis.

### Repository

#### CacheRepository

```java
package com.endpoint.SpringKafkaMessaging.cache.respository;

public interface CacheRepository {

    void putAccessToken(String token, String userId);
    
    String getUserIdByAccessToken(String token);

    void putActivationCode(String mobile, String activationCode);
    
    String queryMobileActivationCode(String mobile, String activationCode);
}
```

Since the business logic of this interface is not automatically created by Spring Boot, we need to create our own logic in Spring’s [@Service](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/stereotype/Service.html) like below.

#### CacheRepositoryImpl

```java
package com.endpoint.SpringKafkaMessaging.cache.respository;

import org.springframework.stereotype.Service;

import com.endpoint.SpringKafkaMessaging.cache.JedisFactory;

import redis.clients.jedis.Jedis;

@Service
public class CacheRepositoryImpl implements CacheRepository {

    @Override
    public void putAccessToken(String token, String userId) {

        try (Jedis jedis = JedisFactory.getConnection()) {

            jedis.set(token, userId);

        } catch (Exception e) {
        	e.printStackTrace();
        }
    }

    @Override
    public String getUserIdByAccessToken(String token) {

        try (Jedis jedis = JedisFactory.getConnection()) {

            return jedis.get(token);

        } catch (Exception e) {
        	e.printStackTrace();
        }

        return null;
    }

    @Override
    public void putActivationCode(String mobile, String activationCode) {

        try (Jedis jedis = JedisFactory.getConnection()) {

            jedis.hset(mobile, String.valueOf(activationCode), "");
            jedis.expire(mobile, 15 * 60);

        } catch (Exception e) {
        	e.printStackTrace();
        }
    }

    @Override
    public String queryMobileActivationCode(String mobile, String code) {

        try (Jedis jedis = JedisFactory.getConnection()) {

            return jedis.hget(mobile, code);
        } catch (Exception e) {
        	e.printStackTrace();
        }

        return null;
    }
}
```

### Activation and Authentication

Activation is a one-time process to activate a mobile number for our messaging service client. After an activation our simple authentication service will provide an access token to messaging client, and this access token will be used for future client logins. To achieve these simple processes let’s create our authentication service interface.

#### AuthService

```java
package com.endpoint.SpringKafkaMessaging.auth;

public interface AuthService {
    void putAccessToken(String code, Long userId);

    void loginWithAccessToken(String mobile, String code);
}
```

#### AuthServiceImpl

```java
package com.endpoint.SpringKafkaMessaging.auth;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.endpoint.SpringKafkaMessaging.cache.respository.CacheRepository;
import com.endpoint.SpringKafkaMessaging.persistent.model.AccessToken;
import com.endpoint.SpringKafkaMessaging.persistent.repository.AccessTokenRepository;

import java.util.Calendar;

@Service
public class AuthServiceImpl implements AuthService {

    @Autowired
    CacheRepository cacheRepository;

    @Autowired
    AccessTokenRepository accessTokenRepository;

    @Override
    public void putAccessToken(String token, Long userId) {

        // store token in the cache
        cacheRepository.putAccessToken(token, String.valueOf(userId));

        // store token in the persistence
        AccessToken accessToken = AccessToken.builder()
        							.token(token)
        							.userId(userId)
        							.createdAt(Calendar.getInstance().getTime())
        							.build();
        accessTokenRepository.save(accessToken);
    }

    @Override
    public void loginWithAccessToken(String mobile, String code) {
    	// TODO
    }
}
```

We won’t implement a complex auth server here.

Let’s look at the draft form of the authentication controller below. The authentication controller here simulates the mobile number activation and one time login with the activation code and provides a unique access token to client. To achieve this I defined activation request and response models.

#### ActivationRequest

```java
package com.endpoint.SpringKafkaMessaging.auth.controller;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Builder
@Data
@AllArgsConstructor
@NoArgsConstructor
public class ActivationRequest {
	
	private String mobile;
	
}
```

#### ActivationResponse

```java
package com.endpoint.SpringKafkaMessaging.auth.controller;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Builder
@Data
@AllArgsConstructor
@NoArgsConstructor
public class ActivationResponse {
	
	private String mobile;
	
	private String activationCode;
	
}
```

#### LoginRequest

```java
package com.endpoint.SpringKafkaMessaging.auth.controller;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Builder
@Data
@AllArgsConstructor
@NoArgsConstructor
public class LoginRequest {
	
	private String mobile;
	
	private String activationCode;
	
}
```

#### AuthController

```java
package com.endpoint.SpringKafkaMessaging.auth.controller;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import com.endpoint.SpringKafkaMessaging.auth.AuthService;
import com.endpoint.SpringKafkaMessaging.cache.respository.CacheRepository;
import com.endpoint.SpringKafkaMessaging.persistent.model.User;
import com.endpoint.SpringKafkaMessaging.persistent.repository.UserRepository;
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    UserRepository userRepository;

    @Autowired
    AuthService authService;

    @Autowired
    CacheRepository cacheRepository;
    
    @RequestMapping(value = "/getcode", method = RequestMethod.POST, consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
    public ResponseEntity<Object> getCode(@Valid @RequestBody ActivationRequest activationRequest) {
    	
    	// TODO
    	
    	return null;
    }
    
    @RequestMapping(value = "/login", method = RequestMethod.POST, consumes = MediaType.APPLICATION_JSON_UTF8_VALUE, produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
    public ResponseEntity<String> login(@RequestBody LoginRequest loginRequest) {
    	
    	// TODO
    	
    	return null;
    }
}
```

In the next chapter we’ll shape and complete the authentication service and controller and add message sender and receiver services. We’ll also configure and enable [Spring WebSocket](https://docs.spring.io/spring-framework/docs/5.0.0.BUILD-SNAPSHOT/spring-framework-reference/html/websocket.html).

In the final chapter, we’ll create a simple web app interface as a messaging client to test our spring-kafka messaging application.
