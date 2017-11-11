---
author: Selvakumar Arumugam
gh_issue_number: 1272
tags: rails, javascript, websocket
title: Implementation of Ruby on Rails 5 Action Cable with Chat Application
---

Ruby on Rails is a wonderful framework for web development. It was lacking for one important feature since the world has been moving to towards realtime data. Everyone wants to see the realtime data on the applications. Mostly, real-time web applications are now accomplished using WebSocket.

WebSocket provides full-duplex communication between server and client using TCP connection once the handshake completed through HTTP protocol. [WebSocket transfers streams of messages on top TCP](https://en.wikipedia.org/wiki/WebSocket#Overview) without being solicited by the client which boosts the data transfer performance on high level compare to HTTP request/response.

WebSocket were adopted on RoR applications with help of third party libraries. But Rails 5 came up with a module called ActionCable which is seamlessly sits with existing framework and integrates the WebSocket to the application. ActionCable provides server and client side framework to implement WebSocket with the application.

## ActionCable Overview:

##### Server Side:

**Connection:** The Connection only handles authentication and authorisation part of logic. The connection object is instantiated when request from the user comes through browser tab or window or devices. Multiple connections could be created when the user access the server from different devices/browser tabs.

**Channel:** The Channel is the parent of all custom channels and shares the common logic with all channels. The custom channels will stream the messages to client when the corresponding channels were subscribed by client.

##### Client Side:

The Client side javascript framework have all functionalities to interact with server side. The Consumer will establish a WebSocket connection with Server to do all the communications. Subscriber subscribes the custom channels to receive the messages from the Server without requests.

**Prerequisite:**

* Ruby 2.2.2 or newer is required for Rails 5. Install the gem package and Rails 5 on your environment.

* ActionCable needs puma as development server to support multithreaded feature.

Let's create the rails 5 chat application...! The application structure will have following default action cable related files.

```shell
$ rails new action-cable-chat-example
 - Server Side
        app/channels
        app/channels/application_cable
        app/channels/application_cable/connection.rb
        app/channels/application_cable/channel.rb

 - Client Side
        app/assets/javascripts
        app/assets/javascripts/channels
        app/assets/javascripts/channels/.keep
        app/assets/javascripts/application.js
        app/assets/javascripts/cable.js
```

Below models and controllers need to be created to have basic chat application.

* User, Room and Message models

* users, rooms, messages, sessions and welcome controllers

The commands to create these items are listed below and skipping the code to focus on ActionCable but the code is available at [github to refer or clone](https://github.com/selvait90/rails5-actioncable-chat-application).

```shell
$ bundle install
$ rails g model user name:string
$ rails g model room title:string name:string user:references
$ rails g model message content:text user:references room:references
$ rake db:migrate

$ rails g controller users new create show
$ rails g controller rooms new create update edit destroy index show
$ rails g controller messages create

$ rails g controller sessions new create destroy
$ rails g controller welcome about
```

Make necessary changes to controllers, models and views to create chat application with chat rooms([Refer Github Repository](https://github.com/selvait90/rails5-actioncable-chat-application)). Start the application with help of puma server to verify the basic functionalities.

```shell
$ rails s -b 0.0.0.0 -p 8000
```

The application should meet following actions. The User will sign up or login with username to get the access new or existing rooms to chat. The user can write messages on the chat room but the messages won't appear to other users at the moment without refreshing the page. Let's see how ActionCable handles it.

## Action Cable Implementation:

**Configurations:**

There are few configurations to enable the ActionCable on the application.

*config/routes.rb* - The server should be mounted on specific path to serve websocket cable requests.

```ruby
mount ActionCable.server =&gt; '/cable'
```

*app/views/layouts/application.html.erb* - The action_cable_meta_tag passes the WebSocket URL(which is configured on environment variable config.action_cable.url) to consumer.

```ruby
&lt;%= action_cable_meta_tag %&gt;
```

*app/assets/javascripts/cable.js* - The consumer should be created to establish the WebSocket connection to specified URL in action-cable-url.

```javascript
(function() {
  this.App || (this.App = {});

  App.cable = ActionCable.createConsumer();

}).call(this);
```

Once ActionCable was enabled, the WebSocket connection will be established on accessing the application from any client. But the messages will transmitted only through channels. Here is the sample handshake to create WebSocket connection.

```html
General:
Request URL:ws://139.59.24.93:8000/cable
Request Method:GET
Status Code:101 Switching Protocols

Request Headers:
Connection:Upgrade
Host:139.59.24.93:8000
Origin:http://139.59.24.93:8000
Sec-WebSocket-Extensions:permessage-deflate; client_max_window_bits
Sec-WebSocket-Key:c8Xg5vFOibCl8rDpzvdgOA==
Sec-WebSocket-Protocol:actioncable-v1-json, actioncable-unsupported
Sec-WebSocket-Version:13
Upgrade:websocket

Response Headers:
Connection:Upgrade
Sec-WebSocket-Accept:v46QP1XBc0g5JYHW7AdG6aIxYW0=
Sec-WebSocket-Protocol:actioncable-v1-json
Upgrade:websocket
```

The /cable is the default URI. if there is a custom URI, it need to mentioned environment file. The origins need to be allowed in the configuration if it is other than localhost.

*environments/development.rb*

```ruby
# config.action_cable.url = 'wss://example.com/cable'
# config.action_cable.allowed_request_origins = [ 'http://example.com', /http:\/\/example.*/ ]
```
**Workflow:**

I created a diagram to illustrate how the pieces fit together and explain the workflow.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2016/12/03/implementation-of-ruby-on-rails-5/image-0.png" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2016/12/03/implementation-of-ruby-on-rails-5/image-0.png"/></a></div>

**Channels:**

The Server side messages channel need to be created to stream the messages from Server to all subscribed clients and client side framework to subscribe the channels to receive the messages. Execute the channels generator and create messages channels skeleton to code on server and client side.

```shell
$ rails generate channel Messages

 app/channels/messages_channel.rb
 app/assets/javascripts/channels/messages.js
```

*messages_controller.rb* - Whenever the user writes a message in the room, it will be broadcasted to 'messages' channel after the save action.

```html
class MessagesController &lt; ApplicationController
  def create
    message = Message.new(message_params)
    message.user = current_user
    if message.save
      ActionCable.server.broadcast 'messages',
        message: message.content,
        user: message.user.username
      head :ok
    end
  end

  private

    def message_params
      params.require(:message).permit(:content, :chatroom_id)
    end
end
```

*messages_channel.rb* - Messages channel streams those broadcasted messages to subscribed clients through established WebSocket connection.

```ruby
class MessagesChannel &lt; ApplicationCable::Channel
  def subscribed
    stream_from 'messages'
  end
end
```

*messages.js* The MessagesChannel was subscribed on accessing the Rooms to chat. The client side receives the message as per subscriptions and populate on the chat room dynamically.

```javascript
App.messages = App.cable.subscriptions.create('MessagesChannel', {
  received: function(data) {
    $("#messages").removeClass('hidden')
    return $('#messages').append(this.renderMessage(data));
  },
  renderMessage: function(data) {
    return "<p><b>" + data.user + ": </b>" + data.message + "</p>";
  }
});
```

These ActionCable channel related changes could make the Chat application to receive the messages on realtime.

## Conclusion:

Rails Action Cable adds additional credits to framework by supplying the promising needed realtime feature. In addition, It could be easily implemented on existing Rails application with the nature of interacting with existing system and similar structural implementation. Also, The strategy of the channels workflow can be applied to any kind of live data feeding. The production stack uses redis by default (config/cable.yml) to send and receive the messages through channels.
