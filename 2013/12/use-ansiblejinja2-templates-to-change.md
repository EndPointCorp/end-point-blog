---
author: Emanuele “Lele” Calò
title: Use Ansible/Jinja2 templates to change file content based on target OS
github_issue_number: 901
tags:
- devops
- ansible
- redhat
- debian
- linux
- ssh
date: 2013-12-19
---

In the End Point hosting team we really love automating repetitive tasks, especially when it involves remembering many little details which can over time be forgotten, like differences of *coreutils* location between some versions of Ubuntu (Debian), CentOS (Red Hat) and OpenBSD variants.

In our environment we bind the backup SSH user authorized_keys entry to a custom command in order to have it secured by being, among other aspects, tied to a specific rsync call.

So in our case the content of our **CentOS** authorized_keys would be something like:

```bash
command="/bin/nice -15 /usr/bin/rsync --server --daemon .",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty ssh-rsa AAAB3[...]Q== endpoint-backup
```

Sadly that’s only true for CentOS systems so that if you want to **automate the distribution of authorized_keys** (as we’ll show in another post) to different Linux distributions (like **Ubuntu**) you may need to tweak it to comply to the new standard “/usr/bin” location, which will be eventually adopted by all new Linux versions overtime.. RHEL 7.x onward included.

To do the OS version detection we decided to use an **Ansible**/**Jinja2** template by placing the following line in the Ansible task:

```bash
- name: Deploy /root/.ssh/authorized_keys
  template: src=all/root/.ssh/authorized_keys.j2
            dest=/root/.ssh/authorized_keys
            owner=root
            group=root
            mode=0600
```

And inside the actual file place a slightly modified version of the line above:

```bash
command="{% if ansible_os_family != "RedHat" %}/usr{% endif %}/bin/nice -15 /usr/bin/rsync --server --daemon .",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty ssh-rsa AAAB3[...]Q== endpoint-backup"
```

So that if the target OS is not part of the “RedHat” family it will add the “/usr” in front of the “/bin/nice” absolute path.

Easy peasy, ain’t it?

Now go out there and exploit this feature to all your needs.
