---
author: Zed Jensen
title: Deploying (Minecraft) Servers Automatically with Terraform
github_issue_number: 1651
tags:
- automation
- terraform
- cloud
date: 2020-07-16
---

![](/blog/2020/07/automating-minecraft-server/banner.jpg)

Last year I bought an old Dell Optiplex on eBay to use as a dedicated [Minecraft](https://www.minecraft.net/en-us/) server for my friends and me. It worked well for a while, but when my university switched to online classes and I moved home, I left it at my college apartment and was unable to fix it (or retrieve our world save) when it failed for some reason. I still wanted to play Minecraft with friends, though, so I had to figure out a solution in the meantime.

I’d previously used a basic [DigitalOcean](https://www.digitalocean.com/) droplet as a Minecraft server, but that had suffered with lag issues, especially with more than two or three people logged in. Their $5 tier of virtual machine provides 1GB of RAM and 1 CPU core, so it shouldn’t be too much of a surprise that it struggled with a Minecraft server. However, more performant virtual machines cost a lot more, and I wanted to keep my solution as cheap as possible.

I mentioned this to a co-worker and he pointed out that most companies don’t actually charge for virtual machines on a monthly basis; in reality, it’s an hourly rate based on when your virtual machine instance actually exists. So, he suggested I create a virtual machine and start my Minecraft server every time I wanted to play, then shut it down and delete it when I was finished, thus saving the cost of running it when it wasn’t being used.

Of course, you could do this manually in your provider’s dev console, but who wants to manually download dependencies, copy your world over, and set up a new server every time you want to play Minecraft? Not me! Instead, I used [Terraform](https://www.terraform.io/), an open-source tool that lets you describe your desired infrastructure and then sets it up for you.

In this post, I’ll show how I got my server setup streamlined into one Terraform configuration file that creates a virtual machine, runs a setup script on it, copies my Minecraft world to it with [rsync](https://rsync.samba.org/), starts the Minecraft server, and adds a DNS entry for your new server.

### Picking a provider

As I mentioned earlier, I’ve used DigitalOcean in the past, but at the recommendation of my co-worker, I decided to try [UpCloud](https://upcloud.com/), a similar service based in Helsinki, Finland. They have datacenters in the US, Europe, and Singapore (the one I used is in Chicago—a full list of locations can be found [here](https://developers.upcloud.com/1.3/5-zones/)). They offer several affordable tiers of virtual machines, including these:

<div class="table-scroll">
  <table>
    <thead>
      <td>Memory</td>
      <td>CPU</td>
      <td>Storage</td>
      <td>Transfer</td>
      <td>Price</td>
    </thead>
    <tr>
      <td>1 GB</td>
      <td>1</td>
      <td>25 GB</td>
      <td>1 TB</td>
      <td>$5/mo</td>
    </tr>
    <tr>
      <td>2 GB</td>
      <td>1</td>
      <td>50 GB</td>
      <td>2 TB</td>
      <td>$10/mo</td>
    </tr>
    <tr>
      <td>4 GB</td>
      <td>2</td>
      <td>80 GB</td>
      <td>4 TB</td>
      <td>$20/mo</td>
    </tr>
    <tr>
      <td>8 GB</td>
      <td>4</td>
      <td>160 GB</td>
      <td>5 TB</td>
      <td>$40/mo</td>
    </tr>
  </table>
</div>

There are more tiers, but for a Minecraft server I didn’t need anything that powerful. I decided on the $20/month tier—or, in my case, $0.03/hour.

### Installing Terraform

The process for setting up Terraform depends on what provider you’re using. If you’d like to use DigitalOcean or another provider, just make sure they’re on Terraform’s list of [supported providers](https://www.terraform.io/docs/providers/index.html). Alternatively (as is the case for UpCloud), some providers aren’t officially supported but do have plugins that work well.

In my case, I followed UpCloud’s instructions for installation [here](https://upcloud.com/community/tutorials/get-started-terraform/). The rest of that tutorial does a great job showing you how to use Terraform with UpCloud via their plugin, but for instructions more suited to other use cases I’d recommend looking at Terraform’s wealth of learning resources, which can be found [here](https://learn.hashicorp.com/terraform).

You’ll also need to install the UpCloud plugin. This is detailed in the earlier tutorial at UpCloud’s site, so I’ll forgo putting it here.

### Creating a Terraform configuration file

Once you’ve got Terraform and UpCloud’s plugin installed, create a directory for your project (`mkdir minecraft`) and run `terraform init` in it. Once you’ve done that, using Terraform is as simple as creating a configuration file describing your server. How exactly that looks depends on your provider, but my initial file, which I named `server.tf`, looked something like this:

```plain
provider "upcloud" {
  # Your UpCloud credentials are read from the environment variables
  # export UPCLOUD_USERNAME="Username for UpCloud API user"
  # export UPCLOUD_PASSWORD="Password for UpCloud API user"
}

resource "upcloud_server" "minecraft1" {
  # System hostname
  hostname = "minecraft1"

  # Availability zone
  zone = "us-chi1"

  # Number of CPUs and memory in GB
  plan = "2xCPU-4GB"

  storage_devices {
    # OS root disk size
    size = 25

    # Template UUID for Ubuntu 18.04
    storage = "01000000-0000-4000-8000-000030080200"

    tier   = "maxiops"
    action = "clone"
  }

  # Include at least one public SSH key
  login {
    user = "root"
    keys = [
      "PUBLIC_SSH_KEY_HERE"
    ]
    create_password = false
  }

  # Configuring connection details
  connection {
    host        = self.ipv4_address
    type        = "ssh"
    user        = "root"
    private_key = file("./id_rsa_upcloud")
  }
}
```

There are a few important sections here:

- The hostname (which will be important later)
- The zone (Full list [here](https://developers.upcloud.com/1.3/5-zones/))
- The plan (more information on the plan codes [here](https://developers.upcloud.com/1.3/7-plans/))
- The `login` and `connection` sections

The last two in particular need some attention; I created an SSH key specifically for managing my Minecraft server and included the public key in the `login` section and a link to the private key in the `connection` section.

After providing credentials via environment variables as per UpCloud’s tutorial, you can run `terraform plan` to see what your current configuration looks like:

```plain
zed@zeds-pc:~/minecraft $ terraform plan
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.


------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # upcloud_server.minecraft1 will be created
  + resource "upcloud_server" "minecraft1" {
      + cpu                  = (known after apply)
      + hostname             = "minecraft1"
      + id                   = (known after apply)
      + ipv4                 = true
      + ipv4_address         = (known after apply)
      + ipv4_address_private = (known after apply)
      + ipv6                 = true
      + ipv6_address         = (known after apply)
      + mem                  = (known after apply)
      + plan                 = "2xCPU-4GB"
      + private_networking   = true
      + title                = (known after apply)
      + zone                 = "us-chi1"

      + login {
          + create_password   = false
          + keys              = [
              + "PUBLIC_SSH_KEY_HERE",
            ]
          + password_delivery = "none"
          + user              = "root"
        }

      + storage_devices {
          + action  = "clone"
          + address = (known after apply)
          + id      = (known after apply)
          + size    = 25
          + storage = "01000000-0000-4000-8000-000030080200"
          + tier    = "maxiops"
          + title   = (known after apply)
        }
    }

Plan: 1 to add, 0 to change, 0 to destroy.

------------------------------------------------------------------------

Note: You didn't specify an "-out" parameter to save this plan, so Terraform
can't guarantee that exactly these actions will be performed if
"terraform apply" is subsequently run.
```

This command shows you what’ll happen when you run `terraform apply`, which also shows you the changes that are going to happen, after which it prompts you to apply them. We’ll hold off for now, since we need more than a blank Ubuntu server; we need to get our Minecraft world and libraries onto this server.

### Adding startup scripts

To get my new virtual machine running a Minecraft server, I needed to perform some initial setup. Specifically, I needed to copy my server files from my local machine, then download the Java runtime and start the server on the newly created VM. To accomplish this, I created a setup script and uploaded it to a private server; you could also use a public GitHub repo or similar and just download it from there. I also had to configure my `server.tf` to get this script and copy over my Minecraft world after creation.

The sections I added to my `upcloud` resource block in my `server.tf` file look like this:

```plain
  provisioner "remote-exec" {
    inline = [ 
      "wget http://zedjensen.com/init_minecraft.sh && chmod +x init_minecraft.sh && ./init_minecraft.sh -f && rm init_minecraft.sh"
    ]   
  }

  provisioner "local-exec" {
    command = "rsync --delete -r -e 'ssh -F ./ssh_config -i ./id_rsa_upcloud' server root@${self.ipv4_address}:~/minecraft/"
  }

  provisioner "remote-exec" {
    inline = [ 
      "bash ~/minecraft/start_server.sh"
    ]   
  }
```

The provisioners `remote-exec` and `local-exec` tell Terraform to run these commands on the new virtual machine and my local machine respectively. As you can see, I have the remote machine fetching an init script I wrote and running it, then deleting it. The local exec then copies over my Minecraft server, using the SSH key I created specifically for this, and using an alternate SSH config that uses /dev/null as the known_hosts file, avoiding security warnings on later runs when the machine at `minecraft.zedjensen.com` isn’t the same machine as it was before. `${self.ipv4_address}` is replaced by Terraform with the IP address of the new server. Finally, I run `start_server.sh` from the files I copied over with rsync.

For reference, the relevant parts of my init script and ssh_config look something like this:

```plain
#!/bin/bash

echo "StrictHostKeyChecking accept-new" >> /etc/ssh/ssh_config
service sshd restart

i=0
tput sc
while ! apt install openjdk-8-jdk-headless tmux zip unzip -y &> /dev/null; do
    case $i in
        0 ) j="-" ;;
        1 ) j="\\" ;;
        2 ) j="|" ;;
        3 ) j="/" ;;
    esac
    tput rc echo =en "\r[$j] Waiting to install dependencies..."
    sleep 1
done

mkdir -p minecraft/server
```

```plain
StrictHostKeyChecking no
UserKnownHostsFile /dev/null
```

### Adding a DNS record with Cloudflare

After the last steps, you should be able to get a server up and running, but you’d have to use the IP address to connect to it directly. I have the domain `zedjensen.com`, so I decided to use `minecraft.zedjensen.com`. Luckily, Terraform also supports Cloudflare, so I set up Cloudflare as my DNS provider for `zedjensen.com` and added a new section to my `server.tf`:

```plain
provider "cloudflare" {
  version = "~> 2.0"
  email = "zed@whatever.com"
  # Your CloudFlare API token is also read from environment variables
  # api_token = "MY_API_TOKEN"
}

resource "cloudflare_record" "minecraft1" {
  name = "minecraft.zedjensen.com"
  zone_id = "ZONE_ID_HERE"
  value = upcloud_server.minecraft1.ipv4_address
  type = "A"

  depends_on = [upcloud_server.minecraft1]
}
```

As you can probably guess, this resource block tells Terraform to add a new A record to my DNS configuration for `minecraft.zedjensen.com` with my new server’s IP address. The last part, `depends_on`, tells Terraform to wait until it’s done with the server setup, otherwise it’ll try to do them at the same time, before it knows the IP address for the new VM. Don’t forget to put your API token in your environment variables too (this one would be `CLOUDFLARE_API_KEY`).

### Adding scripts for destruction

Lastly, I needed to make sure that when I was shutting my server down, my Minecraft world was safely copied off first. Terraform supports hooks for shutting down as well! I added a final section to the server block of my `server.tf`:

```plain
server {

  // ...

  provisioner "local-exec" {
    when = destroy
    command = "./copy_back.sh ${self.ipv4_address}"
  }
}
```

This is similar to the provisioners I added earlier, but it runs only when I’m destroying my server. In addition, if the command fails, Terraform will abort the destruction of the server, giving me a chance to see what went wrong and make a backup manually if needed. The `copy_back.sh` command I’m using here is just a helper script that copies the world back to my local machine; I also put the entire directory in a zipfile and copy that back for redundancy.

### Trying it out

After completing all the above steps, here’s my completed `server.tf`:

```plain
provider "upcloud" {
  # Your UpCloud credentials are read from the environment variables
  # export UPCLOUD_USERNAME="Username for UpCloud API user"
  # export UPCLOUD_PASSWORD="Password for UpCloud API user"
}

provider "cloudflare" {
  version = "~> 2.0"
  email = "zed@whatever.com"
  api_token = "MY_API_TOKEN"
}

resource "upcloud_server" "minecraft1" {
  # System hostname
  hostname = "minecraft1"

  # Availability zone
  zone = "us-chi1"

  # Number of CPUs and memory in GB
  plan = "2xCPU-4GB"

  storage_devices {
    # OS root disk size
    size = 25

    # Template UUID for Ubuntu 18.04
    storage = "01000000-0000-4000-8000-000030080200"

    tier   = "maxiops"
    action = "clone"
  }

  # Include at least one public SSH key
  login {
    user = "root"
    keys = [
      "MY PUBLIC KEY HERE"
    ]
    create_password = false
  }

  # Configuring connection details
  connection {
    host        = self.ipv4_address
    type        = "ssh"
    user        = "root"
    private_key = file("./id_rsa_upcloud")
  }

  provisioner "remote-exec" {
    inline = [
      "wget http://zedjensen.com/init_minecraft.sh && chmod +x init_minecraft.sh && ./init_minecraft.sh -f && rm init_minecraft.sh"
    ]
  }

  provisioner "local-exec" {
    command = "rsync --delete -r -e 'ssh -F ./ssh_config -i ./id_rsa_upcloud' server root@${self.ipv4_address}:~/minecraft/"
  }

  provisioner "remote-exec" {
    inline = [
      "bash ~/minecraft/start_server.sh"
    ]
  }

  provisioner "local-exec" {
    when = destroy
    command = "./get_backup ${self.ipv4_address}"
  }

  provisioner "local-exec" {
    when = destroy
    command = "./run_rsync ${self.ipv4_address}"
  }
}

resource "cloudflare_record" "minecraft1" {
  name = "minecraft.zedjensen.com"
  zone_id = "ZONE_ID_HERE"
  value = upcloud_server.minecraft1.ipv4_address
  type = "A"

  depends_on = [upcloud_server.minecraft1]
}
```

Now that we’ve defined our server configuration, created scripts to set the remote server up, and added provisioners for startup and takedown, we should be able to run our script and see the magic happen. We’ll use the `-out` option this time so that we only have to review the configuration once.

```plain
zed@zeds-pc:~/minecraft $ terraform plan -out plan

Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.


------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # cloudflare_record.minecraft1 will be created
  + resource "cloudflare_record" "minecraft1" {
      + created_on  = (known after apply)
      + hostname    = (known after apply)
      + id          = (known after apply)
      + metadata    = (known after apply)
      + modified_on = (known after apply)
      + name        = "minecraft.zedjensen.com"
      + proxiable   = (known after apply)
      + proxied     = false
      + ttl         = (known after apply)
      + type        = "A"
      + value       = (known after apply)
      + zone_id     = "ZONE_ID_HERE"
    }

  # upcloud_server.minecraft1 will be created
  + resource "upcloud_server" "minecraft1" {
      + cpu                  = (known after apply)
      + hostname             = "minecraft1"
      + id                   = (known after apply)
      + ipv4                 = true
      + ipv4_address         = (known after apply)
      + ipv4_address_private = (known after apply)
      + ipv6                 = true
      + ipv6_address         = (known after apply)
      + mem                  = (known after apply)
      + plan                 = "2xCPU-4GB"
      + private_networking   = true
      + title                = (known after apply)
      + zone                 = "us-chi1"

      + login {
          + create_password   = false
          + keys              = [
              + "SSH_KEY_HERE"
            ]
          + password_delivery = "none"
          + user              = "root"
        }

      + storage_devices {
          + action  = "clone"
          + address = (known after apply)
          + id      = (known after apply)
          + size    = 25
          + storage = "01000000-0000-4000-8000-000030080200"
          + tier    = "maxiops"
          + title   = (known after apply)
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

------------------------------------------------------------------------

This plan was saved to: plan

To perform exactly these actions, run the following command to apply:
    terraform apply "plan"
```

After reviewing the list of changes to be made, we can apply our changes by following the instructions and running `terraform apply plan`:

```plain
zed@zeds-pc:~/minecraft $ terraform apply plan

upcloud_server.minecraft1: Creating...
upcloud_server.minecraft1: Still creating... [10s elapsed]
upcloud_server.minecraft1: Still creating... [20s elapsed]
upcloud_server.minecraft1: Still creating... [30s elapsed]
upcloud_server.minecraft1: Still creating... [40s elapsed]
upcloud_server.minecraft1: Still creating... [50s elapsed]
upcloud_server.minecraft1: Provisioning with 'remote-exec'...
upcloud_server.minecraft1 (remote-exec): Connecting to remote host via SSH...
upcloud_server.minecraft1 (remote-exec):   Host: 111.222.111.222
upcloud_server.minecraft1 (remote-exec):   User: root
upcloud_server.minecraft1 (remote-exec):   Password: false
upcloud_server.minecraft1 (remote-exec):   Private key: true
upcloud_server.minecraft1 (remote-exec):   Certificate: false
upcloud_server.minecraft1 (remote-exec):   SSH Agent: true
upcloud_server.minecraft1 (remote-exec):   Checking Host Key: false
upcloud_server.minecraft1 (remote-exec): Connected!
upcloud_server.minecraft1 (remote-exec): --2020-07-17 20:36:02--  http://zedjensen.com/init_minecraft.sh
upcloud_server.minecraft1 (remote-exec): Resolving zedjensen.com (zedjensen.com)... 111.222.111.222
upcloud_server.minecraft1 (remote-exec): Connecting to zedjensen.com (zedjensen.com)|111.222.111.222|:80... connected.
upcloud_server.minecraft1 (remote-exec): HTTP request sent, awaiting response... 200 OK
upcloud_server.minecraft1 (remote-exec): Length: 1369 (1.3K) [application/octet-stream]
upcloud_server.minecraft1 (remote-exec): Saving to: 'init_minecraft.sh'

upcloud_server.minecraft1 (remote-exec):       init_   0%       0  --.-KB/s
upcloud_server.minecraft1 (remote-exec): init_minecr 100%   1.34K  --.-KB/s    in 0s

upcloud_server.minecraft1 (remote-exec): 2020-07-17 20:36:03 (205 MB/s) - 'init_minecraft.sh' saved [1369/1369]

upcloud_server.minecraft1 (remote-exec):
upcloud_server.minecraft1: Still creating... [1m0s elapsed]
upcloud_server.minecraft1: Still creating... [1m10s elapsed]
upcloud_server.minecraft1: Still creating... [1m20s elapsed]
upcloud_server.minecraft1: Still creating... [1m30s elapsed]
upcloud_server.minecraft1: Still creating... [1m40s elapsed]
upcloud_server.minecraft1 (remote-exec):
upcloud_server.minecraft1: Still creating... [1m50s elapsed]
upcloud_server.minecraft1: Still creating... [2m0s elapsed]
upcloud_server.minecraft1 (remote-exec):
upcloud_server.minecraft1: Still creating... [2m10s elapsed]
upcloud_server.minecraft1: Provisioning with 'local-exec'...
upcloud_server.minecraft1 (local-exec): Executing: ["/bin/sh" "-c" "rsync --delete -r -e 'ssh -F ./ssh_config -i ./id_rsa_upcloud' server root@111.222.111.222:~/minecraft/"]
upcloud_server.minecraft1 (local-exec): Warning: Permanently added '111.222.111.222' (ECDSA) to the list of known hosts.
upcloud_server.minecraft1: Still creating... [2m20s elapsed]

...

upcloud_server.minecraft1: Still creating... [9m40s elapsed]
upcloud_server.minecraft1: Provisioning with 'remote-exec'...
upcloud_server.minecraft1 (remote-exec): Connecting to remote host via SSH...
upcloud_server.minecraft1 (remote-exec):   Host: 111.222.111.222
upcloud_server.minecraft1 (remote-exec):   User: root
upcloud_server.minecraft1 (remote-exec):   Password: false
upcloud_server.minecraft1 (remote-exec):   Private key: true
upcloud_server.minecraft1 (remote-exec):   Certificate: false
upcloud_server.minecraft1 (remote-exec):   SSH Agent: true
upcloud_server.minecraft1 (remote-exec):   Checking Host Key: false
upcloud_server.minecraft1 (remote-exec): Connected!
upcloud_server.minecraft1: Still creating... [9m50s elapsed]
upcloud_server.minecraft1: Creation complete after 9m51s [id=stuff]
cloudflare_record.minecraft1: Creating...
cloudflare_record.minecraft1: Creation complete after 3s [id=things]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

The state of your infrastructure has been saved to the path
below. This state is required to modify and destroy your
infrastructure, so keep it safe. To inspect the complete state
use the `terraform show` command.

State path: terraform.tfstate
```

Awesome! It takes a while to transfer files over, but once it’s done, my Minecraft server is up and running! To destroy, it’s just as easy:

```plain
zed@zeds-pc:~/minecraft$ terraform destroy
upcloud_server.minecraft1: Refreshing state... [id=things]
cloudflare_record.minecraft1: Refreshing state... [id=stuff]

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # cloudflare_record.minecraft1 will be destroyed
  - resource "cloudflare_record" "minecraft1" {
      - created_on  = "2020-07-15T22:25:04.460564Z" -> null
      - data        = {} -> null
      - hostname    = "minecraft.zedjensen.com" -> null
      - id          = "stuff" -> null
      - metadata    = {
          - "auto_added"             = "false"
          - "managed_by_apps"        = "false"
          - "managed_by_argo_tunnel" = "false"
          - "source"                 = "primary"
        } -> null
      - modified_on = "2020-07-15T22:25:04.460564Z" -> null
      - name        = "minecraft.zedjensen.com" -> null
      - priority    = 0 -> null
      - proxiable   = true -> null
      - proxied     = false -> null
      - ttl         = 1 -> null
      - type        = "A" -> null
      - value       = "111.222.111.222" -> null
      - zone_id     = "ZONE_ID_HERE" -> null
    }

  # upcloud_server.minecraft1 will be destroyed
  - resource "upcloud_server" "minecraft1" {
      - cpu                  = 2 -> null
      - hostname             = "minecraft1" -> null
      - id                   = "things" -> null
      - ipv4                 = true -> null
      - ipv4_address         = "111.222.111.222" -> null
      - ipv4_address_private = "IPv4 addr" -> null
      - ipv6                 = true -> null
      - ipv6_address         = "IPv6 addr" -> null
      - mem                  = 4096 -> null
      - plan                 = "2xCPU-4GB" -> null
      - private_networking   = true -> null
      - title                = "minecraft1 (managed by terraform)" -> null
      - zone                 = "us-chi1" -> null

      - login {
          - create_password   = false -> null
          - keys              = [
              - "SSH_KEY_HERE"
            ] -> null
          - password_delivery = "none" -> null
          - user              = "root" -> null
        }

      - storage_devices {
          - action      = "clone" -> null
          - address     = "virtio:0" -> null
          - backup_rule = {} -> null
          - id          = "stuff" -> null
          - size        = 25 -> null
          - storage     = "01000000-0000-4000-8000-000030080200" -> null
          - tier        = "maxiops" -> null
          - title       = "terraform-minecraft1-disk-0" -> null
        }
    }

Plan: 0 to add, 0 to change, 2 to destroy.

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

cloudflare_record.minecraft1: Destroying... [id=stuff]
cloudflare_record.minecraft1: Destruction complete after 0s
upcloud_server.minecraft1: Destroying... [id=things]
upcloud_server.minecraft1: Provisioning with 'local-exec'...
upcloud_server.minecraft1 (local-exec): Executing: ["/bin/sh" "-c" "./get_backup 209.50.58.100"]
upcloud_server.minecraft1 (local-exec): Warning: Permanently added '209.50.58.100' (ECDSA) to the list of known hosts.
upcloud_server.minecraft1 (local-exec): Warning: Permanently added '209.50.58.100' (ECDSA) to the list of known hosts.
upcloud_server.minecraft1: Still destroying... [id=things, 20s elapsed]
upcloud_server.minecraft1: Provisioning with 'local-exec'...
upcloud_server.minecraft1 (local-exec): Executing: ["/bin/sh" "-c" "./run_rsync 209.50.58.100"]
upcloud_server.minecraft1 (local-exec): Warning: Permanently added '209.50.58.100' (ECDSA) to the list of known hosts.
upcloud_server.minecraft1 (local-exec): Warning: Permanently added '209.50.58.100' (ECDSA) to the list of known hosts.
upcloud_server.minecraft1: Still destroying... [id=things, 30s elapsed]
upcloud_server.minecraft1: Still destroying... [id=things, 40s elapsed]
upcloud_server.minecraft1: Still destroying... [id=things, 50s elapsed]
upcloud_server.minecraft1: Still destroying... [id=things, 1m1s elapsed]
upcloud_server.minecraft1: Destruction complete after 1m7s

Destroy complete! Resources: 2 destroyed.
```

Terraform proved to be a great solution for my Minecraft dilemma, but this could come in handy for lots of other purposes too. Let us know what you use Terraform for!
