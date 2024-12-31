---
author: "Jeffry Johar"
title: "Docker and iptables"
date: 2024-06-12
featured:
  image_url: /blog/2024/06/docker-and-iptable/chains.webp
description: Introduction on how to use iptables to block access to Docker containers. 
github_issue_number: 2051
tags:
- docker
- linux
- iptables
- redhat
---

![Four metal poles connected by chains with padlocks at the center stand against the sea, with a blue-orange sunset above.](/blog/2024/06/docker-and-iptables/chains.webp)

Photo by [Egor Kamelev](https://www.pexels.com/@ekamelev/) from [Pexels](https://www.pexels.com/photo/four-metal-poles-with-link-chains-754113/).

Docker utilizes iptables for its networking and routing. Blocking and accepting connections to the running containers on a host might be tricky at first if we are not aware of where Docker puts its chains. Docker chains are all located in the iptables FORWARD chain. Within this chain, Docker provides a convenient chain named DOCKER-USER for users to add their custom rules.

One common mistake is attempting to block Docker Containers at the iptables INPUT chain, which will not work. This is because Docker does not pass through the INPUT chain, it only passes through the FORWARD chain. The following diagram illustrates a simplified chains traversal of Docker containers.

![Docker iptables traversal. A cloud shape labeled "network" sits at the top of a block diagram. An arrow points down from it to a block reading "prerouting". The "PREROUTING" block points down at a green block reading "routing decision". This block has two outward arrows, one to the left and one to the right. The arrow to the left points at a block labeled "INPUT" which itself points down at several stacked blocks labeled "other chains...". The arrow to the right points at a block reading "FORWARD", which points down to a block labeled "DOCKER-USER", which points down to a block labeled "DOCKER", which points down to a block labeled "other chains..."](/blog/2024/06/docker-and-iptables/traversal.webp)

Below are a few working examples of iptables rules that can serve as references. These rules will be applied to the DOCKER-USER chain. It's important to note that the DOCKER-USER chain comes after the PREROUTING chain and FORWARD chain, so we'll need to use the iptables conntrack module for getting the information about source addresses and host ports. iptables conntrack extension allows iptables to track the state of network connections passing through the system. This tracking capability enables iptables to make decisions based on the state of connections.

###  1. Blocking Specific Port and Allowing Access for a Specific IP

The following example allows only the IP address 192.168.0.1 to access port 8080 on this host, while blocking access for all other IPs. We'll use the network interface eth0.

```plain
iptables -A DOCKER-USER -i eth0 -s 192.168.0.1 -p tcp -m conntrack --ctorigdstport 8080 --ctdir ORIGINAL -j ACCEPT
iptables -I DOCKER-USER -i eth0 -p tcp -m conntrack --ctorigdstport 8080 --ctdir ORIGINAL -j DROP
```

**Explanation:**

- The first rule allows incoming TCP traffic (`-p tcp`) on port 8080 (`--ctorigdstport 8080`) from the source IP address 192.168.0.1 (`-s 192.168.0.1`).
- The second rule drops all other incoming TCP traffic on port 8080.

### 2. Blocking All Connections Except for a Specific IP

This example blocks all incoming connections to this host but allows access for IP address 192.168.0.1. We'll again use the network interface eth0.
```plain
iptables -I DOCKER-USER -i ext_if ! -s 192.168.0.1 -j DROP
```

**Explanation:**
- This rule drops all incoming traffic (`-j DROP`) on interface eth0 (`-i eth0`) except for traffic originating from IP address 192.168.0.1 (`! -s 192.168.0.1`).

The examples above demonstrate how to control access to specific ports and IP addresses using iptables rules. Make sure to adjust the IP addresses, port numbers, and network interfaces according to your specific requirements.

### 3. To make the rules permanent

To ensure the added iptables rules are permanent, we need to place them where they can be restored upon boot. On a Red Hat-based Linux system, this location is the `/etc/sysconfig/iptables` file.

```plain
-N DOCKER-USER
-A DOCKER-USER -i eth0 -p tcp -m conntrack --ctorigdstport 8080 --ctdir ORIGINAL -j DROP
```

**Explanation:**
- The first line defines the DOCKER-USER chain (`-N DOCKER-USER`)
- The second line appends the rule to drop all incoming TCP traffic on port 8080

Understanding how to configure iptables for Docker containers is crucial for ensuring network security and efficient traffic management. Using these configurations can safeguard Dockerized environments and optimize network performance. Keep exploring and experimenting with iptables to further enhance your Docker deployments.
