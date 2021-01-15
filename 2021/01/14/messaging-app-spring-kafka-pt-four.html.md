---
author: "Kürşat Kutlu Aydemir"
title: "Creating a Messaging App Using Spring for Apache Kafka, Part 4"
tags: java, spring, kafka, spring-kafka-series
gh_issue_number: 1710
---

![Spring-Kafka](/blog/2021/01/14/messaging-app-spring-kafka-pt-four/banner.jpg)
Photo by [Daniel Tran](https://unsplash.com/@dtmtran) on [Unsplash](https://unsplash.com/photos/FPE6bG8JWRE)

This article is part of a [series](/blog/tags/spring-kafka-series). The GitHub repository with code examples can be found [here](https://github.com/ashemez/SpringKafkaMessaging).

After a long break from this series let’s keep moving further.

Let’s configure and prepare the WebSocket session pool. As we go through some custom operations like authentication and storing messages on the time of socket messages and sessions received, we need to create a WebSocketHandler for WebSocket configuration. When a WebSocket session message is received we’re going to send the message to a Kafka topic. In order to achieve this we need to define our WebSocket message handler `MessageHandler` and Kafka message producer `MessageSender`. We also need a session pool `WebSocketPool` so we can manage the client sessions.

### WebSocketPool

```java
package com.endpoint.SpringKafkaMessaging.websocket;

import org.springframework.web.socket.WebSocketSession;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class WebSocketPool {

  public static Map<Long, Set<WebSocketSession>> websockets = new HashMap<>();

}

```

`WebSocketPool` holds client sessions in a map of `<user_id, <set of WebSocketSession>`. This map allows multiple sessions for one user, ensuring it will work from multiple client applications.

### MessageHandler

```java
package com.endpoint.SpringKafkaMessaging.websocket;

import org.springframework.web.socket.WebSocketSession;

import java.io.IOException;

public interface MessageHandler {

  public void addSessionToPool(Long userId, WebSocketSession session);

  public void sendMessageToUser(Long userId, String message) throws IOException;

  void removeFromSessionToPool(Long userId, WebSocketSession session);
}

```

### MessageHandlerImpl

```java
package com.endpoint.SpringKafkaMessaging.websocket;

import org.springframework.stereotype.Service;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;

import java.io.IOException;
import java.util.HashSet;
import java.util.Set;

@Service
public class MessageHandlerImpl implements MessageHandler {

  @Override
  public void addSessionToPool(Long userId, WebSocketSession session) {

    Set<WebSocketSession> userSessions = WebSocketPool.websockets.get(userId);

    if (userSessions != null) {
      userSessions.add(session);
      WebSocketPool.websockets.put(userId, userSessions);
    } else {
      Set<WebSocketSession> newUserSessions = new HashSet<>();
      newUserSessions.add(session);
      WebSocketPool.websockets.put(userId, newUserSessions);
    }

  }

  @Override
  public void sendMessageToUser(Long userId, String message) throws IOException {

    Set<WebSocketSession> userSessions = WebSocketPool.websockets.get(userId);

    if (userSessions == null) {
      return;
    }

    TextMessage textMessage = new TextMessage(message);
    for (WebSocketSession session : userSessions) {
      session.sendMessage(textMessage);
    }

  }

  @Override
  public void removeFromSessionToPool(Long userId, WebSocketSession session) {
    Set<WebSocketSession> userSessions = WebSocketPool.websockets.get(userId);

    if (userSessions != null) {
      for (WebSocketSession sessionItem : userSessions) {
        if (sessionItem.equals(session)) {
          userSessions.remove(session);
        }
      }
    }
    WebSocketPool.websockets.put(userId, userSessions);
  }
}

```

With MessageHandler we are able to handle adding or removing `WebSocketSession` sessions from the pool as well as sending messages to a target user’s WebSocket sessions. On the other hand, `MessageSender` is going to define a KafkaTemplate broker to send the messages to a specified Kafka topic.

## MessageSender

```java
package com.endpoint.SpringKafkaMessaging.message.broker;

import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
public class MessageSender {

  private static final Logger LOG = LoggerFactory.getLogger(MessageSender.class);

  @Autowired
  private KafkaTemplate<String, String> kafkaTemplate;

  public void send(String topic, String message){

    kafkaTemplate.send(topic, message);
  }
}

```

Now we can create our WebSocketHandler. It will utilize MessageHandler to add and remove user sessions and MessageSender to send `WebSocketSession` messages to Kafka topics. I only used one topic in this messaging app, `SEND_MESSAGE`, but in a real application there would be a bunch of Kafka topics for sending different types of messages like new contact requests, notifications, etc..

### WebSocketHandler

```java
package com.endpoint.SpringKafkaMessaging.websocket;

import com.endpoint.SpringKafkaMessaging.cache.respository.CacheRepository;
import com.endpoint.SpringKafkaMessaging.message.broker.MessageSender;
import com.endpoint.SpringKafkaMessaging.persistent.model.User;
import com.endpoint.SpringKafkaMessaging.persistent.repository.UserRepository;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

@Component
public class WebSocketHandler extends TextWebSocketHandler {

  @Autowired
  CacheRepository cacheRepository;

  @Autowired
  UserRepository userRepository;

  @Autowired
  MessageHandler messageHandler;

  @Override
  public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {

    String parameters[] = session.getUri().getQuery().split("=");

    if(parameters.length == 2 && parameters[0].equals("accessToken")) {
      String accessToken = parameters[1];

      Long senderUserId = 0L;
      String senderId = cacheRepository.getUserIdByAccessToken(accessToken);

      if(senderId == null) {
        User sender = userRepository.findByToken(accessToken);
        if(sender != null) {
          senderUserId = sender.getUserId();
        }
      } else {
        senderUserId = Long.valueOf(senderId);
      }
      if (senderUserId == 0L) {
        return;
      }

      messageHandler.removeFromSessionToPool(senderUserId, session);
    }

  }

  @Override
  public void afterConnectionEstablished(WebSocketSession session) throws Exception {

    String parameters[] = session.getUri().getQuery().split("=");

    if(parameters.length == 2 && parameters[0].equals("accessToken")) {
      String accessToken = parameters[1];

      Long senderUserId = 0L;
      String senderId = cacheRepository.getUserIdByAccessToken(accessToken);

      if(senderId == null) {
        User sender = userRepository.findByToken(accessToken);
        if(sender != null) {
          senderUserId = sender.getUserId();
        }
      } else {
        senderUserId = Long.valueOf(senderId);
      }
      if (senderUserId == 0L) {
        return;
      }

      messageHandler.addSessionToPool(senderUserId, session);
    }
    else {
      session.close();
    }

  }

  @Autowired
  private MessageSender sender;

  @Override
  protected void handleTextMessage(WebSocketSession session, TextMessage textMessage) throws Exception {

    JSONObject jsonObject = new JSONObject(textMessage.getPayload());
    String topic = jsonObject.getString("topic");

    // only SEND_MESSAGE topic is available
    if(topic == null && !topic.equals("SEND_MESSAGE")) {
      return;
    }

    sender.send(topic, textMessage.getPayload());
  }
}
```

We can configure WebSocket in our application by adding the `WebSocketHandler` Bean and our custom `MessageHandler`.

### WebSocketConfig

```java
package com.endpoint.SpringKafkaMessaging.websocket;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;

@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer  {

  @Bean
  public WebSocketHandler myMessageHandler() {
    return new WebSocketHandler();
  }

  @Override
  public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
    registry.addHandler(myMessageHandler(), "/messaging").setAllowedOrigins("*");
  }

}

```

Now our WebSocket configuration is ready. Let’s configure our MessageService:

### MessageService

```java
package com.endpoint.SpringKafkaMessaging.message;

import com.endpoint.SpringKafkaMessaging.persistent.model.Message;

import java.util.List;

public interface MessageService {

  public void sendMessage(String accessToken, Long sendTo, String msg);

  List<Message> getMessageHistory(Long fromUserId, Long toUserId);
}

```

With our MessageService interface we can define common messaging methods to be utilized by the Kafka listeners. Notice the `sendMessage` method where we take `accessToken`, `sendTo` and `msg` parameters. `accessToken` will be used to authenticate user sending the message. `sendTo` is the user_id of the recipient.

### MessageServiceImpl

```java
package com.endpoint.SpringKafkaMessaging.message;

import com.endpoint.SpringKafkaMessaging.cache.respository.CacheRepository;
import com.endpoint.SpringKafkaMessaging.persistent.model.Message;
import com.endpoint.SpringKafkaMessaging.persistent.model.User;
import com.endpoint.SpringKafkaMessaging.persistent.repository.MessageRepository;
import com.endpoint.SpringKafkaMessaging.persistent.repository.UserRepository;
import com.endpoint.SpringKafkaMessaging.websocket.MessageHandler;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.List;

@Service
public class MessageServiceImpl implements MessageService{

  private static final Logger LOGGER = LoggerFactory.getLogger(MessageServiceImpl.class);

  @Autowired
  MessageRepository messageRepository;

  @Autowired
  CacheRepository cacheRepository;

  @Autowired
  UserRepository userRepository;

  @Autowired
  MessageHandler messageHandler;

  @Override
  public void sendMessage(String accessToken, Long sendTo, String msg) {

    Long senderUserId = 0L;
    String senderId = cacheRepository.getUserIdByAccessToken(accessToken);

    if(senderId == null) {
      User sender = userRepository.findByToken(accessToken);
      if(sender != null) {
        senderUserId = sender.getUserId();
      }
    } else {
      senderUserId = Long.valueOf(senderId);
    }
    if (senderUserId == 0L) {
      return;
    }

    try {
      // enrich message with senderId
      JSONObject msgJson = new JSONObject();
      msgJson.put("msg", msg);
      msgJson.put("senderId", senderUserId);
      messageHandler.sendMessageToUser(sendTo, msgJson.toString());
    } catch (IOException e) {
      return;
    }
  }

  @Override
  public List<Message> getMessageHistory(Long fromUserId, Long toUserId) {
    return messageRepository.findByFromUserIdAndToUserId(fromUserId, toUserId);
  }

  private void storeMessageToUser(Message message) {

    messageRepository.save(message);

  }
}
```

We are going to use message brokers as `MessageSender` and `MessageReceiver`. We’re going to define a `KafkaListener` listening to `SEND_MESSAGE` topic inside `MessageReceiver`, which is actually sending message to the target user. Here notice that `MessageReceiver` is not a client method; because this is a server side message orchestration application, it does not directly serve as a client interface. Above we implemented the WebSocket sessions where the actual communication with the clients happening, but the client application is out of our scope.

### MessageReceiver

```java
package com.endpoint.SpringKafkaMessaging.message.broker;

import com.endpoint.SpringKafkaMessaging.message.MessageService;
import com.endpoint.SpringKafkaMessaging.websocket.MessageHandler;
import com.endpoint.SpringKafkaMessaging.websocket.WebSocketPool;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.messaging.MessageHeaders;
import org.springframework.messaging.handler.annotation.Headers;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Service;

@Service
public class MessageReceiver {

  private static final Logger LOG = LoggerFactory.getLogger(MessageReceiver.class);

  @Autowired
  MessageService messageService;

  @Autowired
  MessageHandler messageHandler;

  @KafkaListener(topics = "SEND_MESSAGE")
  public void messagesSendToUser(@Payload String message, @Headers MessageHeaders headers) {

    JSONObject jsonObject = new JSONObject(message);

    if (WebSocketPool.websockets.get(jsonObject.getString("sendTo")) != null) {

      String accessToken = jsonObject.getString("accessToken");
      Long sendTo = Long.parseLong(jsonObject.getString("sendTo"));
      String msg = jsonObject.getString("msg");

      messageService.sendMessage(accessToken, sendTo, msg);

    }
  }

}
```

Here’s what our simple authentication service looks like:

### AuthService

```java
package com.endpoint.SpringKafkaMessaging.auth;

public interface AuthService {
  void putAccessToken(String accessToken, Long userId);
  Long loginWithAccessToken(String code);
}

```

### AuthServiceImpl

```java
package com.endpoint.SpringKafkaMessaging.auth;

import com.endpoint.SpringKafkaMessaging.persistent.model.User;
import com.endpoint.SpringKafkaMessaging.persistent.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.endpoint.SpringKafkaMessaging.cache.respository.CacheRepository;
import com.endpoint.SpringKafkaMessaging.persistent.model.AccessToken;
import com.endpoint.SpringKafkaMessaging.persistent.repository.AccessTokenRepository;

import java.util.Calendar;
import java.util.UUID;

@Service
public class AuthServiceImpl implements AuthService {

  @Autowired
  CacheRepository cacheRepository;

  @Autowired
  AccessTokenRepository accessTokenRepository;

  @Autowired
  UserRepository userRepository;

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
  public Long loginWithAccessToken(String token) {
    String userIdStr = cacheRepository.getUserIdByAccessToken(token);
    if(userIdStr == null) {
      User user = userRepository.findByToken(token);
      if(user != null)
        return user.getUserId();
      else
        return 0L;
    }
    return Long.valueOf(userIdStr);
  }
}

```

### AuthController

```java
package com.endpoint.SpringKafkaMessaging.auth.controller;

import javax.validation.Valid;

import com.endpoint.SpringKafkaMessaging.persistent.model.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import com.endpoint.SpringKafkaMessaging.auth.AuthService;
import com.endpoint.SpringKafkaMessaging.cache.respository.CacheRepository;
import com.endpoint.SpringKafkaMessaging.persistent.repository.UserRepository;
import com.endpoint.SpringKafkaMessaging.util.StringHelper;

import java.util.UUID;


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
    
    int code = StringHelper.generateRandomNumber(6);
    
    // save the activation code to the cache repository (cached auth token)
    cacheRepository.putActivationCode(activationRequest.getMobile(), String.valueOf(code));

    ActivationResponse activationResponse = ActivationResponse.builder()
        .mobile(activationRequest.getMobile())
        .activationCode(String.valueOf(code))
        .build();
    
    return new ResponseEntity<>(
        activationResponse,
        HttpStatus.OK);
  }
  
  @RequestMapping(value = "/login", method = RequestMethod.POST, consumes = MediaType.APPLICATION_JSON_UTF8_VALUE, produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
  public ResponseEntity<Object> login(@RequestBody LoginRequest loginRequest) {
    String mobile = cacheRepository.queryMobileActivationCode(loginRequest.getMobile(), loginRequest.getActivationCode());

    if(mobile == null) {
      return new ResponseEntity<>(
          "Mobile number not found!",
          HttpStatus.NOT_FOUND);
    } else {
      Long userId = 0L;
      User user = userRepository.findByMobile(loginRequest.getMobile());
      if(user == null) {
        // save user in persistence
        userRepository.save(
            User.builder()
            .mobile(loginRequest.getMobile())
            .build()
        );
        user = userRepository.findByMobile(loginRequest.getMobile());
      }
      userId = user.getUserId();
      String accessToken = UUID.randomUUID().toString();
      authService.putAccessToken(accessToken, userId);

      return new ResponseEntity<>(
          LoginResponse.builder()
              .accessToken(accessToken)
              .build(),
          HttpStatus.OK);
    }
  }

}

```

Here the authentication controller is consumed by a client application, which will use the `/getcode` endpoint to get an activation code for a mobile number. Then the client application will use the `/login` endpoint, passing their activation code. Once the `/login` endpoint confirms the activation code, it will return an access token to the client for future requests. The client application will be responsible for adding the accessToken to all WebSocket session messages. Here we used a `StringHelper` method to generate the activation code and a random UUID string to generate an accessToken. Since UUID is not an ideal random token generator for authentication, you should use your own token generator algorithm.
