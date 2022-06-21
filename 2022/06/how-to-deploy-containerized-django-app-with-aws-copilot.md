---
author: "Jeffry Johar"
title: "How to deploy containerized Django app with AWS Copilot"
date: 2022-06-21
tags:
- Docker
- AWS
- copilot
- django
- python
- ECS
- AWS Copilot
---

![Photo of 2 pilots](/blog/2022/06/how-to-deploy-containerized-django-app-with-aws-copilot/pilot.webp)
Photo from [pxhere.com](https://pxhere.com/en/photo/609377)

### The blue pill or the red pill 
Generally there are 2 major options at AWS when it comes to deployment of containerized applications. You can either go for EKS or ECS. EKS (Elastic Kubernetes Service ) is the managed Kubernetes service by AWS . ECS ( Elastic Container Service ) on the other hand is another option to manage your containerized application at AWS. ECS is the AWS own way of doing things. Go to the following link if you want to know more about EKS and ECS [Making Sense of AWS Container Service](https://aws.amazon.com/blogs/containers/amazon-ecs-vs-amazon-eks-making-sense-of-aws-container-services/)

### The chosen one and the sidekick
Your clients or you have chosen **ECS** and now you have to find a nice and easy way to deploy your containerized application on it. There are quite a number of resources from AWS that are needed for your application to live on ECS such as VPC ( Virtual Data Center), Security Group ( Firewall ), EC2 ( Virtual Machine), Load balancer and others. To create these resources manually is cumbersome thus AWS has came out with a tool that can automate the creation of all of them. The tool is known as **AWS Copilot** and we are going to learn how to use it. In this blog we are going to walkthrough on how to deploy a containerized Django app to ECS by using AWS Copilot.

### The how-to
#### 1. Docker 
The Docker or Docker Desktop is required for building the Docker image later. Please refer to my previous blog on how to install Docker Desktop [Getting started with Docker and Kubernetes on macOS](https://www.endpointdev.com/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/)

#### 2. AWS CLI
The docker AWS CLI for the authentication and authorization to AWS.

- Installation

Execute the following command to install the AWS CLI at macOS. For other OS please go here [AWS CLI Installation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) 
```bash
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```
 
- Configuration

Execute the following command and enter the [AWS Account and Access Keys](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html)
```bash
aws configure
```

#### 3. AWS Copilot CLI
The main character; AWS Copilot. 

- Installation

Install AWS Copilot by using brew for macOS. For other method or OS please go here [AWS Copilot Installation](https://aws.github.io/copilot-cli/docs/getting-started/install/)
```bash
brew install aws/tap/copilot-cli
```

#### 4. The Django project

- Create a Django project by using a Python Docker Image. Clone this Git Project to get the Dockerfile, docker-compose.yaml and pip requirement.txt
```bash
git clone https://github.com/aburayyanjeffry/django-copilot.git
```

- Get into the django-pilot directory and execute the docker-compose to create a  Django project named "mydjango". 
```bash
cd django-copilot
docker-compose run web django-admin startproject mydjango .
```

- Edit mydjango setting to allow all hostname for its URL. This is required because by default AWS will generate a random URL for the application
```bash
vim mydjango/settings.py
```

- Find the following variable and set the value as follows
```yaml
ALLOWED_HOSTS = ['*']
```

#### The Deployment with AWS Copilot
- Create an AWS Copilot ```Application```. This is a grouping of services like Web App Or DB, Environtments ( DEV, QA, PRD) and CI/CD pipelines. Execute the following command to create an Application with the name of ```mydjango```.
```bash 
copilot init -a mydjango
```

- Select the Workload type. Since this Django is an internet facing app we will choose the ```Load Balanced Web Service```
```plain
Which workload type best represents your architecture?  [Use arrows to move, type to filter, ? for more help]
    Request-Driven Web Service  (App Runner)
  > Load Balanced Web Service   (Internet to ECS on Fargate)
    Backend Service             (ECS on Fargate)
    Worker Service              (Events to SQS to ECS on Fargate)
    Scheduled Job               (Scheduled event to State Machine to Fargate)
```

- Give the Workload a name. We going to name it ```mydjango-web```
```plain
Workload type: Load Balanced Web Service

  What do you want to name this service? [? for help] mydjango-web
```

- Select the Dockerfile in the current directory
```plain
Which Dockerfile would you like to use for mydjango-web?  [Use arrows to move, type to filter, ? for more help]
  > ./Dockerfile
    Enter custom path for your Dockerfile
    Use an existing image instead
```

- Accept to create a test environtment. 
```plain
All right, you're all set for local development.

  Would you like to deploy a test environment? [? for help] (y/N) y
```

- Wait and see. At the end of the deployment you will get the URL of your application. Open it in a browser. 

Sample output
![Photo of 2 pilots](/blog/2022/06/how-to-deploy-containerized-django-app-with-aws-copilot/sample.webp)


Sample view from a browser
![Photo of 2 pilots](/blog/2022/06/how-to-deploy-containerized-django-app-with-aws-copilot/browser.webp)


- Now let's migrate some data, create a superser and try to login. The Django app comes with a sqlite DB. Execute the following command to get a terminal for the Django app
```bash
copilot svc exec
```

- Once in the terminal, execute the following to migrate the inital data dan to create the superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

Sample output
![db migration](/blog/2022/06/how-to-deploy-containerized-django-app-with-aws-copilot/sample-db.webp)

- Now you may access the admin page at the URL/admin and login by using the created credential.

![login page 1](/blog/2022/06/how-to-deploy-containerized-django-app-with-aws-copilot/login01.webp) 
![successful login](/blog/2022/06/how-to-deploy-containerized-django-app-with-aws-copilot/login02.webp) 

- A Mini cheet sheet

| AWS Copilot commands          | Remarks                               | 
|-------------------------------|---------------------------------------|
| copilot app ls                | To list available Applications        |
| copilot app show -n appname   | To get the details of an Application  |
| copilot app delete -n appname | To delete an Application              |
| copilot svc ls                | To list available Services            |
| copilot svc show -n svcname   | To get the details of a Service       |
| copilot svc delete -n svcname | To delete a Service                   |

### The End
That is all folks. AWS Copilot is a tool to automate the deployment of AWS infrastructure for our containerized application needs. It moves away most of the worries of the infrastructure and enables the application owner to focus more on the application development. For further info of AWS Copilot go here https://aws.github.io/copilot-cli/

