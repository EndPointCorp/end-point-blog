---
author: "Jeffry Johar"
title: "How to deploy Django App and Aurora Serverless DB with AWS Copilot"
date: 2022-06-26
tags:
- docker
- containers
- aws
- aurora
- postgresql
---
![Photo of an aurora](/blog/2022/06/how-to-deploy-django-app-and-aurora-serverless-db-with-aws-copilot/aurora-banner.webp)
Photo by Виктор Куликов

<!-- Photo licensed under Legal Simplicity (public domain) from https://www.pexels.com/photo/white-tent-on-green-grass-field-under-aurora-borealis-during-night-time-8601966/  -->




AWS Copilot has the capability to provision external DB for its containerized work load. The options for the DB are DynamoDB ( NoSQL), Aurora Serverless DB ( SQL) and S3 Buckets. For this blog we are going to provision and use Aurora Serverless DB with a containerized Django app. Aurora serverless DB comes with 2 options for its engine. The engine could either be MySQL or PostgreSQL. 
Watch the following 1++ minute video to get the basic idea of Aurora Serverless DB. [Introduction to Amazon Aurora](https://www.youtube.com/watch?v=FzxqIdIZ9wc)


We are going to work with the same  Django application from [my previous article](https://www.endpointdev.com/blog/2022/06/how-to-deploy-containerized-django-app-with-aws-copilot/).
Previously the Django application was deployed with SQLite as the DB. The application’s data is stored in the SQLite which resides internally inside the container. The problem with this set up is the data is not persistent. Whenever we redeploy the application, the container will get a new filesystem. Thus all old data will be removed automatically. Now we are moving away the application’s data externally so that the life of the data does not depend on the container. We are going to put the data on the Aurora Serverless DB with PostgreSQL as the engine. 

![django with sqlite](/blog/2022/06/how-to-deploy-django-app-and-aurora-serverless-db-with-aws-copilot/django-sqlite.webp)
<p style="text-align: center;"><B>Django with SQLite as the internal DB</B></p>
<br>

![django with aurora](/blog/2022/06/how-to-deploy-django-app-and-aurora-serverless-db-with-aws-copilot/django-aurora.webp)
<p style="text-align: center;"><B>Django with Aurora Serverless DB as the external DB</B></p>
<br>



### The Prerequisites

Docker, AWS CLI and AWS Copilot CLI are required . Please refer to my previous article if you required the guide on how to install these tools.

### The Django Project
Create a Django project by using a Python Docker Image. You can clone my Git project to get the Dockerfile, docker-compose.yaml and requirements.txt that I’m using.

```plain
$ git clone https://github.com/aburayyanjeffry/django-copilot.git django-aurora
```

Go to the django-aurora directory and execute docker-compose to create a Django project named “mydjango”.

```plain
$ cd django-aurora
$ docker-compose run web django-admin startproject mydjango .
```

### The Deployment with AWS Copilot


Execute the following command to create a AWS Copilot Application with the name of mydjango, a load balance container with the name of django-web which is made from  the Dockerfile in the current directory.  

```plain
$ copilot init \
-a mydjango \
-t "Load Balanced Web Service" -n django-web \
-d ./Dockerfile
```

Answer N to the following question. We want to defer the deployment until we have set up the DB. 

```plain
All right, you're all set for local development.

 Would you like to deploy a test environment? [? for help] (y/N) N
```
    
We need to create an environment for our application. Execute the following to create an environment named ```test``` for the mydjango application with the default setting. 

```plain
$ copilot env init \
--name test \
--profile default \
--app mydjango \
--default-config
```

Now we are going to generate a config for our Aurora Serveless DB.  Basically this is the cloudformation template that will be use to create the Aurora Serverless DB. Execute the following to generate the configuration for a Aurora cluster named mydjango-db that will be use for django-web application. The Aurora cluster will be using the PostgreSQL engine and database name will be mydb.

```plain
$ copilot storage init \
-n mydjango-db \
-t Aurora -w \
django-web \
--engine PostgreSQL \
--initial-db mydb
```    

Take note of the injected environment variable name. This is where the Database info and credential are stored. We need to use this variable in the following steps. 

```plain
✔ Wrote CloudFormation template at copilot/django-web/addons/mydjango-db.yml

Recommended follow-up actions:
 - Update django-web's code to leverage the injected environment variable MYDJANGODB_SECRET.
```    

Edit mydjango/settings.py to include the following. Please replace the DATABASE section with the following . Use the injected environment variable  that we got previously to the function for getting the DBINFO variables.  

```plain
from pathlib import Path
import os
import json
.
.
ALLOWED_HOSTS = ['*']
.
.

DBINFO = json.loads(os.environ.get('MYDJANGODB_SECRET', '{}'))
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'HOST': DBINFO['host'],
       'PORT': DBINFO['port'],
       'NAME': DBINFO['dbname'],
       'USER': DBINFO['username'],
       'PASSWORD': DBINFO['password'],
   }
}
```

Deploy the application

```plain
$ copilot deploy --name django-web
```    

Get the terminal of the service. 

```plain
$ copilot svc exec
```

Execute the following commands to migrate the initial DB and to create a superuser id

```plain
$ python manage.py migrate
$ python manage.py createsuperuser
```

Execute the following to check on the environment variable. Take note of the MYDJANGODB_SECRET variable. It is the variable that holds the DB information. 

```plain
env | grep MYDJANGODB_SECRET
```

### How to query Aurora Serverless DB

We could use the Query Editor at AWS Console for RDS to query Aurora Serverless DB. Let’s try to do this. Go to the following link. 
https://console.aws.amazon.com/rds/home


Click the DB base on the DB identifier from the injected environment variable and click Modify
![RDS Main](/blog/2022/06/how-to-deploy-django-app-and-aurora-serverless-db-with-aws-copilot/rds-02-modify.webp)

Click the check box for API
![RDS api](/blog/2022/06/how-to-deploy-django-app-and-aurora-serverless-db-with-aws-copilot/rds-03-api.webp)

Select Apply Immediately
![RDS immediately](/blog/2022/06/how-to-deploy-django-app-and-aurora-serverless-db-with-aws-copilot/rds-04-immediately.webp)

Click Query Editor and fill in the Database information from the injected environment variable. 
![RDS info](/blog/2022/06/how-to-deploy-django-app-and-aurora-serverless-db-with-aws-copilot/rds-05-dbinfo.webp)

Now you may use the Query Editor to query the DB. Execute the following query to list all tables in the database. 
![RDS info](/blog/2022/06/how-to-deploy-django-app-and-aurora-serverless-db-with-aws-copilot/rds-06-query.webp)


### The End

That’s all, folks. We have deployed a containerized Django application and an Aurora Serverless DB with AWS Copilot. For further info on AWS Copilot [visit its website](https://aws.github.io/copilot-cli/).
