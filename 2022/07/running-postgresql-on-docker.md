---
author: Jeffry Johar
title: "Running PostgreSQL on Docker"
date: 2022-07-27
tags:
- Docker
- PostgresSQL
---
![An elephant in a jungle](/blog/2022/07/running-postgresql-on-docker/elephant.webp)

<!-- Photo licensed under CC0 (public domain) from https://pxhere.com/en/photo/1366104 -->
### Introduction
PostgreSQL or in short it is just known as Postgres, is an open-source relational database. The officially supported platforms are the major operating systems such as Windows, Linux, BSD, MacOS and others. Besides running  as an executable binary in an operating system, Postgres is able to be executed as a containerized application on Docker! In this article we are going to walk through the Postgres implementation on Docker. 

### Prerequisites
- Docker or Docker Desktop is required to execute the Postgres container image. Please refer to [my previous article](https://www.endpointdev.com/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/) if you need help with Docker installation. 
- Internet access is required to pull or download the Postgres container image from the Docker Hub https://hub.docker.com
- A decent text editor such as vim or notepad++ to create the configuration yaml files. 


### Get to know the official  Postgres Image
Go to Docker Hub https://hub.docker.com and search for "postgres". 
![docker hub](/blog/2022/07/running-postgresql-on-docker/docker01.webp)

There is a lot of images made for PostgreSQL at Docker Hub. If you don't have any special requirement or need, it is best to select the official image. This is the image maintained by the Docker PostgresSQL Community. 
![docker hub2](/blog/2022/07/running-postgresql-on-docker/docker02.webp)

This page describes the Postgres Image, how it was made and how to use it. From this page we know the image name and the required parameters. These are essential information for starting a docker image as we will see in the following steps.

### Run the Postgres image as a basic Postgres container
Execute the following command to execute the bare minimum setup of  Postgres  on Docker 
```plain
docker run --name basic-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```
Where: 
- ```--name basic-postgres``` set the container name to basic-postgres
- ```-e POSTGRES_PASSWORD=mysecretpassword``` set the password of the default user ```postgres```
- ```-d``` run the container in detached mode or in other words in the background
- ```postgres``` use the postgres. By default it will get the image from https://hub.docker.com


Execute ```docker ps``` to check on running containers on Docker. We should see our basic-postgres container running.  ```docker ps``` is like ```ps -ef``` at Linux/Unix Operating System which is to list all running applications. 

Sample Output:
![docker hub](/blog/2022/07/running-postgresql-on-docker/term01.webp)

### Working with the Postgres container
Just as Postgres on an operating system, Postgres on Docker comes with the psql client to access the Postgres database. To access the psql client in the Postgerss container execute the following command

```plain
docker exec -it basic-postgres psql -U postgres
```
Where:
- ```exec -it``` to execute something interactive with a terminal
- ```basic-postgres``` to specify which container
-```psql -U postgres``` is the psl command with its switch to specify the Postgres user

Now we are able to execute any psql command. Let's try few Postgres commands and import the famous dvdrental database to our Postgres. 

List all available database.
```plain
\l
```

Create a database named dvdrental.
```plain
create database dvdrental;
```

List all available databases. We should see the created dvdrental database
```plain
\l
```

Quit from psql
```plain
\q
```

Download the dvdrental database backup from the www.postgresqltutorial.com and unzip it
```plain
curl -O https://www.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip && unzip dvdrental.zip
```

Execute the following command to import the data.  This command will restore the dvdrental.tar backup to our Postgres database.
```plain
docker exec -i basic-postgres pg_restore -U postgres -v -d dvdrental < dvdrental.tar
```
Where:
- ```exec -i``` to execute something interactive 
- ```basic-postgres``` to specify which container
- ```pg_restore -U postgres -v -d dvdrental < dvdrental.tar``` is the pg_restore command to restore dvdrental.tar to a database named dvdrental in Postgres. 

Login to dvdrental database 
```plain
docker exec -it basic-postgres psql -U postgres -d dvdrental
```
Where:
- ```exec -it``` to execute something interactive with a terminal
- ```basic-postgres``` to specify which container
- ```psql -U postgres -d dvdrental``` is the psl command with its switch to specify the Postgres user and the dvdrental database


List all tables by describing the tables in the dvdrental database
```plain
\dt
```

List the first 10 actor from the actor table
```plain
select * from actor limit 10;
```

Quit from psql
```plain
\q
```

Gracefully stop the Docker Container
```plain
docker stop basic-postgres
```

If you don’t need it anymore you can delete the container
```plain
docker rm basic-postgres 
```

Sample Output:
![psql](/blog/2022/07/running-postgresql-on-docker/psql01.webp)
![psql](/blog/2022/07/running-postgresql-on-docker/psql02.webp)


### Run Postgres Image as a “real world” Postgres Container
The basic Postgres Container is only good for learning or testing the Postgres Container. It requires more features to be able to serve as a working database for the real world application. We will add 2 more features to make it useable
- Persistence Storage: By default the container filesystem is ephemeral. What this means is whenever we restart a terminated or deleted container, it will get an all new fresh filesystem and all previous data will be wiped clean.  This is not suitable for database systems. To be a working database, we need to add a persistent filesystem to the container
- Port Forward from Host to Container: Container network is isolated, thus making it inaccessible from the outside world. A database is no use if it can’t be accessed. To make it accessible we need to port forward the host operating system port to the container port. 


Let’s start building a “real world” Postgres Container. Firstly we need to create the persistence storage or in Docker this is known as volume.
Execute the following command to create a volume named pg-data
```plain
docker volume create pg-data
```

List all Docker volumes and ensure that pg-data was created 
```plain
docker volume ls | grep pg-data
```

Execute the following command to run a Postgres Container with a persistence storage and a port forward 
```plain
docker run --name real-postgres \
-e POSTGRES_PASSWORD=mysecretpassword \
-v pg-data:/var/lib/postgresql/data \
-p 5432:5432 \
-d \
postgres
```
Where:
- ```--name real-postgres``` set the container name
- ```-e POSTGRES_PASSWORD=mysecretpassword``` set the password of the default user ```postgres```
- ```-v pg-data:/var/lib/postgresql/data``` mount the pg-data volume as the postgres data directory. 
- ```-p 5432:5432 ``` forward from port 5432 of host operating system to port 5432 of container 
- ```-d``` run the container in detached mode or in other words in the background
- ```postgres``` use the postgres. By default it will get the image from https://hub.docker.com

Execute ```docker ps``` to check on running containers on Docker. Take note that the real-postgres has port forwarding information. 

Now we are going to try to access the Postgres container from a psql client from the host operating system.
```plain
psql -h localhost -p 5432 -U postgres
```

Sample Output:
![docker hub](/blog/2022/07/running-postgresql-on-docker/term02.webp)

### Cleaning up the running container 
Stop the container
```plain
docker stop real-postgres
```

Delete the container
```plain
docker rm real-postgres
```


Delete the volume
```plain
docker volume rm pg-data
``` 


### Managing Postgres Container with Docker Compose
Managing a Container with a long list of arguments at Docker CLI command  is tedious and error prone. Instead of the Docker CLI command we could use Docker Compose. Docker Compose is a tool for managing containers from a YAML manifest file. 


Create the following file with the name of docker-compose.yaml. 
```yaml
version: '3.1'
services:
  db:
    container_name: real-postgres2
    image: postgres
    restart: always
    ports:
      - "5432:5432"
    environment:
      POSTGRES_PASSWORD: mysecretpassword
    volumes:
      - pg-data-2:/var/lib/postgresql/data
volumes:
  pg-data-2:
    external: false
```


To start Postgres container with Docker Compose is to execute the following command in the same location of the docker-compose.yaml 
```plain
docker-compose up -d
```

Execute ```docker ps``` to check on running containers on Docker. Take note that the real-postgres2 created by Docker Compose

To stop Postgres container with Docker Compose is to execute the following command in the same location of the docker-compose.yaml
```plain
docker-compose down
```

Sample Output:
![docker hub](/blog/2022/07/running-postgresql-on-docker/term03.webp)

### Conclusion
That’s all folks. We have successfully implemented PostgreSQL on Docker. Now we are able to reap the benefits of Container technology for PostgresSQL such as but not limited to portability, agility and better management.
