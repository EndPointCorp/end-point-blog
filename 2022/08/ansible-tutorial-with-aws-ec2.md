---
author: "Jeffry Johar"
title: "Ansible tutorial with AWS EC2"
date: 2022-08-04
tags:
- ansible
- aws
- ec2
- amazon linux
---
![A ferris wheel](/blog/2022/08/ansible-tutorial-with-aws-ec2/wheel.webp)
Photo by David Buchi


### Introduction
Ansible is a tool to manage multiple remote systems from a single command center. In Ansible environment, the single command center is known as Control Node and the remote systems to be managed is known as Managed Node. The following tables describe about the 2 nodes:

| # | Ansible Node | Remarks |
|---|--------------|------------|
| 1 | Control Node | - The command center were Ansible is installed<br> - Supported systems are Unix and Unix Like ( Linux, BSD , MacOS )<br> - Python and sshd are required<br> - Remote systems to be managed are listed in a YAML or INI file called Inventory<br> - Tasks to be executed are defined in a YAML file called Playbook  |
| 2 | Managed Node | - The remote systems to be managed<br> - Supported Unix/Unix like, Windows and Appliances ( eg: Cisco, Netapp )<br> - Python and sshd are required for Unix/Unix like<br> - Powershell and WinRM are required for Windows |

In this  tutorial we will use Ansible to manage multiple EC2 instances. For simplicity we are going to provision EC2 instances by AWS web console. Then we will configure one EC2 as the Control Node that will be managing multiple EC2 instances as Managed Nodes.

### Prerequisites
For this tutorial we will be needing  the following from AWS:
- An active AWS account.
- of EC2 instances with Amazon Linux 2 as the OS.
- AWS Keys for SSH to access Control Node and Manage Nodes.
- Security group which allow SSH protocol and HTTP protocol.
- A decent editor such as Vim or Notepad++ to create the Inventory and the Playbook.
 
### EC2 Instances provisioning
The following are the steps to provision EC2 instances with the AWS web console. 

1. Go to AWS Console > EC2 > Launch Instances.
2. Select the Amazon Linux 2 AMI.
3. Select a Key Pair. If there are no available Key Pair , please create one according to [this instruction.]( https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html )
4. Allow SSH and HTTP
5. Set Number of Instances to 4
6. Click Launch Instance

Screenshot:
![Steps to EC2](/blog/2022/08/ansible-tutorial-with-aws-ec2/ansible02-ec2.webp)


### Ansible Nodes and SSH keys
In this section we will gather the IP of EC2 instances and setup the SSH keys for accssing them. 

1. Go to AWS Console > EC2 > Launch Instances
2. Get the Public IPV4
3. Wed will choose the first EC2 to be the Ansible Control Node and the rest to be the Manage Nodes as follows:
| Ansible Node | IP Adddress |
|--------------|-------------|
| Control Node | 13.215.159.65 |
| Manage Nodes | 18.138.255.51<br>13.229.198.36<br>18.139.0.15 |

Screenshot:
![Steps to EC2](/blog/2022/08/ansible-tutorial-with-aws-ec2/ansible-ng02.webp)

Login Control Node by using our Key Pair. For me it is kaptenjeffry.pem
```plain 
ssh -i kaptenjeffry.pem ec2-user@13.215.159.65
```
Open another terminal and copy the Key Pair to the Control Node
```plain
scp -i kaptenjeffry.pem kaptenjeffry.pem ec2-user@13.215.159.65:~/.ssh
```
Go back to the Control Node Terminal. Try to login from Control Node to one of the Manage Nodes by using the Key Pair. This is to ensure the Key Pair is usable to access the Managed Nodes
```plain
ssh -i .ssh/kaptenjeffry.pem ec2-user@18.138.255.51
```
Register the rest for the Manage Nodes as known hosts to the Control Nodes. This is to set the managed nodes as known hosts to Control Nodes in bulk. 
```plain
ssh-keyscan -t ecdsa-sha2-nistp256 13.229.198.36 18.139.0.15 >> .ssh/known_hosts
```

### Ansible Installation and Configuration
In this section we will install Ansible in the Control Node and create the Inventory file.

1. Go to the Control Node and execute the following commands to install Ansible
```plain
sudo yum update -y
sudo amazon-linux-extras install ansible2 -y
ansible –version
```
Where:
- The fist command is to update the yum package manager
- The 2nd command is to install ansible by using amazon-linux-extras command
- The 3rd command is to check the version of installed ansible

