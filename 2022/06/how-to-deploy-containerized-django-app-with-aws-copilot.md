---
author: "Jeffry Johar"
title: "How to deploy a containerized Django app with AWS Copilot"
date: 2022-06-21
github_issue_number: 1877
tags:
- docker
- aws
- python
- django
---

![Photo of 2 pilots](/blog/2022/06/how-to-deploy-containerized-django-app-with-aws-copilot/pilots.webp)

Photo from [pxhere.com](https://pxhere.com/en/photo/609377)

### The blue pill or the red pill 

Generally there are 2 major options at AWS when it comes to deployment of containerized applications. You can either go for EKS or ECS. EKS (Elastic Kubernetes Service) is the managed Kubernetes service by AWS. ECS (Elastic Container Service), on the other hand, is AWS's own way to manage your containerized application. You can learn more about EKS and ECS [on the AWS website](https://aws.amazon.com/blogs/containers/amazon-ecs-vs-amazon-eks-making-sense-of-aws-container-services/).

For this post we will use ECS.

### The chosen one and the sidekick

Your clients or you have chosen **ECS** and now you have to find a nice and easy way to deploy your containerized application on it. There are quite a number of resources from AWS that are needed for your application to live on ECS, such as VPC (Virtual Private Cloud), Security Group (Firewall), EC2 (Virtual Machine), Load balancer, and others. Creating these resources manually is cumbersome so AWS has came out with a tool that can automate the creation of all of them. The tool is known as **AWS Copilot** and we are going to learn how to use it.

### Install Docker 

Docker or Docker Desktop is required for building the Docker image later. Please refer to my previous article on [how to install Docker Desktop on macOS](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/), or [follow Docker's instructions](https://docs.docker.com/get-docker/) for Linux and Windows.

### Set up AWS CLI

We need to set up the Docker AWS CLI for authentication and authorization to AWS.

Execute the following command to install the AWS CLI on macOS. For other OSes see [Amazon's docs](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

```plain
$ curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
$ sudo installer -pkg AWSCLIV2.pkg -target /
```

Execute the following command and enter the [AWS Account and Access Keys](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html).

```plain
$ aws configure
```

### Install AWS Copilot CLI

Now it's time for the main character: AWS Copilot. 

Install AWS Copilot with Homebrew for macOS. See [AWS Copilot Installation](https://aws.github.io/copilot-cli/docs/getting-started/install/) for other platforms.

```plain
$ brew install aws/tap/copilot-cli
```

### The Django project

Create a Django project by using a Python Docker Image. You can clone my Git project to get the `Dockerfile`, `docker-compose.yaml` and `requirements.txt` that I'm using.

```plain
$ git clone https://github.com/aburayyanjeffry/django-copilot.git
```

Go to the `django-pilot` directory and execute `docker-compose` to create a Django project named "mydjango". 

```plain
$ cd django-copilot
$ docker-compose run web django-admin startproject mydjango .
```

Edit `mydjango/settings.py` to allow all hostnames for its URL. This is required because by default AWS will generate a random URL for the application. Find the following variable and set the value as follows:

```python
ALLOWED_HOSTS = ['*']
```

### The Deployment with AWS Copilot

Create an AWS Copilot `Application`. This is a grouping of services like Web App or DB, Environments (DEV, QA, PRD), and CI/CD pipelines. Execute the following command to create an Application with the name of `mydjango`.

```plain 
$ copilot init -a mydjango
```

Select the Workload type. Since this Django is an internet-facing app we will choose the `Load Balanced Web Service`.

```plain
Which workload type best represents your architecture?  [Use arrows to move, type to filter, ? for more help]
    Request-Driven Web Service  (App Runner)
  > Load Balanced Web Service   (Internet to ECS on Fargate)
    Backend Service             (ECS on Fargate)
    Worker Service              (Events to SQS to ECS on Fargate)
    Scheduled Job               (Scheduled event to State Machine to Fargate)
```

Give the Workload a name. We are going to name it `mydjango-web`.

```plain
Workload type: Load Balanced Web Service

  What do you want to name this service? [? for help] mydjango-web
```

Select the Dockerfile in the current directory.

```plain
Which Dockerfile would you like to use for mydjango-web?  [Use arrows to move, type to filter, ? for more help]
  > ./Dockerfile
    Enter custom path for your Dockerfile
    Use an existing image instead
```

Accept to create a test environment. 

```plain
All right, you're all set for local development.

  Would you like to deploy a test environment? [? for help] (y/N) y
```

Wait and see. At the end of the deployment you will get the URL of your application. Open it in a browser. 

![Sample output](/blog/2022/06/how-to-deploy-containerized-django-app-with-aws-copilot/sample.webp)

![Sample view from a browser](/blog/2022/06/how-to-deploy-containerized-django-app-with-aws-copilot/browser.webp)

Now let's migrate some data, create a superuser, and try to login. The Django app comes with a SQLite database. Execute the following command to get a terminal for the Django app:

```plain
$ copilot svc exec
```

Once in the terminal, execute the following to migrate the initial data and to create the superuser:

```plain
$ python manage.py migrate
$ python manage.py createsuperuser
```

![db migration](/blog/2022/06/how-to-deploy-containerized-django-app-with-aws-copilot/sample-db.webp)

Now you may access the admin page and login by using the created credential.

![login page 1](/blog/2022/06/how-to-deploy-containerized-django-app-with-aws-copilot/login01.webp) 

![successful login](/blog/2022/06/how-to-deploy-containerized-django-app-with-aws-copilot/login02.webp) 

A Mini cheat sheet:

| AWS Copilot commands          | Remarks                               | 
|-------------------------------|---------------------------------------|
| copilot app ls                | To list available Applications        |
| copilot app show -n appname   | To get the details of an Application  |
| copilot app delete -n appname | To delete an Application              |
| copilot svc ls                | To list available Services            |
| copilot svc show -n svcname   | To get the details of a Service       |
| copilot svc delete -n svcname | To delete a Service                   |

### The End

That's all, folks. AWS Copilot is a tool to automate the deployment of AWS infrastructure for our containerized application needs. It takes away most of the worries about infrastructure and enables the application owner to focus more on the application development. For further info on AWS Copilot [visit its website](https://aws.github.io/copilot-cli/).

