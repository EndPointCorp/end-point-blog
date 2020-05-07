---
author: Spencer Christensen
gh_issue_number: 1026
tags: camps, environment, tools, vagrant
title: Looking at development environments with DevCamps and Vagrant
---

For most web developers, you have practices and tools that you are used to using to do your work. And for most web developers this means setting up your workstation with all the things you need to do your editing, compiling, testing, and pushing code to some place for sharing or deployment. This is a very common practice even though it is fraught with problems- like getting a database setup properly, configuring a web server, any other services (memcached, redis, mongodb, etc), and many more issues.

Hopefully at some point you realize the pain that is involved in doing everything on your workstation directly and start looking for a better way to do web development. In this post I will be looking at some ways to do this better: using a virtual machine (VM), Vagrant, and DevCamps.

 

### Using a VM for development

One way to improve things is to use a local virtual machine for your development (for example, using VirtualBox, or VMware Fusion). You can edit your code normally on your workstation, but then execute and test it in the VM. This also makes your workstation “clean”, moving all those dependencies (like a database, web server, etc.) off your workstation and into the VM. It also gets your dev environment closer to production, if not identical. Sounds nice, but let’s break down the pros and cons.

#### Benefits of using a VM

- Dev environment closely matches production.
- Execute and test code in a dedicated machine (not your workstation directly).
- Allows for multiple projects to be worked on concurrently (one VM per project).
- Exposes the developer to the Operations (systems administration) side of the web application (always a good thing).
- Developer can edit files using their favorite text editor locally on the workstation (but will need to copy files to the VM as needed).

#### Problems with using a VM

- Need to create and configure the VM. This could be very time consuming and error prone.
- Still need to install and configure all services and packages. This could also be time consuming and error prone.
- Backups of your work/configuration/everything are your own responsibility (extremely unlikely to happen).
- Access to your dev environment is extremely limited, thus probably only you can access it and test things on it. No way for a QA engineer or business owner to test/demo your work.
- Inexperienced developers can break things, or change them to no longer match production (install arbitrary packages, different versions than what is in production, screw up the db, screw up Apache configuration, etc.).
- If working with an established database, then downloading a dump, installing, and getting the database usable is time consuming and error prone. (“I just broke my dev database!” can be a complete blocker for development.)
- The developer needs to set up networking for the VM in order to ssh to it, copy files back and forth, and point a web browser to it. This may include manually setting up DNS, or /etc/hosts entries, or port forwarding, or more complex setups.
- If using SSL with the web application, then the developer also needs to generate and install the SSL cert and configure the web server correctly.

### Vagrant

