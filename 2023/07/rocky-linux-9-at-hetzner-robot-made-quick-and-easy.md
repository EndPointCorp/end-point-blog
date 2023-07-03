---
title: "Rocky Linux 9 at Hetzner Robot Made Quick and Easy"
author: "Jeffry Johar"
github_issue_number: 1986
date: 2023-07-01
tags:
- cloud
- hosting
- linux
- sysadmin
- redhat
---

![Malaysian Mango Pickles](/blog/2023/06/rocky-linux-9-at-hetzner-robot-made-quick-and-easy/mangopickles.webp)<br>
Image [by Jeffry Johar](https://www.pexels.com/photo/mango-pickles-17315505/)

### Introduction

In [my last blog post](/blog/2023/06/rocky-linux-9-at-hetzner-robot-for-the-impatient/), I shared my experience of installing Rocky Linux 8 on my Hetzner robot server and subsequently upgrading it to Rocky Linux 9. However, Rocky Linux project manager [Brian Clemens](https://github.com/brianclemens) commented that this method is not recommended and suggested using a boot kickstart for an automated installation. Thanks, Brian! Despite my attempts to utilize kickstart, I encountered difficulties in booting my NVMe disk. During this process, I discovered another workaround for installing Rocky 9 using the installimage script. It's important to note that this method is also experimental, just like the previous one.

### The Steps

1. Access the rescue mode (refer to [my previous blog post](/blog/2023/06/rocky-linux-9-at-hetzner-robot-for-the-impatient/#enabling-rescue-mode) if you need guidance).
2. Copy the existing Rocky Linux 9 image to Rocky Linux 8 and place it in the root directory by executing the following command:

    ```plain
    cp /root/images/Rocky-91-amd64-base.tar.gz /root/Rocky-87-amd64-base.tar.gz
    ```

The filename should adhere to the required naming convention for the installimage script to function correctly.

3. Launch the `installimage` and select the Custom Image option.

    ![installimage](/blog/2023/06/rocky-linux-9-at-hetzner-robot-made-quick-and-easy/installimage.webp)

4. Configure the disk settings as required, and at the end of the script, select the image accordingly.

    ```bash
    IMAGE /root/Rocky-87-amd64-base.tar.gz
    ```

5. To save the configuration file, simply press F10, allowing the installation process to resume uninterrupted. You may encounter a warning indicating the absence of an image signature, which is perfectly normal. Once the installation is finished, proceed to reboot the system.

    ![installation completes with no error](/blog/2023/06/rocky-linux-9-at-hetzner-robot-made-quick-and-easy/complete.webp)

6. After the system restarts, you will have access to Rocky Linux 9. The installation will provide you with some fairly recent point-release of Rocky Linux, such as 9.1, but as always you need to update to the latest packages with `dnf update`.

### Conclusion

That's all, folks! This second method is much easier compared to the first one, as it swiftly takes you to Rocky 9 without any complications.
