---
author: "Kürşat Kutlu Aydemir"
title: "Creating a Messaging App Using Spring for Apache Kafka, Part 5"
date: 2022-10-07
tags:
- java
- spring
- apache-kafka
- spring-kafka-series
---

![Close Up Photo of Pencils](/blog/2022/10/spring-kafka-messaging-part-5/pencils-closeup.webp)
[Photo by BOOM 💥](https://www.pexels.com/photo/close-up-photo-of-pencils-12585543/)

I guess this is the longest break I gave for a post of this series. But finally I had a chance to touch it and prepare a working example to finalize this series. So, up-to-date code is aready available in the [GitHub repository](https://github.com/ashemez/SpringKafkaMessaging).

## Activation and Login

This was already implemented in the previous parts. However, we didn't show that in action yet. There can some code fixes and small changes within the workflow of activation and login steps. So you can refer to the GitHub repository for the latest code.

Authentication and activation is managed through the `AuthController` class where these activation and login requests are handled. Let's take a look at the `REST` endpoints handling these requests and explain the steps.

### Activation

Activation is a pretend mobile phone number activation step. You can think of it like you activate your messaging application (like Whatsapp) against your phone number you are associating with. There is no restriction I introduced in this application so you can assume that the phone number activation is just a pretending pseudo step and you can supply any number. But in real life, the phone number activation would use a real SMS or other activation services to activate your chat application against the user's real phone number.

The activation endpoint is `/api/auth/getcode` takes the mobile number as payload. A sample `curl` command is like below:

```shell
curl -H "Content-Type: application/json" -X POST localhost:8080/api/auth/getcode -d '{ "mobile": "01234" }'
```

The response of this endpoint is `ActivationResponse` which in return gives an activation code along with the provided mobile number. This `activationCode` later will be used to login and retreive an access token for further loginless connections. Here is a example output of this response.

```JSON
{
  "mobile": "01234",
  "activationCode": "309652"
}
```

This random activation code is provided for the given mobile number and the client is now responsible to use this activation to move one step further to get an access token to use it for furter authentication purpose.

### Login

The login step is supposed to be a one time login after getting the activation code which is used as login credential for the given mobile number. Our application returns an access token in return. Login endpoint is `/api/auth/login`. Request and response examples are like below.

```shell
curl -H "Content-Type: application/json" -X POST localhost:8080/api/auth/login -d '{ "mobile": "01234", "activationCode": "309652" }'
```
Running login endpoint gives an access token in return. The access token is further needed in the message sending requests so that the client can be authenticated. Storing locally and reusing this access token is responsibility of the client.

```JSON
{
  "accessToken": "5eab27f8-8748-4fdc-a4de-ac782ce17a74"
}
```

## Chat Application

To show the messaging in action the chat application is the final part of this series. Chat application is designed as a simple proof of concept in idea and simulates a chatting session.

To extend our Spring application with some web UI added two static files `app.js` and `index.html` under `resources` directory. `index.html` is supposed to serve as the chat application UI and `app.js` is responsible for making ajax calls and WebSocket connection from the client browser.

![Chat UI](/blog/2022/10/spring-kafka-messaging-part-5/kafkamessagewebui.webp)
I added all the three steps in the chat application UI to make the workflow clearer. As you see in the chat screen above these three steps are activation, login and starting a new chat. Let's walk through these steps. 

### Activation and login through the chat application

Activation simply requires a pretend mobile phone number and when you click on `Activate` button it just simply posts the request to `/api/auth/getcode` endpoint we mentioned above.

```Javascript
function activate() {
  var mobileFormData = JSON.stringify({
    'mobile': $("#mobile").val(),
  });

  console.log("here we are")
  $.ajax({
    type: "POST",
    url: "http://localhost:8080/api/auth/getcode",
    data: mobileFormData,
    contentType: "application/json;charset=utf-8",
    success: function(result){
        $("#activationCode").val(result.activationCode);
    }
  });
}
```

The result `activationCode` is automatically put into login input. Now you already know what this activationCode is and where it is stored in the backend. So, now our chat client can use this activationCode along with the mobile number to login and get the access token. When you click on `Login` button it posts to `/api/auth/login` endpoint and gets the access token into the `Access Token` input box this time.

```Javascript
function login() {
  var loginFormData = JSON.stringify({
    'mobile': $("#mobile").val(),
    'activationCode': $("#activationCode").val(),
  });

  $.ajax({
    type: "POST",
    url: "http://localhost:8080/api/auth/login",
    data: loginFormData,
    contentType: "application/json;charset=utf-8",
    success: function(result){
        $("#accessToken").val(result.accessToken);
    }
  });
}
```

Now finally our web client can connect to our Websocket URI. Without a login step we could let our application to accept Websocket connections as well, however we simulated an authentication step and we want to know who is connecting to WebSocket handler.

```Javascript
function connect() {
	ws = new WebSocket('ws://localhost:8080/messaging?accessToken=' + $("#accessToken").val());
    ws.addEventListener('error', (error) => {
		console.log("Error: ", error.message);
		setConnected(false);
    });
    ws.addEventListener('close', (event) => {
		console.log("Close: ", event.code + " - " + event.reason);
	    setConnected(false);
    })
	ws.onmessage = function(event) {
		helloWorld(event.data);
		console.log("Connected to websocket " + event.data);
	}
	setConnected(true);
}
```

### WebSocket Handshake

In our `WebSocketConfig` class I added an WebSocket handshake interceptor `    WSHandshakeInterceptor` to authenticate the connecting user by checking the `accessToken`. So, `accessToken` is necessary at first step while connecting to the WebSocket registry. If the client doesn't provide an accessToken or provides an invalid accessToken then the handshake will fail.

```Java
    @Override
    public boolean beforeHandshake(ServerHttpRequest serverHttpRequest, ServerHttpResponse serverHttpResponse, org.springframework.web.socket.WebSocketHandler webSocketHandler, Map<String, Object> map) throws Exception {

        LOG.info("hand shaking for ws session url  " + serverHttpRequest.getURI().getPath() + " ? " + serverHttpRequest.getURI().getQuery());
        String parameters[] = serverHttpRequest.getURI().getQuery().split("=");

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

            LOG.info("Handshake found userId: " + senderUserId);

            if (senderUserId == 0L) {
                LOG.info("Handshake failed: user not found for given accessToken");
                map.put("CUSTOM-HEADER", "Handshake failed: user not found for given accessToken");
                return false;
            }

            map.put("CUSTOM-HEADER", "Handshake successful");
            LOG.info("Handshake successful");
            return true;
        }

        map.put("CUSTOM-HEADER", "Handshake failed: accessToken not found");
        LOG.info("Handshake failed: accessToken not found");
        return false;

    }
```

If everything goes well and our webclient is connected to WebSocket then the client can start sending messages to the other WebSocket sessions. We don't manage offline messaging or other capabilities in this application. As you'll see a WebSocket session will be able to send messages to only corresponding active WebSocket sessions. In real life examples you would manage offline messaging and deliver to the destination users whenever they become online.

### Chat in action

When I open the chat application in two different browsers and login with different mobile numbers I woul be able to make them have a chat. I assume mobile number `01234` has two contacts `12345` and `23456` in their contact list.

On this screen I checked `12345` contact to start messaging. I entered my message and clicked on `Send` button. Since both clients connected to WebSocket I was able to send the message to `12345` as you can see on the second client's window.


![Chatting](/blog/2022/10/spring-kafka-messaging-part-5/km-chat-in-action.webp)

The messages are not tidied here but to show you that in action I made the WebSocket message to be listing the message on the client where it connected to its WebSocket session.

Here is the Javascript code sending the message to WebSocket session when you click on `Send` button.

```Javascript
function sendData() {
	var data = JSON.stringify({
	  'topic': 'SEND_MESSAGE',
	  'message': {
	    'accessToken': $("#accessToken").val(),
	    'sendTo': $("#sendTo").val(),
	    'msg': $("#messageArea").val(),
	  }
	})
	ws.send(data);
}
```

When we send the message to WebSocket, our `WebSocketHandler` handles the received message through WebSocket session. However, it doesn't directly sends the message to the corresponding WebSocket session. We send our message to the Kafka topic `SEND_MESSAGE` using `MessageSender.send()` method at this point  and Kafka manages the streaming messages.

On the Kafka listener side of our application `MessageReceiver.messagesSendToUser()` is receiving the messages and it redirects the messages to the corresponding WebSocket session. So we took this workload from WebSocket handler to Kafka listener so it would be busy only with the messages sent by the clients. Another approach would be sending the messages directly to Kafka topics instead of WebSocket handler so we would give all the workload to Kafka services.

```Java
    @KafkaListener(topics = "SEND_MESSAGE", groupId = "foo")
    public void messagesSendToUser(@Payload String message, @Headers MessageHeaders headers) {

        JSONObject jsonObject = new JSONObject(message);

        LOG.info("Websocket message will be sent if corresponding destination websocket session is found");
        if (jsonObject.get("sendTo") != null
                && WebSocketPool.websockets.get(jsonObject.getLong("sendTo")) != null
                && WebSocketPool.websockets.get(jsonObject.getLong("sendTo")).size() > 0) {

            String accessToken = jsonObject.getString("accessToken");
            Long sendTo = jsonObject.getLong("sendTo");
            String msg = jsonObject.getString("msg");

            LOG.info("Websocket message is sent to " + sendTo);

            String topic = "SEND_MESSAGE";

            messageService.sendMessage(accessToken, sendTo, msg, topic);

        } else {
            LOG.info("Websocket session not found for given sendTo");
        }
    }
```

Here is our logging for the message sent through the chat application.

```
2022-10-07 16:36:41.371  INFO 37554 --- [nio-8080-exec-1] c.e.S.websocket.WebSocketHandler         : {"topic":"SEND_MESSAGE","message":{"accessToken":"5eab27f8-8748-4fdc-a4de-ac782ce17a74","sendTo":"5","msg":"Hey dude, howdy?"}}
2022-10-07 16:36:41.411  INFO 37554 --- [ntainer#0-0-C-1] c.e.S.message.broker.MessageReceiver     : Websocket message will be sent if corresponding destination websocket session is found
2022-10-07 16:36:41.411  INFO 37554 --- [ntainer#0-0-C-1] c.e.S.message.broker.MessageReceiver     : Websocket message is sent to 5
2022-10-07 16:36:41.412  INFO 37554 --- [ntainer#0-0-C-1] c.e.S.message.broker.MessageReceiver     : Sending websocket message {"msg":"Hey dude, howdy?","senderId":4,"topic":"SEND_MESSAGE"}
```

## What is the point of using Kafka and Websocket?

Let's go back to the question why we used Kafka and Websockets for a messaging app. We questioned this paradigm in [part 1](https://www.endpointdev.com/blog/2020/04/messaging-app-spring-kafka-pt-one/) of this series while discussing the design and architecture. Actually that all depends on what you aim to do with a messaging application.

There are times when WebSocket has advantage over HTTP or XMPP and these protocols can be compared for certain cases. The debates are not going to be done in this post either. WebSocket simply is a fast relaying and simple protocol which enables a web server app to communicate with web browser or more broadly WebSocket clients easily. So you can use WebSocket to create chat applications over Web and let the same user's multiple sessions run concurrently on multiple clients.

Kafka, on the other hand, a message orchestrator, highly aware of what is coming in and going out and can be scaled upwards. You can guarantee to process each messages arrived at Kafka without worrying concurrency and delay issues which you can usually face with traditional threads or services. Kafka is not a chat application backend essentially but can handle the millions and even billions of messages easily. The main purpose of this example application is not creating a chat application but as you can notice from the title, a messaging application.

So, while chatting would designate a narrow scope, messaging name is used to address a broad application to handle high load of data streaming environments.

## Conclusion

Kafka is used in several environments by lots of giants of the industries and startups. A few industry examples would be financial services, telecom, manufacturing and healthcare. You can make data streaming seamless and real-time using Kafka. Would you mind sharing your experiences using Kafka and related technologies. That can even include ML and model training streams.
