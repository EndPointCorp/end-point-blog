---
author: "Jeffry Johar"
title: "Ansible tutorial with AWS EC2"
github_issue_number: 1888
date: 2022-08-11
featured:
  image_url: /blog/2022/08/ansible-tutorial-with-aws-ec2/wheel.webp
description: Ansible is a tool to manage multiple remote systems from a single command center. This article covers how to use Ansible to manage multiple EC2 instances.
tags:
- ansible
- aws
- linux
- sysadmin
---

![A ferris wheel lit up by red lights at night](/blog/2022/08/ansible-tutorial-with-aws-ec2/wheel.webp)<br>
Photo by David Buchi

Ansible is a tool to manage multiple remote systems from a single command center. In Ansible, the single command center is known as the control node and the remote systems to be managed are known as managed nodes. The following describes the 2 nodes:

1. Control node:

    - The command center where Ansible is installed.
    - Supported systems are Unix and Unix-like (Linux, BSD, macOS).
    - Python and sshd are required.
    - Remote systems to be managed are listed in a YAML or INI file called an inventory.
    - Tasks to be executed are defined in a YAML file called a playbook.

2. Managed node:

    - The remote systems to be managed.
    - Supported systems are Unix/Unix-like, Windows, and Appliances (eg: Cisco, NetApp).
    - Python and sshd are required for Unix/Unix-like.
    - PowerShell and WinRM are required for Windows.

In this tutorial we will use Ansible to manage multiple EC2 instances. For simplicity, we are going to provision EC2 instances in the AWS web console. Then we will configure one EC2 as the control node that will be managing multiple EC2 instances as managed nodes.

### Prerequisites

For this tutorial we will need the following from AWS:

- An active AWS account.
- EC2 instances with Amazon Linux 2 as the OS.
- AWS Keys for SSH to access control node and managed nodes.
- Security group which allows SSH and HTTP.
- A decent editor such as Vim or Notepad++ to create the inventory and the playbook.
 
### EC2 Instances provisioning

The following are the steps to provision EC2 instances with the AWS web console. 

