---
author: Mike Farmer
gh_issue_number: 946
tags: ansible, devops, environment, tools
title: Provisioning a Development Environment with Packer, Part 2
---



In my [previous post](/blog/2014/03/12/provisioning-development-environment) on provisioning a development environment with [Packer](https://www.packer.io) I walked through getting a server setup with an operating system installed. This post will be focused setting up [Ansible](https://www.ansible.com) so that I can setup my development environment just the way I like it. Packer supports many different methods for provisioning. After playing with some of them, I decided that Ansible was a good mix of simplicity and functionality.

A Packer provisioner is simply a configuration template that is added to the json configuration file. The “provisioners” section of the configuration file takes an array of json objects which means that you aren’t stuck with just one kind of provisioner. For example, you could run some shell scripts using the [shell provisioner](https://www.packer.io/docs/provisioners/shell.html), then upload some files using the [File Uploads](https://www.packer.io/docs/provisioners/file.html) provisioner, followed by your devops tool of choice ([puppet](https://www.packer.io/docs/provisioners/puppet-masterless.html), [salt](https://www.packer.io/docs/provisioners/salt-masterless.html), [chef](https://www.packer.io/docs/provisioners/chef-solo.html), or [ansible](https://www.packer.io/docs/provisioners/ansible-local.html)). You can even [roll-your-own](https://www.packer.io/docs/extend/provisioner.html) provisioner if desired. Here’s an example provisioner setup for the shell provisioner:

```
{
  "variables": {...},
  "builders" : [...],
  "provisioners" [
    {
      "type": "shell",
      "inline": [ "echo foo" ]
    }
  ]
}
```

### Sudo and User Considerations

Packer will login to the server over ssh and run your provisioners. The big headache that always comes out of this is some provisioners require sudo, or being logged in as root, to run their commands. Packer, however, will login as the user that was created during the build stage (see the “builders” section in the code snippet in the [previous post](/blog/2014/03/12/provisioning-development-environment)). There are a couple of ways to handle this. First, you can do everything in packer as root. I don’t love this approach because I like to simulate the way that I setup a machine by hand and I never login as root if I can help it. The second method is to grant your user sudo access. This gets a little tricky so I’ll just show the a code snippet and then explain it below.

```
{
  "type": "shell",
  "execute_command": "echo '{{user `ssh_pass`}}' | {{ .Vars }} sudo -E -S sh '{{ .Path }}'",
  "inline": [
    "echo '%sudo    ALL=(ALL)  NOPASSWD:ALL' >> /etc/sudoers"
  ]
}
```

Utilizing the shell provisioner, the execute_command option is used to specify to the provisioner that whenever a command is run, use this command. The commands provided to the inline array are compiled into a single shell script which is injected as the .Path variable. To quote the Packer [documentation](https://www.packer.io/docs/provisioners/shell.html):

> 
> 
> 
> The -S flag tells sudo to read the password from stdin, which in this case is being piped in with the value of [the user variable ssh_pass.] The -E flag tells sudo to preserve the environment, allowing our environmental variables to work within the script.
> 
> 
> 
> 
> 
> By setting the execute_command to this, your script(s) can run with root privileges without worrying about password prompts.
> 
> 
> 

Taking advantage of this trick, a command can now be placed in the inline section that will add all members of the sudo group to the sudoers file granting them permission to use sudo without a password. Now I know this isn’t secure but for my purpose, which is to create a custom development enviornment on a Virtual Machine running only on my machine, this will be just fine. I also use this example to illustrate how to run commands as sudo.

### The Ansible Provisioner

Once the shell provisioner is working, Ansible can be installed on the new machine and then executed using Packer’s Ansible provisioner. The easiest way to do this that I found was to have the shell provisioner install Ansible on the virtual machine as well as upload an ssh public key so that the Ansible user could log in. My “provisioners” section looks like this:

```
"provisioners": [
  {
    "type": "shell",
    "inline": [
      "mkdir .ssh",
      "echo '{{user `public_key`}}' >> .ssh/authorized_keys"
    ]
  },
  {
    "type": "shell",
    "execute_command": "echo '{{user `ssh_pass`}}' | {{ .Vars }} sudo -E -S sh '{{ .Path }}'",
    "inline": [
      "add-apt-repository ppa:rquillo/ansible",
      "apt-get update",
      "apt-get install -y ansible",
      "echo '%sudo    ALL=(ALL)  NOPASSWD:ALL' >> /etc/sudoers"
    ]
  },
  {
    "type": "ansible-local",
    "playbook_file": "site.yml"
  }
]
```

This configuration uses a variable in which I placed an ssh public key (I could also have used the File Uploads provisioner for this), installs Ansible from an updated PPA, and grants the user sudo priveliges via the sudo group as explained above. This also shows how you can execute more than one statement at a time using the “shell” provisioner.

### Ansible Provisioning Tip

This tip could probably apply to any of the devops tools you’d like to use. If you are creating your Ansible yml files for the first time, you will likely run into the issue where you spend a lot of time waiting for the machine to build and provision only to discover your Ansible script is wrong. Troubleshooting becomes a problem because if anything fails during the provision, Packer will stop running and delete the Virtual Machine leaving you with no option other than fixing your mistake and then waiting for the entire process to run again.

One way I found around this is to take the last section of the provisioners array out, build your machine, and then move the base machine into a new directory once it’s been successfully built. From there you can start the machine manually and then run the ansible-playbook command from your local machine while you develop your playbook. Once you have a working playbook, add the ansible-local section back to the provisioners array and rebuild your machine with Packer. That should speed up your development and troubleshooting cycles.

### A Hiccup with Ansible and Packer

Ansible allows you to create template files that can be used for configuration files and the like. According to the documentation, you can specify the location of the templates and other files using the playbook_paths option in the provisioner. I could not get this to work and after a lot of troubleshooting and looking at the [code for the provisioner](https://github.com/mitchellh/packer/blob/master/provisioner/ansible-local/provisioner.go) I am convinced there is a bug copying the playbook_paths directories to the remote machine. I’ve [posted on the Packer discussion group](https://groups.google.com/forum/#!topic/packer-tool/RrIGFH3K1bE) about this but haven’t had any response on it yet. Once I get to the bottom the issue I’ll post an update here.

### Conclusion

Packer has turned out to be a fabulous resource for me in quickly ramping up development environments. Ansible has also been a breath for fresh air for provisioning those machines. I’ve previously used [chef](https://www.getchef.com/chef/) and other devops tools which only led to a great deal of frustration. I’m happy to have some new tools in my belt that took very little time to learn and to get working.


