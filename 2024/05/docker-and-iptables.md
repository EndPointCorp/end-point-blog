---
author: "Jeffry Johar"
title: "Docker and iptables"
date: 2024-05-15
featured:
  image_url: /blog/2024/05/docker-and-iptable/chains.webp
description: Introduction on how to use iptables to block access to Docker containers. 
tags:
- docker
- linux
- iptables
- Red Hat
---
![four-metal-poles-with-link-chain](/blog/2024/05/docker-and-iptables/chains.webp)

<!-- https://www.pexels.com/photo/four-metal-poles-with-link-chains-754113/ -->

Docker utilizes iptables for its networking and routing. Blocking and accepting connections to the running containers on a host might be tricky at first if we are not aware of where Docker puts its chains. Docker chains are all located in the iptables FORWARD chain. Within this chain, Docker provides a convenient chain named DOCKER-USER for users to add their custom rules.

One common mistake is attempting to block Docker Containers at the iptables INPUT chain, which will not work. This is because Docker does not pass through the INPUT chain; it only passes through the FORWARD chain. The following diagram illustrates a simplified chains traversal of Docker containers.

![Docker iptables traversal](/blog/2024/05/docker-and-iptables/traversal.webp)

Working Examples of iptables Rules

Below are a few working examples of iptables rules that can serve as references. These rules will be applied to the DOCKER-USER chain. It's important to note that the DOCKER-USER chain comes after the PREROUTING chain and FORWARD chain, so we'll need to use iptables conntrack extension for getting the information about source addresses and host ports. iptables conntrack extension allows iptables to track the state of network connections passing through the system. This tracking capability enables iptables to make decisions based on the state of connections.

###  1. Blocking Specific Port and Allowing Access for a Specific IP

The following example allows only the IP address 192.168.0.1 to access port 8080 on this host, while blocking access for all other IPs. We'll use the network interface eth0.

```plain
iptables -A DOCKER-USER -i eth0 -s 192.168.0.1 -p tcp -m conntrack --ctorigdstport 8080 --ctdir ORIGINAL -j ACCEPT
iptables -I DOCKER-USER -i eth0 -p tcp -m conntrack --ctorigdstport 8080 --ctdir ORIGINAL -j DROP
```

**Explanation:**

- The first rule allows incoming TCP traffic (-p tcp) on port 8080 (--ctorigdstport 8080) from the source IP address 192.168.0.1 (-s 192.168.0.1).
- The second rule drops all other incoming TCP traffic on port 8080.

### 2. Blocking All Connections Except for a Specific IP

This example blocks all incoming connections to this host but allows access for IP address 192.168.0.1. We'll again use the network interface eth0.
```plain
iptables -I DOCKER-USER -i ext_if ! -s 192.168.0.1 -j DROP
```

**Explanation:**
- This rule drops all incoming traffic (-j DROP) on interface eth0 (-i eth0) except for traffic originating from IP address 192.168.0.1 (! -s 192.168.0.1).

The examples above demonstrate how to control access to specific ports and IP addresses using iptables rules. Ensure to adjust the IP addresses, port numbers, and network interfaces according to your specific requirements. 

### 3. To make the rules permanent
To ensure the added iptables rules are permanent, we need to place them where they can be restored upon boot. On a Red Hat-based Linux system, this location is the /etc/sysconfig/iptables file.
```plain
-N DOCKER-USER
-A DOCKER-USER -i eth0 -p tcp -m conntrack --ctorigdstport 8080 --ctdir ORIGINAL -j DROP
```

**Explanation:**
- The first line defines the DOCKER-USER chain (-N DOCKER-USER)
- The second line appends the rule to drop all incoming TCP traffic on port 8080

In conclusion, understanding how to configure iptables for Docker containers is crucial for ensuring network security and efficient traffic management. By grasping the concepts discussed in this blog post, you can better safeguard your Dockerized environments and optimize network performance. Keep exploring and experimenting with iptables to further enhance your Docker deployments.


