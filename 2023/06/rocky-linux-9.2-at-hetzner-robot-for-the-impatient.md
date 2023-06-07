---
title: "Rocky Linux 9.2 at Hetzner Robot for the impatient"
author: "Jeffry Johar"
date: 2023-06-07
featured:
  image_url: https://www.pexels.com/photo/17122631/
tags:
- Heztner
- Rocky Linux 9
- Cloud Computing
---

### Introduction
Rocky Linux is a free and open-source community-driven operating system designed to be a drop-in replacement for CentOS. CentOS was previously a popular Linux distribution that was based on the same source code as Red Hat Enterprise Linux (RHEL) but offered as a free alternative with community support.

As of to date ( 6th June 2023) , Rocky Linux 9 is not supported by Hetzner Robot to install at its dedicated physical servers. Despite the installimage indicating support, attempting to install it will result in the following error: “We do not yet support rockylinux 9.1 on EFI systems”

If you are looking for a workaround, consider installing Rocky Linux 8 and upgrading it to version 9. While it's important to note that this installation approach is still in the testing phase and hasn't undergone comprehensive testing, I'll provide you with the following step-by-step instructions to accomplish it.

### Provisioning the Server:
To get started, follow the guide in the following link  to order and provision a server from Hetzner Robot. 
https://docs.hetzner.com/robot/dedicated-server/general-information/root-server-hardware


### Enabling Rescue Mode:

1. Access the Hetzner Robot interface and navigate to the "Rescue" tab.
2. Choose Linux as the rescue media and select the SSH option to access the server. Alternatively, use the generated root password.
3. Click the "Activate rescue system" button.