1. Go to AWS Console → EC2 → Launch Instances.
2. Select the Amazon Linux 2 AMI.
3. Select a key pair. If there are no available key pairs, please create one according to [Amazon's instructions](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html).
4. Allow SSH and HTTP.
5. Set Number of Instances to 4.
6. Click Launch Instance.

![AWS web console, open to the "Instances" tab in the toolbar. This is circled and pointing to the table column starting with "Public IPv4..."](/blog/2022/08/ansible-tutorial-with-aws-ec2/ansible03-ec2.webp)

### Ansible nodes and SSH keys

In this section we will gather the IP addresses of EC2 instances and set up the SSH keys. 

1. Go to AWS Console → EC2 → Launch Instances.
2. Get the Public IPv4 addresses.
3. We will choose the first EC2 to be the Ansible control node and the rest to be the managed nodes:

    - control node: 13.215.159.65
    - managed nodes: 18.138.255.51, 13.229.198.36, 18.139.0.15


![AWS web console, again open to the Instances tab, with the Public IPv4 column circled. A green banner says that the EC2 instance was successfully started, followed by a long ID](/blog/2022/08/ansible-tutorial-with-aws-ec2/ansible-ng02.webp)

Login to the control node using our key pair. For me, it is `kaptenjeffry.pem`.

```plain 
ssh -i kaptenjeffry.pem ec2-user@13.215.159.65
```

Open another terminal and copy the key pair to the control node

```plain
scp -i kaptenjeffry.pem kaptenjeffry.pem ec2-user@13.215.159.65:~/.ssh
```

Go back to the control node terminal. Try to log in from the control node to one of the managed nodes by using the key pair. This is to ensure the key pair is usable to access the managed nodes.

```plain
ssh -i .ssh/kaptenjeffry.pem ec2-user@18.138.255.51
```

Register the rest of the managed nodes as known hosts to the control nodes, in bulk:

```plain
ssh-keyscan -t ecdsa-sha2-nistp256 13.229.198.36 18.139.0.15 >> .ssh/known_hosts
```

### Ansible Installation and Configuration

In this section we will install Ansible in the control node and create the inventory file.

1. In the control node, execute the following commands to install Ansible:

    ```plain
    sudo yum update
    sudo amazon-linux-extras install ansible2
    ansible --version
    ```

    Where:

    - `yum update` updates all installed packages using the yum package manager,
    - `amazon-linux-extras install` installs Ansible, and
    - `ansible --version` checks the installed version of Ansible.

2. Create a file named `myinventory.ini`. Insert the IP addresses that we identified earlier to be the managed nodes in the following format:

```ini
[mynginx]
red ansible_host=18.138.255.51
green ansible_host=13.229.198.36
blue ansible_host=18.139.0.15
```

Where:

- `[mynginx]` is the group name of the managed nodes,
- `red`, `green`, and `blue` are the aliases of each managed node, and
- `ansible_host=x.x.x.x` sets the IP Address each managed node.

`myinventory.ini` is a basic inventory file in a INI format. An inventory file could be either in INI or YAML format. For more information on inventory see the [Ansible docs](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html).

### Ansible modules and Ansible ad hoc commands

Ansible modules are scripts to do a specific task at managed nodes. For example, there are modules to check availability, copy files, install applications, and lots more. To get the full list of modules, you can check the official [Ansible modules page](https://docs.ansible.com/ansible/2.9/modules/list_of_all_modules.html).

A quick way to use Ansible modules is with an ad hoc command. Ad hoc commands use the `ansible` command-line interface to execute modules at the managed nodes. The usage is as follows:

```plain
ansible <pattern> -m <module> -a "<module options>" -i <inventory>
```

Where:

- `<pattern>` is the IP address, hostname, alias or group name,
- `-m module` is name of the module to be used,
- `-a "<module options>"` sets options for the module, and
- `-i <inventory>` is the inventory of the managed nodes.

#### Ad hoc command examples

The following are some example of Ansible ad hoc commands:

`ping` checks SSH connectivity and Python interpreter at the managed node. To use the `ping` module against the `mynginx` group of servers (all 3 hosts: red, green, and blue), run:

```plain
ansible mynginx -m ping -i myinventory.ini
```

![Sample output of ping. Several green blocks of JSON show successful ping responses](/blog/2022/08/ansible-tutorial-with-aws-ec2/ansible04-ping-all.webp)

`copy` copies files to a managed node. To copy a text file (`/home/ec2-user/hello.txt` in our test case) from the Control node to `/tmp/` at all managed nodes in the `mynginx` group, run:

```plain
ansible mynginx -m copy \
-a 'src=/home/ec2-user/hello.txt dest=/tmp/hello.txt' \
-i myinventory.ini
```

`shell` executes a shell script at a managed node. To use module shell to execute `uptime` at all managed nodes in the `mynginx` group, run:

```plain
ansible mynginx -m shell -a 'uptime' -i myinventory.ini
```

### Ansible playbooks

Ansible playbooks are configuration files in a YAML format that tell Ansible what to do. A playbook executes its assigned tasks sequentially from top to bottom. Tasks in playbooks are grouped by a block of instructions called a play. The following diagram shows the high level structure of a playbook:

<p align="center">
  <img alt="An outer box labeled 'Playbook' contains two smaller boxes. The first is labeled 'Play 1', the second is labeled 'Play 2'. They contain stacked boxes similar to each other. The first box is a lighter color than the others, labeled 'Hosts 1 (or Hosts 2, for the 'Play 2' box)'. The others are labeled 'Task 1', 'Task 2', and after an ellipsis 'Task N'." src="/blog/2022/08/ansible-tutorial-with-aws-ec2/high-level-playbook.webp" width="400" />
</p>

Now we are going to use a playbook to install Nginx at our three managed nodes as depicted in the following diagram:

![At the left, a box representing a control node, with the Ansible logo inside. Pointing to the Ansible logo inside the control node box are flags reading "playbook" and "inventory". The control node box points to three identical "managed node" boxes, each with the Nginx logo inside.](/blog/2022/08/ansible-tutorial-with-aws-ec2/ansible01.webp)

Create the following YAML file and name it `nginx-playbook.yaml`. This is a playbook with one play that will install and configure Nginx service at the managed node. 

```yaml
---
- name: Installing and Managing Nginx Server 
  hosts: mynginx   
  become: True
  vars:
    nginx_version: 1
    nginx_html: /usr/share/nginx/html
    user_home: /home/ec2-user
    index_html: index.html
  tasks:
    - name: Install the latest version of nginx
      command: amazon-linux-extras install nginx{{ nginx_version }}=latest -y

    - name: Start nginx service
      service:
        name: nginx
        state: started

    - name: Enable nginx service
      service:
         name: nginx
         enabled: yes
    - name: Copy index.html to managed nodes
      copy:
        src:  "{{ user_home }}/{{ index_html }}"
        dest: "{{ nginx_html }}"
```

Where:

- `name` (top most) is the name of this play,
- `hosts` specifies the managed nodes for this play,
- `become` says whether to use superuser privilege (sudo for Linux),
- `vars` defines variables for this play,
- `tasks` is the start of the task section,
- `name` (under task section) specifies the name of each task, and
- `name` (in a `service` section) specifies the name of a module.

Let's try to execute this playbook. Firstly we need to create the source `index.html` to be copied to managed nodes.

```plain
echo 'Hello World!' > index.html
```

Execute `ansible-playbook` against our playbook. Just like the ad hoc command, we need to specify the inventory with the `-i` switch.

```plain
ansible-playbook nginx-playbook.yaml -i myinventory.ini
```

![A shell with the results of the ansible-playbook command above](/blog/2022/08/ansible-tutorial-with-aws-ec2/ansible-playbook-run.webp)

Now we can `curl` our managed nodes to check on the Nginx service and the custom `index.html`.

```plain
curl 18.138.255.51
curl 13.229.198.36
curl 18.139.0.15
```

<p align="center">
<img alt="The output of each curl command above, with the responses being identical: 'Hello World!'" src="/blog/2022/08/ansible-tutorial-with-aws-ec2/ansible-ng10.webp" width="600" />
</p>

### Conclusion

That’s all, folks. We have successfully managed EC2 instances with Ansible. This tutorial covered the fundamentals of Ansible to start managing remote servers.

Ansible rises above its competitors due to its simplicity of its installation, configuration, and usage. To get further information about Ansible you may visit its [official documentation](https://docs.ansible.com/ansible/latest/getting_started/index.html).
