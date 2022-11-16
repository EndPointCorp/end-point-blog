---
author: "Jeffry Johar"
title: "Introduction to Terraform with AWS"
date: 2022-11-09
featured:
  image_url: /blog/2022/11/introduction-to-terraform-with-aws/portdickson.webp
description: Terraform is a tool to enable infrastructure as code.
github_issue_number: 1916
tags:
- terraform
- aws
- linux
- sysadmin
---

![Port Dickson, a Malaysian Beach. Rocks in the forground jut out into an inlet, across which is a line of red-roofed houses.](/blog/2022/11/introduction-to-terraform-with-aws/portdickson.webp)<br>
Photo by Jeffry Johar

<!-- https://www.pexels.com/photo/malaysia-rocky-beach-hotel-by-the-beach-avilion-13550224/ -->

Terraform is a tool from HashiCorp to enable infrastructure as code (IaC). With it users can define and manage IT infrastructure in source code form.

Terraform is a declarative tool. It will ensure the desired state as defined by the user.

Terraform comes with multiple plugins or providers which enable it to manage a wide variety of cloud providers and technologies such as but not limited to AWS, GCP, Azure, Kubernetes, Docker and others.

This blog will go over how to use Terraform with AWS.

### Prerequisites

For this tutorial we will need the following:

- An active AWS account.
- An internet connection to download required files.
- A decent editor such as Vim or Notepad++ to edit the configuration files.

### Install AWS CLI

We need to set up the AWS CLI (command-line interface) for authentication and authorization to AWS.

Execute the following command to install the AWS CLI on macOS:

```plain
$ curl -O https://awscli.amazonaws.com/AWSCLIV2.pkg
$ sudo installer -pkg AWSCLIV2.pkg -target /
```

For other OSes see [Amazon’s docs](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

Execute the following command and enter the [AWS Account and Access Keys](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html):

```plain
$ aws configure
```

### Install Terraform

We need to install Terraform. It is just a command line tool. Execute the following to install Terraform on macOS:

```plain
$ brew tap hashicorp/tap
$ brew install hashicorp/tap/terraform
```

For other OSes see [Terraform’s installation docs](https://learn.hashicorp.com/tutorials/terraform/install-cli).

### Create the Terraform configuration file

Before we can create any Terraform configuration file for a project, we need to create a directory where Terraform will pick up any configuration in the current directory and will store the state of the created infrastructure in a file.

The name of the directory can be anything. For this tutorial we are going to name it `terraform-aws`. Create the directory and `cd` to it:

```plain
$ mkdir terraform-aws
$ cd terraform-aws
```

Create the following file and name it `main.tf`. This is the main configuration file for our Terraform project. This configuration will provision an EC2 instance, install Amazon Linux 2 as the OS and install Nginx as the web server. The comments start with a hash `#`. They describe each section's function. For simplicity, the configuration is using the default VPC that comes with the selected AWS region.

```plain
# Set AWS as the cloud provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

# Set AWS region
provider "aws" {
  region = "ap-southeast-1"
}

# Set the default VPC as the VPC
resource "aws_default_vpc" "main" {
  tags = {
    Name = "Default VPC"
  }
}

# Set AWS security group to allow SSH and HTTP
resource "aws_security_group" "ssh_http" {
  name        = "ssh_http"
  description = "Allow SSH and HTTP"
  vpc_id      = aws_default_vpc.main.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # make this your IP address or range
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


# AWS EC2 configuration
# The user_data contains the script to install Nginx
resource "aws_instance" "app_server" {
  ami           = "ami-0b89f7b3f054b957e"
  instance_type = "t2.micro"
  key_name = "kaptenjeffry"
  vpc_security_group_ids = [aws_security_group.ssh_http.id]
  user_data = <<EOF
   #!/bin/bash
   sudo yum update
   sudo amazon-linux-extras install nginx1 -y
   sudo systemctl start nginx
  EOF

  tags = {
    Name = "Nginx by Terraform"
  }
}

# EC2 Public IP
output "app_server_public_ip" {
  description = "Public IP address of app_server"
  value       = aws_instance.app_server.public_ip
}
```

### Initialize the project

Initialize the project by downloading the required plugin. For this example, it will download the AWS plugin. Initialize the project by executing the following command:

```plain
$ terraform init
```

### Validate the configuration file

Check the syntax of the configuration file:

```plain
$ terraform validate
```

### Apply the configuration

This will make Terraform create and provision the resources specified in the configuration file. It will ask to review the configuration; answer yes to proceed. Take note of the public IP of the provisioned EC2.

```plain
$ terraform apply
```

Sample output:

![Terraform Apply output. Highlighted is a line reading "Enter a value:". "yes" has been entered as the answer. Also highlighted is a line under "Outputs:" reading "app_server_public_ip = "46.137.236.88".](/blog/2022/11/introduction-to-terraform-with-aws/blog08-01.webp)

### Access the provisioned EC2 and Nginx

Use the `key_name` that is configured in `main.tf` and the generated public IP address to SSH to the EC2 Instance.

```plain
$ ssh -i kaptenjeffry.pem ec2-user@46.137.236.88
```

Use the generated public IP address in a web browser to access the Nginx service. Please make sure to use `http` protocol since the Nginx is running on port 80.

![The default Nginx page in a web browser. The top of the page reads "Welcome to nginx on Amazon Linux!"](/blog/2022/11/introduction-to-terraform-with-aws/blog08-02.webp)

### Conclusion

That's all, folks. This is the bare minimum Terraform configuration to quickly deploy an EC2 instance at AWS.

For more cool stuffs you can visit the [Terraform main documentation for AWS](https://registry.terraform.io/providers/hashicorp/aws/latest/docs).

Have a nice day :)
