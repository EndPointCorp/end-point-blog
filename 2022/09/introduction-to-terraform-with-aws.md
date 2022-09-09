---
author: "Jeffry Johar"
title: "Introduction to Terraform with AWS"
date: 2022-09-09
featured:
  image_url: /blog/2022/09/introduction-to-terraform-with-aws/portdickson.webp
description: Terraform is a tool to enable infrastructure as a code a.k.a IaC
tags:
- terraform
- aws
- linux
- sysadmin
---

![Port Dickson, a Malaysia Beach](/blog/2022/09/introduction-to-terraform-with-aws/portdickson.webp)<br>
Photo by Jeffry Johar
<!--- https://www.pexels.com/photo/malaysia-rocky-beach-hotel-by-the-beach-avilion-13550224/ --->

According to the Merriam-Webster dictionary, the meaning of terraform is to transform (a planet, moon, etc.) so that it is suitable for supporting human life. In the IT world, Terraform is a product from HashiCorp to enable infrastructure as a code (IaC). This is a tool that enables users to define and manage the IT infrastructures in a source code form. Terraform is a declarative tool. It will ensure the desired state as defined by the user. Terraform comes with multiple plugins or providers which enable it to manage a wide variety of cloud providers and technologies such as but not limited to AWS, GCP, Azure, Kubernetes, Dockers and others. This blog will go over on how to use Terraform with AWS. 

### Prerequisites
For this tutorial we will need the following
- An active AWS account
- An internet connection to download required files
- A decent editor such as Vim or Notepad++ to edit the configuration files. 

### Install AWS CLI
We need to set up the AWS CLI (command-line interface) for authentication and authorization to AWS.
 
Execute the following command to install the AWS CLI on macOS:
```plain 
$ curl -O "https://awscli.amazonaws.com/AWSCLIV2.pkg"
$ sudo installer -pkg AWSCLIV2.pkg -target /
```
 
For other OSes see [Amazon’s docs.]( https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
 
 
Execute the following command and enter the [AWS Account and Access Keys.]( https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html)
```plain 
$ aws configure
```

### Install Terraform
We need to install Terraform. It is just a command line tool . Execute the following to install Terraform on macOS
```plain
$ brew tap hashicorp/tap
$ brew install hashicorp/tap/terraform
```
For other OSes see [Terraform’s docs.](https://learn.hashicorp.com/tutorials/terraform/install-cli)

### Create the Terraform configuration file
Before we can create any Terraform configuration file for a project, we need to create a directory. This is because Terraform will pick up whatever configurations in the current directory and will store the state of the created infrastructure in a file in the directory. The name of the directory can be anything. For this tutorial we are going to name it terraform-aws. Create the directory and get into it. 
```plain 
$ mkdir terraform-aws
$ cd terraform-aws
```
 
Create the following file and name it `main.tf`. This is the main configuration file for our Terraform project. This configuration will provision an EC2 instance, install Amazon Linux 2 as the OS and  install Nginx as the web server.  The comments starts with the # sign. They describe each sections’ function . For simplicity, the configuration is using the default VPC that comes with the selected AWS region.
```plain
# Set AWS as the Cloud Provider
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
    cidr_blocks = ["0.0.0.0/0"] # make this your IP/IP Range
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


# AWS EC2 configuration. The user_data contains the script to install Nginx
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
This will initialize the project by downloading the required plugin. For this example it will download the AWS plugin. Initialize the project by executing the following command:
```plain
$ terraform init
```

### Validate the configuration file
This will check the syntax of the configuration file
```plain
$ terraform validate
```

### Apply the configuration 
This will make Terraform create and provision the resources specified in the configuration file. It will ask to review the configuration and answer yes to proceed. Take note of the public IP of the provisioned EC2.
```plain
$ terraform apply
```

Sample output:
![Terraform Apply output](/blog/2022/09/introduction-to-terraform-with-aws/blog08-01.webp)<br>

 
### Access the provisioned EC2 and Nginx
Use the key_name that is configured in the `main.tf` and the generated public IP address to SSH to the EC2 Instance. 
```plain
$ ssh -i kaptenjeffry.pem ec2-user@46.137.236.88
```

Use the generated public IP address in a web brower to access the Nginx service. Please ensure to use `http` protocol since the Nginx is running on port 80. 
![Nginx in a web browser](/blog/2022/09/introduction-to-terraform-with-aws/blog08-02.webp)<br>


### Conclusion

That's all folks. This is the bare minimum Terraform configuration to quickly deploy an EC2 instance at AWS. For more cool stuffs you can have a visit to the [Terraform main documentation for AWS](https://registry.terraform.io/providers/hashicorp/aws/latest/docs). Have a nice day :)


