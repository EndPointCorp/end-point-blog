---
author: Matt Vollrath
gh_issue_number: 721
tags: liquid-galaxy, sysadmin
title: Using cec-client to Control HDMI Devices
---



Maintaining the horde of computers it takes to run [Liquid Galaxies](https://liquidgalaxy.endpoint.com/) in all corners of the globe is a big job. As of November of 2012, we’re monitoring 154 computers at permanent installations in addition to keeping our development and testing systems running like the well-oiled machines we want them to be. All that fluff aside, end users never see the fruits of our labor unless the TVs are working as expected! Without methods for getting and setting the status of displays, we are completely blind to what people are actually experiencing in front of a Liquid Galaxy.

Enter [HDMI-CEC](https://en.wikipedia.org/wiki/HDMI#CEC). CEC is a protocol that allows HDMI-connected devices to control each other in various ways. It has a set of standard features that make it easy for home users with a stack of DVD players or TiVos or other devices to change the active source, put everything on standby, control the volume, and some other handy tricks.

We typically use Samsung TVs which support CEC under the trade name “Anynet+”. To interface between computers and TVs, we use [Pulse Eight’s USB-CEC adapters](https://www.pulse-eight.com/store/products/104-usb-hdmi-cec-adapter.aspx) which, in conjunction with [libCEC](http://libcec.pulse-eight.com/), give us a command line interface for arbitrary commands to the TV.

libCEC is available on apt for Ubuntu users:

```nohighlight
$ sudo apt-get install cec-utils
```

Once installed, we have access to all kinds of fun commands. [CEC-O-Matic](http://www.cec-o-matic.com/) is a great reference, and will even build command strings for you! Just bear in mind that CEC-O-Matic output has colons separating the octets, while cec-client’s “tx” expects spaces.

The syntax of a libCEC “tx” command is like this:

```nohighlight
$ echo 'tx <src-dst> <cmd> <args...>' | cec-client <device>
```

The first octet of the command will be the source and destination. The P8 CEC adapter uses device 1 by default, which is “Recording 1”, and a TV is always 0, so when querying the TV our first octet will be “10”.

The second octet is a command code. Let’s say we want to know what language the TV’s menu is set to. On CEC-O-Matic you can find this in the “Supporting Features” tab, “System Information” section, “Get Menu Language,” which indicates that the message ID is “91”.

Arguments are situational, and many commands will not require any arguments. We’ll talk about arguments soon.

The device can be found with the ever-handy:

```nohighlight
$ cec-client -l
Found devices: 1

device:              1
com port:            /dev/ttyACM0
firmware version:    2
firmware build date: Thu Aug  2 09:40:28 2012 +0000
type:                Pulse-Eight USB-CEC Adapter
```

We want to use that COM port, “/dev/ttyACM0”.

For example, let’s query the menu language of the TV connected to the first CEC adapter.

```nohighlight
$ echo 'tx 10 91' | cec-client /dev/ttyACM0
[ . . . ]
DEBUG:   [             492] << requesting power status of 'TV' (0)
TRAFFIC: [             492] << 10:8f
TRAFFIC: [             638] >> 01:90:00
DEBUG:   [             638] >> TV (0) -> Recorder 1 (1): report power status (90)
DEBUG:   [             638] TV (0): power status changed from 'unknown' to 'on'
DEBUG:   [             638] expected response received (90: report power status)
waiting for input
TRAFFIC: [             639] << 10:91
TRAFFIC: [             842] >> 0f:32:65:6e:67
DEBUG:   [             842] >> TV (0) -> Broadcast (F): set menu language (32)
DEBUG:   [             842] TV (0): menu language set to 'eng'
```

Here you see that, after a bunch of other cruft is resolved, the adapter requests the power status of the TV (10:8f) and the TV reports that is is “on” (01:90:00). This seems to be the first action of any query. Now, since we received an expected response, it sends the menu language query (10:91). In response the TV sends `0f:32:65:6e:67`. What does this mean?

The first octet “0f” means the source is the TV (0) and the destination is “broadcast to all devices in the signal path” (f). The second octet, “32”, is the command code for “Set Menu Language”. The next three octets “65:6e:67” are [ASCII](https://en.wikipedia.org/wiki/ASCII) code for “eng” which is the [ISO 639-2 Code](https://www.loc.gov/standards/iso639-2/php/code_list.php)  for “English.” So, instead of just telling us what the menu language is, the TV is responding by setting all devices to its language.

In the next two DEBUG lines it reports what I just explained.

At this point, cec-client is idling. Use Ctrl-C to end the process gracefully.

What if we want to change the power setting of the TV? In this case, libCEC has built-in commands to make it a little more intuitive.

```nohighlight
$ echo 'standby 0' | cec-client -s /dev/ttyACM0
$ echo 'on 0' | cec-client -s /dev/ttyACM0
```

The first command will put the TV on standby, the second will turn it on. In this case, we don’t need to specify the command source, only the destination of TV (0). Also notice that we used the -s argument to cec-client and it exited as soon as it sent the command. -s is short for --single-command, which sends a command and then exits. We didn’t use -s in the above menu language query because it causes cec-client to exit before we get the response back from the TV! For automated cec-client commands, such as automatic screen sleeping at night, -s is quite useful since the process doesn’t “hang” after execution.

These are the basics of cec-client. For more information on the app itself, you can consult the cec-client manpage or visit the [libcec project on GitHub](httpss://github.com/Pulse-Eight/libcec).

Happy hacking!


