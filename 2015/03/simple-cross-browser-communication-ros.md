---
author: Matt Vollrath
title: Simple cross-browser communication with ROS
github_issue_number: 1107
tags:
- javascript
- liquid-galaxy
- ros
date: 2015-03-24
---

[ROS](http://www.ros.org/) and [RobotWebTools](http://robotwebtools.org/) have been extremely useful in building our latest crop of distributed interactive experiences. We’re continuing to develop browser-fronted ROS experiences very quickly based on their huge catalog of existing device drivers. Whether a customer wants their interaction to use a touchscreen, joystick, lights, sound, or just about anything you can plug into the wall, we now say with confidence: “Yeah, we can do that.”

A typical ROS system is made out of a group (“graph”) of nodes that communicate with (usually TCP) messaging. Topics for messaging can be either publish/subscribe namespaces or request/response services. ROS bindings exist for several languages, but C++ and Python are the only supported direct programming interfaces. ROS nodes can be custom logic processors, aggregators, arbitrators, command-line tools for debugging, native Arduino sketches, or just about any other imaginable consumer of the data streams from other nodes.

The [rosbridge server](https://github.com/RobotWebTools/rosbridge_suite/tree/master), implemented with [rospy](http://wiki.ros.org/rospy) in Python, is a ROS node that provides a web socket interface to the ROS graph with a simple JSON protocol, making it easy to communicate with ROS from any language that can connect to a web socket and parse JSON. Data is published to a messaging topic (or topics) from any node in the graph and the rosbridge server is just another subscriber to those topics. This is the critical piece that brings all the magic of the ROS graph into a browser.

A handy feature of the [rosbridge JSON protocol](https://github.com/RobotWebTools/rosbridge_suite/blob/master/ROSBRIDGE_PROTOCOL.md) is the ability to create topics on the fly. For interactive exhibits that require multiple screens displaying synchronous content, topics that are only published and subscribed between web socket clients are a quick and dirty way to share data without writing a “third leg” ROS node to handle input arbitration and/or logic. In this case, rosbridge will act as both a publisher and a subscriber of the topic.

To develop a ROS-enabled browser app, all you need is an Ubuntu box with ROS, the rosbridge server and a web socket-capable browser installed. Much has been written about [installing ROS (indigo)](http://wiki.ros.org/indigo/Installation/Ubuntu), and once you’ve installed ros-indigo-ros-base, set up your shell environment, and started the ROS core/master, a rosbridge server is two commands away:

```
$ sudo apt-get install ros-indigo-rosbridge-suite
$ rosrun rosbridge_server rosbridge_websocket
```

While rosbridge is running, you can connect to it via ws://hostname:9090 and access the ROS graph using the rosbridge protocol. Interacting with rosbridge from a browser is best done via [roslibjs](http://wiki.ros.org/roslibjs), the JavaScript companion library to rosbridge. All the JavaScripts are available from the [roslibjs CDN](http://wiki.ros.org/roslibjs#CDN_Releases) for your convenience.

```javascript
<script type="text/javascript"
  src="http://cdn.robotwebtools.org/EventEmitter2/current/eventemitter2.min.js">
</script>
<script type="text/javascript"
  src="http://cdn.robotwebtools.org/roslibjs/current/roslib.min.js">
</script>
```

From here, you will probably want some shared code to declare the Ros object and any Topic objects.

```javascript
//* The Ros object, wrapping a web socket connection to rosbridge.
var ros = new ROSLIB.Ros({
  url: 'ws://localhost:9090' // url to your rosbridge server
});

//* A topic for messaging.
var exampleTopic = new ROSLIB.Topic({
  ros: ros,
  name: '/com/endpoint/example', // use a sensible namespace
  messageType: 'std_msgs/String'
});
```

The messageType of [std_msgs/String](http://docs.ros.org/api/std_msgs/html/msg/String.html) means that we are using a message definition from the std_msgs package (which ships with ROS) containing a single string field. Each topic can have only one messageType that must be used by all publishers and subscribers of that topic.

A “proper” ROS communication scheme will use predefined message types to serialize messages for maximum efficiency over the wire. When using the std_msgs package, this means each message will contain a value (or an array of values) of a single, very specific type. See the [std_msgs documentation](http://wiki.ros.org/std_msgs) for a complete list. Other message types may be available, depending on which ROS packages are installed on the system.

For cross-browser application development, a bit more flexibility is usually desired. You can roll your own data-to-string encoding and pack everything into a single string topic or use multiple topics of appropriate messageType if you like, but unless you have severe performance needs, a JSON stringify and parse will pack arbitrary JavaScript objects as messages just fine. It will only take a little bit of boilerplate to accomplish this.

```javascript
/**
 * Serializes an object and publishes it to a std_msgs/String topic.
 * @param {ROSLIB.Topic} topic
 *       A topic to publish to. Must use messageType: std_msgs/String
 * @param {Object} obj
 *       Any object that can be serialized with JSON.stringify
 */
function publishEncoded(topic, obj) {
  var msg = new ROSLIB.Message({
    data: JSON.stringify(obj)
  });
  topic.publish(msg);
}

/**
 * Decodes an object from a std_msgs/String message.
 * @param {Object} msg
 *       Message from a std_msgs/String topic.
 * @return {Object}
 *       Decoded object from the message.
 */
function decodeMessage(msg) {
  return JSON.parse(msg.data);
}
```

All of the above code can be shared by all pages and views, unless you want some to use different throttle or queue settings on a per-topic basis.

On the receiving side, any old anonymous function can handle the receipt and unpacking of messages.

```javascript
// Example of subscribing to a topic with decodeMessage().
exampleTopic.subscribe(function(msg) {
  var decoded = decodeMessage(msg);
  // do something with the decoded message object
  console.log(decoded);
});
```

The sender can publish updates at will, and all messages will be felt by the receivers.

```javascript
// Example of publishing to a topic with publishEncoded().
// Explicitly declare that we intend to publish on this Topic.
exampleTopic.advertise();

setInterval(function() {
  var mySyncObject = {
    time: Date.now(),
    myFavoriteColor: 'red'
  };
  publishEncoded(exampleTopic, mySyncObject);
}, 1000);
```

From here, you can add another layer of data shuffling by writing message handlers for your communication channel. Re-using the EventEmitter2 class upon which roslibjs depends is not a bad way to go. If it feels like you’re implementing ROS messaging on top of ROS messaging.. well, that’s what you’re doing! This approach will generally break down when communicating with other non-browser nodes, so use it sparingly and only for application layer messaging that needs to be flexible.

```javascript
/**
 * Typed messaging wrapper for a std_msgs/String ROS Topic.
 * Requires decodeMessage() and publishEncoded().
 * @param {ROSLIB.Topic} topic
 *       A std_msgs/String ROS Topic for cross-browser messaging.
 * @constructor
 */
function RosTypedMessaging(topic) {
  this.topic = topic;
  this.topic.subscribe(this.handleMessage_.bind(this));
}
RosTypedMessaging.prototype.__proto__ = EventEmitter2.prototype;

/**
 * Handles an incoming message from the topic by firing an event.
 * @param {Object} msg
 * @private
 */
RosTypedMessaging.prototype.handleMessage_ = function(msg) {
  var decoded = decodeMessage(msg);
  var type = decoded.type;
  var data = decoded.data;
  this.emit(type, data);
};

/**
 * Sends a typed message to the topic.
 * @param {String} type
 * @param {Object} data
 */
RosTypedMessaging.prototype.sendMessage = function(type, data) {
  var msg = {type: type, data: data};
  publishEncoded(this.topic, msg);
};
```

Here’s an example using RosTypedMessaging.

```javascript
//* Example implementation of RosTypedMessaging.
var myMessageChannel = new RosTypedMessaging(exampleTopic);

myMessageChannel.on('fooo', function(data) {
  console.log('fooo!', data);
});

setInterval(function() {
  var mySyncObject = {
    time: Date.now(),
    myFavoriteColor: 'red'
  };
  myMessageChannel.sendMessage('fooo', mySyncObject);
}, 1000);
```

If you need to troubleshoot communications or are just interested in seeing how it works, ROS comes with some neat command line tools for publishing and subscribing to topics.

```nohighlight
### show messages on /example/topicname
$ rostopic echo /example/topicname

### publish a single std_msgs/String message to /example/topicname
### the quotes are tricky, since rostopic pub parses yaml or JSON
$ export MY_MSG="data: '{\"type\":\"fooo\",\"data\":{\"asdf\":\"hjkl\"}}'"
$ rostopic pub -1 /example/topicname std_msgs/String "$MY_MSG"
```

To factor input, arbitration or logic out of the browser, you could write a roscpp or rospy node acting as a server. Also worth a look are ROS services, which can abstract asynchronous data requests through the same messaging system.

A [gist of this example JavaScript](https://gist.github.com/minshallj/50e6b2e85985ca56e8e0) is available, much thanks to [Jacob Minshall](/team/jacob-minshall).
