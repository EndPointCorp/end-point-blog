---
author: Cas Rusnov
title: Ansiblizing SSH Keys
github_issue_number: 938
tags:
- ansible
- ssh
- sysadmin
date: 2014-03-03
---



It is occasionally the case that several users share a particular account on a few boxes, such as in a scenario where a test server and a production server share a deployment account, and several developers work on them. In these situations the preference is to authenticate the users with their ssh keys through authorized_keys on the account they are sharing, which leads to the problem of keeping the keys synchronized when they are updated and changed. We add the additional parameter that perhaps any given box will have a few users of the account that aren’t shared by the others, but otherwise allow a core of developers to access them. Now extend this scenario across hundreds of machines, and the maintenance becomes difficult or impossible when updating any of the core accounts. Obviously this is a job for a remote management framework like Ansible.

### Our Example Scenario

We have developers Alice, Bob and Carla which need access to every box. We have additional developers Dwayne and Edward that only need access to one box each. We have a collection of servers: dev1, dev2, staging and prod. All of the servers have an account called web_deployment.

The authorized_keys for web_deployment on each box contains:

- dev1

    - alice
    - bob
    - carla

- dev2

    - alice
    - bob
    - carla
    - dwayne

- staging

    - alice
    - bob
    - carla
    - edward

- prod

    - alice
    - bob
    - carla

### Enter Ansible

Ansible is setup for every box already. The basic strategy for managing the keys is to copy a default authorized_keys file from the ansible host containing Alice, Bob and Carla (since they are present on all of the destination machines) and assemble the keys with a collection of keys local to the host (Dwayne’s key on dev2, and Edward’s key on staging). To perform the assembly action we also want to provide a script so that the keys can be manually manipulated (local keys changed) without touching the ansible box. The script is thus:

```bash
#!/usr/bin/env bash
set -u -o errexit -o pipefail

target_ssh_dir="/home/web_deployment/.ssh"
base_authorized_key_file="authorized_keys"

local_authorized_keys="${target_ssh_dir}/${base_authorized_key_file}.local"
hosting_authorized_keys="${target_ssh_dir}/${base_authorized_key_file}.hosting"
target_authorized_keys="${target_ssh_dir}/${base_authorized_key_file}"

tmp_authorized_keys="${target_ssh_dir}/${base_authorized_key_file}.tmp"

authorized_keys_backup_dir="${target_ssh_dir}/history"

# BEGIN multiline configuration_management_disclaimer string variable
configuration_management_disclaimer="\n\
# ******************************************************************************\n\
# This file is automatically managed by End Point Configuration management
# system. In order to change it please apply your changes
# to $local_authorized_keys and run $0\n\
# so to assemble a new $target_authorized_keys\n\
# ******************************************************************************\n\
"
# END multiline configuration_management_disclaimer string variable

# BEGIN assembling tmp file
echo -e "$configuration_management_disclaimer" > $tmp_authorized_keys

echo -e "# BEGIN STANDARD HOSTING KEYS\n" >> $tmp_authorized_keys
cat $hosting_authorized_keys >> $tmp_authorized_keys
echo -e "# END STANDARD HOSTING KEYS\n" >> $tmp_authorized_keys

if [[ -r $local_authorized_keys ]]
then
  echo -e "# BEGIN LOCAL KEYS\n" >> $tmp_authorized_keys
  cat $local_authorized_keys >> $tmp_authorized_keys
  echo -e "# END LOCAL KEYS\n" >> $tmp_authorized_keys
fi

echo -e "$configuration_management_disclaimer" >> $tmp_authorized_keys
# END assembling tmp file

# BEGIN check (and do) backup of old file
if ! cmp $tmp_authorized_keys $target_authorized_keys &> /dev/null
then
  mkdir -p $authorized_keys_backup_dir

  backup_old_auth_keys="${authorized_keys_backup_dir}/${base_authorized_key_file}_$(date '+%Y%m%dT%H%M%z')"
  cat $target_authorized_keys > $backup_old_auth_keys
fi
# END check (and do) backup of old file

cat $tmp_authorized_keys > $target_authorized_keys

rm $tmp_authorized_keys

if [ -d $authorized_keys_backup_dir ]
then
  if [ -n "$(find $authorized_keys_backup_dir -maxdepth 0 -type d)" ]
  then
    chmod -R u=rwX,go= $authorized_keys_backup_dir
  fi
fi

if [ -f $local_authorized_keys ]
then
  if [ -n "$(find $local_authorized_keys -maxdepth 0 -type f)" ]
  then
    chmod u=rw $local_authorized_keys
  fi
fi

if [ -f $hosting_authorized_keys ]
then
  if [ -n "$(find $hosting_authorized_keys -maxdepth 0 -type f)" ]
  then
    chmod u=rw $hosting_authorized_keys
  fi
fi
```

We then use an Ansible task to distribute the files to the destination hosts:

```js
# tasks/authorized_keys_deploy.yml
---
  - name: Create /home/web_deployment subdirectories
    file: path=/home/web_deployment/{{ item }}
          state=directory
          owner=web_deployment
          group=web_deployment
          mode=0700
    with_items:
      - .ssh
      - bin

  - name: Copy /home/web_deployment/.ssh/authorized_keys.universal
    template: src=all/home/web_deployment/.ssh/authorized_keys.universal.j2
          dest=/home/web_deployment/.ssh/authorized_keys.hosting
          owner=web_deployment
          group=web_deployment
          mode=0600
    notify:
      - Use shellscript to locally assemble authorized_keys

  - name: Copy /home/web_deployment/bin/assemble_authorized_keys.sh
    copy: src=files/all/home/web_deployment/bin/assemble_authorized_keys.sh
          dest=/home/web_deployment/bin/assemble_authorized_keys.sh
          owner=web_deployment
          group=web_deployment
          mode=0700
    notify:
      - Use shellscript to locally assemble authorized_keys
```

This task is invoked by an Ansible playbook:

```js
# authorized_keys_deploy.yml
---
- name: authorized_keys file deployment/management
  hosts: authorized_keys_servers
  user: root

  handlers:
  - include: handlers/authorized_keys_deploy.yml

  tasks:
  - include: tasks/authorized_keys_deploy.yml
```

And finally the handler which invokes the assembly script:

```js
# handlers/authorized_keys_deploy.yml
---
  - name: Use shellscript to locally assemble authorized_keys
    command: "/home/web_deployment/bin/assemble_authorized_keys.sh"
```

A note about this setup: The authorized_keys.universal has the extension .j2, and is invoked as a Jinja2 template. This allows server-specific conditionals amongst other things. It is useful for example when per-key shell features are used (for example restricting one particular key to invoking rsync for backups), and if the OS selection is mixed thus requiring the paths to differ between hosts.

### Conclusion

We hope that this example is helpful. There are some clear directions for improvement and ways to make this suit other scenarios, such as having the universal keys list also merged with an additional keys list select by host or other information such as OS or abstract values associated with the host. One could also envision a system in which some arbitrary collection of key files are merged at the destination server selected through the aforementioned means or others.

Shout out to Lele Calo for his putting together the Ansible setup for this procedure.


