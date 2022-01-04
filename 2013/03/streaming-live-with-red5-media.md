---
author: Marina Lohova
title: 'Streaming Live with Red5 Media Server: Two-Way'
github_issue_number: 767
tags:
- java
- video
- audio
date: 2013-03-07
---

I already wrote about [the basics of publishing and broadcasting](/blog/2012/04/streaming-live-with-red5-media-server) with Red5 Media Server. Let’s fast forward to the advanced topics and create a video conference now!

### Getting Ready

First, a word about the technology stack: a little bit of Java6/Java EE will be used for the server-side work (Red5 is written in Java), ActionScript2/Adobe Flash CS6 will be the primary tool for the client side development, and OS X Mountain Lion is my operating system.

Red5 Server comes with the set of sample applications that provide the source code for about everything you may want to achieve. The primary challenge is to unleash the power of it, since the samples fall extremely short of documentation! The **“fitcDemo”** application will serve as a base for all our customization.

Originally I made all the development in Red5 RC 1.0 version where fitcDemo was present. Unfortunately, when I downloaded the latest Red5 1.0.1 release yesterday it was simply not there! The source code was still in the repo, just outdated and not working. Well, I did all the work for Red5 team, so you can just download [fitcDemo.war](https://github.com/marinalohova/red5-example/blob/master/fitcDemo/dist/fitcDemo.war) from my repo and drop it into the **“webapps”** directory of Red5 1.0.1 installation—​and you are good!

You will then find the video conference demo at [http://localhost:5080/demos/videoConference.html](http://localhost:5080/demos/videoConference.html)

Here is how it looks out of the box:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/03/streaming-live-with-red5-media/image-0.jpeg" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/03/streaming-live-with-red5-media/image-0.jpeg"/></a></div>

Here is how we want it to look!

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/03/streaming-live-with-red5-media/image-1.jpeg" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/03/streaming-live-with-red5-media/image-1.jpeg"/></a></div>

The goal is to make our Red5 conference look as neat as Google Hangout.

### Sleek Subscribers

Default video conference has five subscribers statically positioned on the stage. It’s way more fun to have the subscribers added and removed on the fly as they connect to the server. So let’s do that! I have the complete tutorial code based on Red5 1.0.1 The final version is in my [GitHub repo](https://github.com/marinalohova/red5-flash), so I will be explaining parts of it further. Open [videoConference.fla](https://github.com/marinalohova/red5-flash/blob/master/videoConference.fla) in Flash. I used CS6 for all the FLA/ActionScript editing in the tutorial.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/03/streaming-live-with-red5-media/image-2.jpeg" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/03/streaming-live-with-red5-media/image-2.jpeg"/></a>  <br/>
</div>

Edit the VideoConference clip in the Library, to remove everything in it and add a ScrollPane with the following properties:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/03/streaming-live-with-red5-media/image-3.jpeg" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/03/streaming-live-with-red5-media/image-3.jpeg"/></a><br/>
</div>

Edit the VideoPool clip, to remove everything in it as well and drag a Broadcaster clip to the top left corner:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/03/streaming-live-with-red5-media/image-4.jpeg" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/03/streaming-live-with-red5-media/image-4.jpeg"/></a><br/>
</div>

Broadcaster and Subscriber clips should be modified too and have only the video component visible. You may look into the complete source code for details. Don’t forget to change the Publish Settings to **Flash Player 8; ActionScript2** and publish.

Modify [Connector.as](https://github.com/marinalohova/red5-flash/blob/master/classes/org/red5/samples/livestream/videoconference/Connector.as) to point to the Red5 server. It is important to specify the IP address of the host machine rather than just “localhost”, so other computers can join the hangout over network.

```javascript
public static var red5URI:String = "rtmp://192.168.0.5/fitcDemo";
```

Make a slight change to configUI() to make it auto connect:

```javascript
public function configUI():Void
 {
  connection  = new Connection();

  connection.addEventListener("success", Delegate.create(this, onComplete));
  connection.addEventListener("onSetID", this);

  connection.addEventListener("newStream", this);
  connection.addEventListener("close", Delegate.create(this, onComplete));
  connected = connection.connect(red5URI, getTimer());
  dispatchEvent({type:"connectionChange", connected: connected});
 }

 private function onComplete(evtObj:Object):Void
 {
  dispatchEvent({type:"connectionChange", connected: evtObj.connected});
 }
```

Get rid of all the default Subscriber variables in the class and change configUI():

```javascript
private function configUI():Void
{
  subscriberList = [];
}
```

Open [VideoPool.as](https://github.com/marinalohova/red5-flash/blob/master/classes/org/red5/samples/livestream/videoconference/VideoPool.as) and modify getVideoContainer() so that every subscriber will be dynamically created and positioned on stage. The row will have 4 streams with the broadcaster stream (your computer’s camera) being the first in the first row, and more rows will be created in the scroll pane to accommodate more streams.

```javascript
private function getVideoContainer(p_id:Number):Subscriber
{
  var d:Number = 1;
  if (subscriberList.length > 0) {
    d = subscriberList[subscriberList.length - 1].getDepth() + 1;
  }

  var positionX:Number = broadcaster._x + ((subscriberList.length + 1)%4) * broadcaster._width;
  var positionY:Number = broadcaster._y + (broadcaster._height * Math.floor((subscriberList.length + 1)/4));

  attachMovie("org.red5.samples.livestream.videoconference.Subscriber", "subscriber_" + p_id, d, {_x:positionX, _y:positionY});

  var s:Subscriber = _level0.instance1.scrollPane.content["subscriber_" + p_id];
  subscriberList.push(s);
  return s;
}
```

The new Subscriber instance for the particular stream will be generated when subscribe() method is called.

```javascript
public function subscribe(p_id:Number):Void
{
  if(p_id == "undefined" || isNaN(p_id) || p_id == "") return;

  var s:Subscriber = getVideoContainer(p_id);

  s.subscribe("videoStream_" + p_id, connection);
}
```

If the subscriber is added, at some point it may need to be removed! Add removeSubscriber() function that will delete the disconnected subscriber and reposition all the other subscribers and invalidate ScrollPane.

```javascript
public function removeSubscriber(s:Subscriber): Void {
  for(var i= 0; i < subscriberList.length; i++) {
    if (Subscriber(subscriberList[i]).videoStream == s.videoStream) {
      subscriberList.removeItemAt(i);
    }
  }
  for (var i= 0; i < subscriberList.length; i++) {
    var positionX:Number = broadcaster._x + (subscriberList.length%4) * broadcaster._width;
    var positionY:Number = broadcaster._y + (broadcaster._height * Math.floor(subscriberList.length/4));
    var mc:Subscriber = Subscriber(subscriberList[i]);
    mc._x = positionX;
    mc._y = positionY;
  }
  s.removeMovieClip();
  _level0.instance1.scrollPane.invalidate();
}
```

Look into [Subscriber.as](https://github.com/marinalohova/red5-flash/blob/master/classes/org/red5/samples/livestream/videoconference/Subscriber.as). When the subscriber disconnects the stream fires an "unpublishNotify" event, that eventually makes a call to the removeSubscriber() function.

```javascript
public function subscribe(p_subscriptionID:String, p_connection:Connection):Void
{
  ...
  stream.addEventListener("unpublishNotify", Delegate.create(this, streamStop));
  ...
}

public function streamStop(evtObj:Object):Void
{
  videoPool.removeSubscriber(this);
  publish_video.clear();
  stream.close();
}
```

Finally open [VideoConference.as](https://github.com/marinalohova/red5-flash/blob/master/classes/org/red5/samples/livestream/videoconference/VideoConference.as). This is a controller class, the Red Queen of all the above classes! It manages all the incoming subscribing streams and the broadcasting stream. When your computer is ready to broadcast, the camera is up and the broadcasting stream received its id, VideoConference sends requests to get all the publishing streams to the url on the server and process them as the subscribers.

```javascript
private function configUI():Void
{
  ...
  videoPool.broadcaster.addEventListener("onSetID", this);
  ...
}

private function setID(p_id:Number, p_connection:Connection):Void
{
  //set local videoID
  videoID = Number(p_id);

  // set connection
  connection = p_connection;

  getStreams();
}

private function getStreams():Void
{
  connection.call("getStreams", this.result);
}
```

Since VideoPool with all the streams loads into the ScrollPane component now, VideoConference needs to be updated with the correct VideoPool reference:

```javascript
private var videoPool:VideoPool;
private var scrollPane:ScrollPane;
...
private function configUI():Void
{
  ...
  scrollPane.setStyle("borderStyle", "none");
  videoPool = VideoPool(scrollPane.content);

  videoPool.broadcaster.registerController(this);
  videoPool.broadcaster.addEventListener("connected", this);
  videoPool.broadcaster.addEventListener("disconnected", this);
  videoPool.broadcaster.addEventListener("onSetID", this);
}
```

We could wrap the last four lines in some kind of configUI() function on VideoPool, but haven’t I told you? Refactoring will be your homework assignment!

When the new subscriber shows up, we add him or her and update ScrollPane.

```javascript
private function processQue():Void
{
  if(streamQue.length <= 0)
  {
    clearInterval(si);
    return;
  }

  var id:Number = Number(streamQue.shift().split("_")[1]);

  videoPool.subscribe(id);

  scrollPane.invalidate();
}
```

Almost ready! Publish the swf file and copy to the website folder. If you want to re-compile ActionScript classes only, use [MTASC compiler](https://github.com/marinalohova/mtasc-mx/blob/master/bin/mtasc) and MX libraries from my [Github repo](https://github.com/marinalohova/mtasc-mx):

```bash
> cp videoConference.swf classes/videoConference.swf
> cd classes
> export PATH="$HOME/mtasc-mx/bin:$HOME/mtasc-mx/bin/std:$PATH"
> mtasc -version 8 -cp "." -swf videoConference.swf -mx org/red5/samples/livestream/videoConference/videoConference.as -v
> cp videoConference.swf $HOME/Sites/red5-hangout/videoConference.swf
```

Include into the webpage:

```javascript
<script type="text/javascript">
  swfobject.embedSWF("videoConference.swf", "participants", "100%", "100%", "7.0.0", "assets/expressInstall.swf", {}, { allowScriptAccess: "always" });
</script>
<div id="participants"></div>
```

### Stylish Spotlight

The “Spotlight” component is the larger video of the “talking” person that shows up when one of the smaller previews is clicked. simpleSubscriber.fla is the ideal base for this component:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/03/streaming-live-with-red5-media/image-5.jpeg" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/03/streaming-live-with-red5-media/image-5.jpeg"/></a></div>

Subscriber and Broadcaster will respond to the “click” event and call JavaScript function with the video stream name as a parameter. The video stream name is just a string like “videoStream_12” denoting the 12th stream accepted by “fitcDemo” application.

In [Broadcaster.as](https://github.com/marinalohova/red5-flash/blob/master/classes/org/red5/samples/livestream/videoconference/Broadcaster.as#L96):

```javascript
private function configUI():Void
{
  this.onRelease = function(){
    _global.tt('Broadcaster ' + this.videoStream + ' clicked.');
    if (ExternalInterface.available) {
      ExternalInterface.call("spotlight", this.videoStream);
    }
  }
}
```

In [Subscriber.as](https://github.com/marinalohova/red5-flash/blob/master/classes/org/red5/samples/livestream/videoconference/Subscriber.as#L108)

```javascript
public function configUI():Void
{
  this.onRelease = function() {
    ExternalInterface.call("spotlight",this.videoStream);
  }
};
```

JavaScript will embed the SimpleSubscriber clip and pass along the video stream name that should be played via flashvars.

On the page

```javascript
<script type="text/javascript">
  function spotlight(streamName) {
    swfobject.embedSWF("simpleSubscriber.swf", "spotlight", "100%", "100%", "7.0.0", "assets/expressInstall.swf", {"streamName":streamName});
  }
</script>
<div id="stage"><div id="spotlight"></div></div>
```

In SimpleSubscriber [Main.as](https://github.com/marinalohova/red5-flash/blob/master/classes/org/red5/samples/livestream/subscriber/Main.as):

```javascript
private var streamName:String;
...
private function configUI():Void
  {
    streamName = String(_level0.streamName);
    ...
  }
```
```javascript
private function connectionChange(evtObj:Object):Void
{
  if(evtObj.connected)
  {

    stream = new Stream(evtObj.connection);

    stream.play(streamName, -1);

    publish_video.attachVideo(stream);
  }
}
```

Publish [simpleSubsciber.swf](https://github.com/marinalohova/red5-flash/blob/master/classes/org/red5/samples/livestream/subscriber/Main.as) and place it into the website folder. To recompile the ActionScript part only:

```bash
> mtasc -version 8 -cp "." -swf simpleSubscriber.swf -mx org/red5/samples/livestream/subscriber/Main.as -v
> cp simpleSubscriber.swf $HOME/Sites/red5-hangout/simpleSubscriber.swf
```

By the way the -version 8 flag for mtasc was added specifically to compile ExternalInterface, otherwise, these libraries would not be found.

### Chat in the absence of Sound

One thing I really appreciate about the Google Hangout architecture is that it does not just make the whole page a bulky <embed> or <object> and lock everything into the external component. I love how they use the familiar and friendly JavaScript and HTML to add some interactive features. That’s why I decided to break the single VideoConference component into pieces as well and tie them together on a web page.

The original conference had its audio support commented out with the note about performance issues. Bummer! This will surely need to be addressed, but for now I decided to use the existing chat and make it separate. Create a blank document [chat.fla](https://github.com/marinalohova/red5-flash/blob/master/chat.fla) and drag Chat clip from the VideoConference Library to the stage.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/03/streaming-live-with-red5-media/image-6.jpeg" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/03/streaming-live-with-red5-media/image-6.jpeg"/></a></div>

Remove any reference to VideoConference and VideoPool from [Chat.as](https://github.com/marinalohova/red5-flash/blob/master/classes/org/red5/samples/livestream/videoconference/Chat.as), create its own GlobalObject and Connection and paste the sound settings from [VideoConference.as](https://github.com/marinalohova/red5-flash/blob/master/classes/org/red5/samples/livestream/videoconference/VideoConference.as):

```javascript
private var red5URI = "rtmp://192.168.0.5/fitcDemo";
...
public function configUI():Void
{
  streamID = Number(_level0.streamName.split("_")[1]);

  ...

  loadProfile("videoConference");

  var my_nc:Connection = new Connection();
  my_nc.connect(red5URI);

  chatID = "videoConferenceChat";
  connected = so.connect(chatID, my_nc, false);

  ...

  sndTarget = this.createEmptyMovieClip("sndTarget", this.getNextHighestDepth());
  snd = new Sound (sndTarget);
  snd.attachSound("newChatMessage");
  snd.setVolume(80);

  soundPlay._visible = false;
  soundMute.addEventListener("click", Delegate.create(this, updateMute));
  soundPlay.addEventListener("click", Delegate.create(this, updateMute));
  soundMute.tooltip = "Mute new chat sound";
  soundPlay.tooltip = "Un-mute new chat sound";
}
```

Initialize the chat in [Broadcaster.as](https://github.com/marinalohova/red5-flash/blob/master/classes/org/red5/samples/livestream/videoconference/Broadcaster.as#L154) after the stream is initialized:

```javascript
private function onSetID(evtObj:Object):Void
{
  ...
  ExternalInterface.call("chat", this.videoStream);
}
```

Publish or recompile:

```bash
> mtasc -version 8 -cp "." -swf chat.swf -mx org/red5/samples/livestream/videoConference/Chat.as -v
> cp chat.swf $HOME/Sites/red5-hangout/chat.swf
```

Add the chat to the web page:

```javascript
<script type="text/javascript">
function chat(streamName) {
  swfobject.embedSWF("chat.swf", "chat", "330px", "460px", "7.0.0", "assets/expressInstall.swf",
                     {"streamName": streamName });
}
</script>
<div id="chat" style="display:none">
</div>
```

And enjoy chatting with yourself for a while in different browser tabs:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/03/streaming-live-with-red5-media/image-7.jpeg" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/03/streaming-live-with-red5-media/image-7.jpeg"/></a></div>

### Final result

After a bit of styling and herding my test participants, here is what I got:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/03/streaming-live-with-red5-media/image-8.jpeg" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/03/streaming-live-with-red5-media/image-8.jpeg"/></a></div>

### Questions, questions

There are problems to be addressed yet.

First, there is no audio. It’s commented out in the original code with the note about performance issues. Silence may be golden, but the grimace-enhanced chat experience is totally not acceptable for production!

Second, the whole performance talk brings up the other important questions: How many subscribers can this setup handle? Is it possible to achieve the better video quality? Why is the video stream choppy at times?

Finally, every application needs a mobile presence. Will it be possible to port the client to mobile devices using AIR? How to port to iPads and iPhones?

The Flash source code in its entirety is located in my [GitHub repo](https://github.com/marinalohova/red5-flash). Please, keep in mind, that the code is not perfect, and the logic can be better organized between classes with event handlers. The demo application can be found [here](https://github.com/marinalohova/red5-hangout). MTASC compiler and MX libraries for compilation are available [here](https://github.com/marinalohova/mtasc-mx).

I would love to hear your feedback on this!
