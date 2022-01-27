---
title: "Using SSH tunnels to get around network limitations"
author: Zed Jensen
tags:
- development
- networking
- sysadmin
- ssh
- tips
date: 2022-01-26
github_issue_number: 1827
---

![Cliff dwelling in Arizona](/blog/2022/01/using-ssh-tunnels-network-limitations/banner.jpg)

<!-- Picture by Zed Jensen, 2020 -->

SSH is an extremely useful way to use computers that you aren't near physically. However, it can also be used to overcome some unique networking challenges, particularly those where one computer needs to connect to another in an unorthodox way. This post will show a couple uses of SSH tunnels that have come in handy for me personally.

### Serving content without a public IP

In the past, [I wrote](/blog/2020/07/automating-minecraft-server/) about maintaining a Minecraft server to play on with my friends. In that post, I was dealing with being physically separated from the physical server I intended to use, but once I got that machine back, I realized that I still had an issue. My ISP didn't support port forwarding, meaning that I couldn't connect to my server from outside my home network, and even if I could, the public IP I was assigned changed regularly. One solution I found was to use a reverse SSH tunnel to forward traffic from a publicly-visible virtual server to my local server.

To set this up, you just need your local machine and a server with a publicly visible IP address. I used a virtual machine from [UpCloud](https://upcloud.com/), which costs $5 per month, but you could use any other server, as long as it has its own IP. Setup is fairly simple.

First, on the local machine, we create a new SSH key just for this connection. This key serves as a way to authenticate without a password (but without using a personal SSH key).

```plain
ssh-keygen -t ed25519 -f ~/.ssh/ed25519 -q -N ""
```

Next, we create a new user `proxy` on the server. Creating a user specifically for this purpose lets us make sure that our password-free SSH key doesn't give access to any sensitive data on the remote server.

```plain
useradd -m proxy
```

Then, we add the public key generated earlier to `authorized_keys` in the new proxy user's `.ssh` folder.

Finally, on the local machine, we run the following command. Here's what each part does:

- `-f` tells ssh to run in the background
- `-N` doesn't run a command on the remote host, which is perfect since we're just forwarding traffic.
- `-i` specifies the SSH key we're using, 
- `-R` is a bit more complicated. `0.0.0.0:25565` specifies which traffic to intercept on the remote host and `localhost:25565` where to forward it to. Note that `25565` is a TCP port number (UDP isn't supported by SSH out of the box) and will vary based on the application you're using.
- `proxy@myserver` is the user and hostname of the remote server.

```plain
ssh -fN -i /home/zed/.ssh/id_ed25519 -R 0.0.0.0:25565:localhost:25565 proxy@myserver
```

And that's it! The reverse tunnel will now forward traffic from our publicly visible server to the specified port to our machine.

Another good use for this setup is when you have an IPv4 address at the edge of a network but only IPv6 internally (this is becoming more common as IPv4 addresses become more scarce). Also note that for more permanent situations, a VPN like WireGuard or OpenVPN might be a better choice than an SSH tunnel; however, for lower-volume traffic SSH works just fine.

### Splitting a Docker app between multiple machines

There are many other uses for SSH tunnels. One of our clients has an application with a lot of different moving parts that all need to communicate with each other for the entire application to function. For instance, there's a database container, a container for part of the backend that needs CUDA support, and several others, in addition to a React frontend. Applications like this can of course slow your computer down quite a bit. What if you only need to make modifications to the frontend or another light part of the application? I asked around and found that a couple of coworkers had already found a workaround.

The solution is simple but effective - if you have another computer available (in my case, a desktop that you don't usually use for work), you can run the performance-intensive containers on that machine. This allows you to work on the lighter parts of the application without experiencing slowdown (or fan noise, or other issues like that) on your laptop.

Because the different parts of the application were already using Docker, it wasn't hard to run the different pieces on separate machines, but they needed to know to talk to each other across the network. SSH tunnels let us do that without modifying our Docker configuration!

For the rest of this example I'll refer to the two computers in this scenario as "the laptop" and "the desktop", running the frontend and backend portions respectively, but keep in mind that you could do this with other setups as well.

#### 1. Collecting some info

Before we can set everything up, we need to know which ports our application is communicating on. Examining the Dockerfiles for the backend containers in this application, I found that it was using ports 9933, 9934, and 10004. Normally, our frontend application would be communicating with these containers by talking to `http://localhost:9933` and so on, but once we know which ports it's going to use, we can set up SSH to forward the traffic to our desktop machine instead.

The other important piece of info we'll need is the IP address of our desktop machine. In this case, mine is `192.168.0.55`, so we'll use that.

#### 2. Setting up the SSH config

The most important step to making the different machines talk to each other is going to be in our SSH config, `~/.ssh/config`.

We'll start by coming up with an alias hostname for our desktop, like `backend`, and creating a section for it in our config file. We then add a `LocalForward` line for each port we want to forward like so:

```plain
Host backend
	HostName 192.168.0.55
	User zed
	ForwardAgent yes
	LocalForward 9933 127.0.0.1:9933
	LocalForward 9934 127.0.0.1:9934
	LocalForward 10004 127.0.0.1:10004
```

#### 3. Connecting the computers

For the different parts of the application to talk to each other, there needs to be an active SSH connection. I usually open an SSH connection like normal (make sure to use the hostname we set in step 2!), start a tmux session, and then run the backend portions of the app in the tmux session:

```sh
[zed@laptop ~]$ ssh desktop-machine
[zed@desktop ~]$ get-stuff-started
```

However, if you'd prefer, you can also open a reverse SSH connection that will run in the background until killed:

```sh
[zed@laptop ~]$ ssh -fN desktop-machine
[zed@laptop ~]$
```

#### 4. Test it!

Now that we've got an SSH session running to forward traffic to the desktop machine, you can try spinning up the React app and see if it connects properly.

### Conclusion

There are many other uses for SSH tunnels. Feel free to let us know in the comments how you've used them!