2. Create a file named  myinventory.ini. Insert the IP addresses that we have identified earlier to be the managed node in the following format:
```ini
[mynginx]
red ansible_host=18.138.255.51
green ansible_host=13.229.198.36
blue ansible_host=18.139.0.15
```
Where:
- [mynginx] =  the group name of the manage nodes
- The first column is the alias of a manage node
- 2nd column is the IP Address of a manage nodes

The myinventory.ini above is a basic Inventory file in a INI format. An Inventory file could be either in INI or YAML format. For more information on the Inventory  [go here.]( https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html)

### The Ansible Modules and  The Ansible Adhoc Command

Ansible modules are scripts to do a specific task at managed nodes.  For example there are modules to check availability, there are modules to copy files, there are modules to install applications and many more. To get the full list of modules, you can check the official [Ansible modules page.]( https://docs.ansible.com/ansible/2.9/modules/list_of_all_modules.html)

A quick way to use Ansible modules is with the Ansible Adhoc command. It is the command line interface for executing modules at the managed nodes. The usage are as follows
```plain
ansible [pattern] -m [module] -a "[module options]" -i [inventory]
```

Where 
- pattern= ip, hostname, alias or group name
- -m module= name of the module to be use
- -a “...”= argument or option for the module
- -i [inventory] = inventory of the manage nodes 

The following are some example of Ansible Adhoc Commands:

Ping module: To check ssh connectivity and python interpreter at the managed node..To use module ping against mynginx group of servers ( all 3 host; red,green and blue)
```plain
ansible mynginx -m ping -i myinventory.ini
```
Sample output:
![ping](/blog/2022/08/ansible-tutorial-with-aws-ec2/ansible04-ping-all.webp)

Copy module: To copy file to managed node. To use module copy to copy a text file /home/ec2-user/hello.txt at Control node to /tmp/ at all manage nodes in the mynginx group.
```plain
ansible mynginx -m copy \
-a 'src=/home/ec2-user/hello.txt dest=/tmp/hello.txt' \
-i myinventory.ini
```

Shell module: To execute a shell script at managed node. To use module shell to execute "uptime" at all manage nodes in the mynginx gro
up.
```plain
ansible mynginx -m shell -a 'uptime' -i myinventory.ini
```

### The Ansible Playbook

Ansible Playbook is a configuration file in a YAML format that will tell Ansible what to do. Ansible Playbook executes its assigned tasks sequentially from top to bottom. Tasks in Playbook are grouped by a block of codes Play. The following diagram shows the high level structure of a Playbook.

<p align="center">
<img src="/blog/2022/08/ansible-tutorial-with-aws-ec2/ansible-hi-level.webp" width="400" />
</p>

Now we are going to use Ansible Playbook to install nginx at the 3 Manage Nodes as depicted in the following diagram. 
![hi-level-playbook](/blog/2022/08/ansible-tutorial-with-aws-ec2/ansible01.webp)

Create the following YAML file and name it nginx-playbook.yaml. This is a playbook with one Play that will install and configure Nginx service at the managed node. 

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
- name ( top most): name of this play
- hosts: targeted manage nodes for this play
- become:   use superuser privilege ( sudo for linux )
- vars: variables definition for this play  
- task: start of task section
- name ( under task section): name of a task
- module name ( under the name of the task)
- module attribute ( under module name )


Lets try to execute this Playbook. Firstly we need to create the source index.html to be copied to managed node.
```plain
echo 'Hello World!' > index.html
```

Execute the following ansible-playbook command against our Playbook. Just like the Adhoc command, we need to specify the Inventory by the -i switch.
```plain
ansible-playbook nginx-playbook.yaml  -i myinventory.in
```
Sample output:
![ping](/blog/2022/08/ansible-tutorial-with-aws-ec2/ansible-ng07.webp)

Now we can curl our manage nodes to check on the  Nginx service and the custom index.html
```plain
curl 18.138.255.51
curl 13.229.198.36
curl 18.139.0.15
```
Sample output:
<p align="center">
<img src="/blog/2022/08/ansible-tutorial-with-aws-ec2/ansible-ng10.webp" width="600" />
</p>

### Conclusion
That’s all folks. We have successfully managed EC2 instances with Ansible. What covers in this tutorial are the fundamentals of Ansible to start managing remote servers. Ansible rises above its competitors due to its simplicity of its installation, configuration and usage.  To get further information for Ansible you may visit its [official documentation.](https://docs.ansible.com/ansible/latest/getting_started/index.html)