What is [Vagrant](https://www.vagrantup.com)? It is a set of tools to make it easier to use a virtual machine for your web development. It attempts to lessen many of the problems listed above through the use of automation. By design it also makes some assumptions about how you are using the VM. For example, it assumes that you have the source code for you project in a directory somewhere directly on your workstation and would prefer to use your favorite text editor on those files. Instead of expecting you to continually push updated files to your VM, it sets up a corresponding directory on the VM and keeps the two in sync for you (using either shared folders, NFS, Samba, or rsync). It also sets up the networking for accessing the VM, usually with port forwarding, so you don’t have to worry about that.

#### Benefits of Vagrant

- ***Same as those listed above for using a VM, plus...***
- Flexible configuration (Vagrantfile) for creating and configuring the VM.
- Automated networking for the VM with port forwarding. Abstracted ssh access (don’t need to set up a hostname for the VM, simply type `vagrant ssh` to connect). Port forwarded browser access to the VM (usually http://localhost:8080, but configurable).
- Synced directory between your workstation and the VM for source code. Allows for developers to use their favorite text editor locally on their workstation without needing to manually copy files to the VM.
- Expects the use of a configuration management system (like puppet, chef, salt, or bash scripts) to “provision” the VM (which could help with proper and consistent setup).
- Through the use of [Vagrant Cloud](https://vagrantcloud.com/) you can get a generated url for others to access your VM (makes it publicly available through a tunnel created with the command `vagrant share`).
- Configuration (Vagrantfile and puppet/chef/salt/etc.) files can be maintained/reviewed by Operations engineers for consistency with production.

#### Problems with Vagrant

- Still need to install and configure all services and packages. This is lessened with the use of a configuration management tool like puppet, but you still need to create/debug/maintain the puppet configuration and setup.
- Backups of your work/configuration/everything are your own responsibility (extremely unlikely to happen). This may be lessened for VM configuration files, assuming they are included in your project’s VCS repo along with your source code.
- Inexperienced developers can still break things, or change them to no longer match production (install arbitrary packages, different versions than what is in production, screw up the db, screw up Apache configuration, etc.).
- If working with an established database, then downloading a dump, installing, and getting the database usable is time consuming and error prone. (“I just broke my dev database!” can be a complete blocker for development.)
- If using SSL with the web application, then the developer also needs to generate and install the SSL cert and configure the web server correctly. This might be lessened if puppet (or whatever) is configured to manage this for you (but then you need to configure puppet to do that).

### DevCamps

The [DevCamps](http://devcamps.org) system takes a different approach. Instead of using VMs for development, it utilizes a shared server for all development. Each developer has their own account on the camps server and can create/update/delete “camps” (which are self-contained environments with all the parts needed). There is an initial setup for using camps which needs thorough understanding of the web application and all of its dependencies (OS, packages, services, etc.). For each camp, the system will create a directory for the user with everything related to that camp in it, including the web application source code, their own web server configuration, their own database with its own configuration, and any other resources. Each camp is assigned a camp number, and all services for that camp run on different ports (based on the camp number). For example, camp 12 may have Apache running on ports 9012 (HTTP) and 9112 (HTTPS) and MySQL running on port 8912. The developer doesn’t need to know these ports, as tools allow for easier access to the needed services (commands like `mkcamp`, `re` for restarting services, `mysql_camp` for access to the database, etc.).

DevCamps has been designed to address some of the pain usually associated with development environments. Developers usually do not need to install anything, since all dependencies should already be installed on the camps server (which should be maintained by an Operations engineer who can keep the packages, versions, etc. consistent with production). Having all development on a server allows Operations engineers to backup all dev work fairly easily. Databases do not need to be downloaded, manually setup, or anything- they should be set up initially with the camps system and then running `mkcamp` clones the database and sets it up for you. Running `refresh-camp --db` allows a developer to delete their camp’s database and get a fresh clone, ready to use.

#### Benefits of DevCamps

- Each developer can create/delete camps as needed, allowing for multiple camps at once and multiple projects at once.
- Operations engineers can manage/maintain all dependencies for development, ensuring everything is consistent with production.
- Backups of all dev work is easy (Operations engineer just needs to backup the camps server).
- Developer does not need to configure services (camp templating system auto-generates needed configuration for proper port numbers), such as Apache, nginx, unicorn, MySQL, Postgres, etc.
- SSL certificates can be easily shared/generated/installed/etc. automatically with the `mkcamp` script. Dev environments can easily have HTTPS without the developer doing anything.
- Developers should not have permissions to install/change system packages or services. Thus inexperienced developers should not be able to break the server, other developer’s environments, install arbitrary software. Screwing up their database or web server config can be fixed by either creating a new camp, refreshing their existing one, or an Operations engineer can easily fix it for them (since it is on a central server they would already have access to, and not need to worry about how to access some VM who knows where).

#### Problems with DevCamps

- Since all camps live on a shared server running on different ports, this will not closely match production in that way. However, this may not be significant if nearly everything else does closely match production.
- Adding a new dependency (for example, adding mongodb, or upgrading the version of Apache) may require quite a bit of effort and will affect all camps on the server- Operations engineer will need to install the needed packages and add/change the needed configuration to the camps system and templates.
- Using your favorite text editor locally on your workstation doesn’t really work since all code lives on the server. It is possible to SFTP files back and forth, but this can be tedious and error prone.
- Many aspects of the Operations (systems administration) side of the web application are hidden from the developer (this might also be considered a benefit).
- All development is on a single server, which may be a single point of failure (if the camps server is down, then all development is blocked for all developers).
- One camp can use up more CPU/RAM/disk/etc. then others and affect the server’s load, affecting the performance of all other camps.

### Concluding Thoughts

It seems that Vagrant and DevCamps certainly have some good things going for them. I think it might be worth some thought and effort to try to meld the two together somehow, to take the benefits of both and reduce the problems as much as possible. Such a system might look like this:

- Utilize vagrant commands and configuration, but have all VMs live on a central VM server. Thus allowing for central backups and access.
- Source code and configuration lives on the server/VM but a synced directory is set up (sshfs mount point?) to allow for local editing of text files on the workstation.
- VMs created should have restricted access, preventing developers from installing arbitrary packages, versions, screwing up the db, etc.
- Configuration for services (database, web server, etc.) should be generated/managed by Operations engineers for consistency (utilizing puppet/chef/salt/etc.).
- Databases should be cloned from a local copy on the VM server, thus avoiding the need to download anything and reducing setup effort.
- SSL certs should be copied/generated locally on the VM server and installed as appropriate.
- Sharing access to a VM should not depend on Vagrant Cloud, but instead should use some sort of internal service on the VM server to automate VM hostname/DNS for browser and ssh access to the VM.

I’m sure there are more pros and cons that I’ve missed. Add your thoughts to the comments below. Thanks.
