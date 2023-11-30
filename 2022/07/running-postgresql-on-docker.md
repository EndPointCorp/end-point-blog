---
author: Jeffry Johar
title: "Running PostgreSQL on Docker"
github_issue_number: 1884
date: 2022-07-27
tags:
- docker
- postgres
- containers
---

![An elephant in a jungle](/blog/2022/07/running-postgresql-on-docker/elephant.webp)

<!-- Photo licensed under CC0 (public domain) from https://pxhere.com/en/photo/1366104 -->

### Introduction

PostgreSQL, or Postgres, is an open-source relational database. It is officially supported on all the major operating systems: Windows, Linux, BSD, MacOS, and others.

Besides running as an executable binary in an operating system, Postgres is able to run as a containerized application on Docker! In this article we are going to walk through the Postgres implementation on Docker.

### Prerequisites

- Docker or Docker Desktop. Please refer to [my previous article](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/) for help with Docker installation.
- Internet access is required to pull or download the Postgres container image from the Docker Hub.
- A decent text editor, such as Vim or Notepad++, to create the configuration YAML files.


### Get to know the official Postgres Image

Go to [Docker Hub](https://hub.docker.com) and search for "postgres".

![Docker Hub website search screen shot](/blog/2022/07/running-postgresql-on-docker/docker01.webp)

There are a lot of images for PostgreSQL at Docker Hub. If you don't have any special requirements, it is best to select the official image. This is the image maintained by the Docker PostgreSQL Community.

![Docker Hub website search result for postgres](/blog/2022/07/running-postgresql-on-docker/docker02.webp)

The [page that search result links to](https://hub.docker.com/_/postgres) describes the Postgres image, how it was made and how to use it. From this page we know the image name and the required parameters. This is essential information for starting a Docker image, as we will see in the following steps.

### Run the Postgres image as a basic Postgres container

The following command is the bare minimum for running Postgres on Docker:

```plain
docker run --name basic-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```

Where:

- `--name basic-postgres` sets the container name to basic-postgres,
- `-e POSTGRES_PASSWORD=mysecretpassword` sets the password of the default user `postgres`,
- `-d` runs the container in detached mode or in other words in the background, and
- `postgres` uses the postgres image. By default it will get the image from https://hub.docker.com.


Execute `docker ps` to check on running Docker containers. We should see our basic-postgres container running. `docker ps` is like `ps -ef` on Linux/Unix, which lists all running applications.

Sample output:

![Screen shot of terminal showing docker ps output after postgres container was started](/blog/2022/07/running-postgresql-on-docker/term01.webp)

### Working with the Postgres container

Just as Postgres running natively on an operating system, Postgres on Docker comes with the psql front-end client for accessing the Postgres database. To access psql in the Postgres container execute the following command:

```plain
docker exec -it basic-postgres psql -U postgres
```

Where:

- `exec -it` executes something interactive (`-i`) with a TTY (`-t`),
- `basic-postgres` specifies the container, and
- `psql -U postgres` is the psql command with its switch to specify the Postgres user.

Now we are able to execute any psql command.

Let's try a few Postgres commands and import the famous "dvdrental" sample database to our Postgres installation.

List all available databases:

```plain
\l
```

Create a database named `dvdrental`:

```plain
create database dvdrental;
```

List all available databases. We should now see the created `dvdrental` database.

```plain
\l
```

Quit from psql:

```plain
\q
```

Download the dvdrental database backup from [postgresqltutorial.com](https://www.postgresqltutorial.com/) and after it succeeds, unzip it:

```plain
curl -O https://www.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip
unzip dvdrental.zip
```

Execute the following command to import the data. It will restore the `dvdrental.tar` backup to our Postgres database.

```plain
docker exec -i basic-postgres pg_restore -U postgres -v -d dvdrental < dvdrental.tar
```

Where:

- `exec -i` executes something interactive,
- `basic-postgres` specifies which container,
- `pg_restore -U postgres -v -d dvdrental` is the pg_restore command with its own arguments:
  - `-U postgres` says to connect as the postgres user,
  - `-v` enables verbose mode,
  - `-d dvdrental` specifies the database to connect to, and
- `< dvdrental.tar` says which file's data the outside shell should pass into the container to pg_restore.

Log in to the dvdrental database:

```plain
docker exec -it basic-postgres psql -U postgres -d dvdrental
```

Where:

- `exec -it` executes something interactive with a terminal,
- `basic-postgres` specifies which container, and
- `psql -U postgres -d dvdrental` is the psql command with the postgres user and the dvdrental database specified.

List all tables by describing the tables in the dvdrental database:

```plain
\dt
```

List the first 10 actors from the actor table:

```plain
select * from actor limit 10;
```

Quit from psql:

```plain
\q
```

Gracefully stop the Docker container:

```plain
docker stop basic-postgres
```

If you don’t need it anymore you can delete the container:

```plain
docker rm basic-postgres
```

Sample output:

![Screen shot of terminal showing import of dvdrental sample database into Postgres](/blog/2022/07/running-postgresql-on-docker/psql01.webp)

And later:

![Screen shot of terminal showing psql investigation of dvdrental sample database](/blog/2022/07/running-postgresql-on-docker/psql02.webp)


### Run Postgres image as a “real world” Postgres container

The basic Postgres container is only good for learning or testing. It requires more features to be able to serve as a working database for a real world application. We will add 2 more features to make it useable:

- **Persistent storage:** By default the container filesystem is ephemeral. What this means is whenever we restart a terminated or deleted container, it will get an all-new, fresh filesystem and all previous data will be wiped clean. This is not suitable for database systems. To be a working database, we need to add a persistent filesystem to the container.
- **Port forwarding from host to container:** The container network is isolated, making it inaccessible from the outside world. A database is no use if it can’t be accessed. To make it accessible we need to forward a host operating system port to the container port.

Let’s start building a “real world” Postgres container. Firstly we need to create the persistent storage. In Docker this is known as a volume.

Execute the following command to create a volume named `pg-data`:

```plain
docker volume create pg-data
```

List all Docker volumes and ensure that `pg-data` was created:

```plain
docker volume ls | grep pg-data
```

Run a Postgres container with persistent storage and port forwarding:

```plain
docker run --name real-postgres \
-e POSTGRES_PASSWORD=mysecretpassword \
-v pg-data:/var/lib/postgresql/data \
-p 5432:5432 \
-d \
postgres
```

Where:

- `--name real-postgres` sets the container name,
- `-e POSTGRES_PASSWORD=mysecretpassword` sets the password of the default user `postgres`
- `-v pg-data:/var/lib/postgresql/data` mounts the pg-data volume as the postgres data directory,
- `-p 5432:5432` forwards from port 5432 of host operating system to port 5432 of container,
- `-d` runs the container in detached mode or, in other words, in the background, and
- `postgres` use the postgres image. By default it will get the image from https://hub.docker.com

Execute `docker ps` to check on running containers on Docker. Take note that the real-postgres container has port forwarding information.

Now we are going to try to access the Postgres container with psql from the host operating system.

```plain
psql -h localhost -p 5432 -U postgres
```

Sample output:

![Screen shot of terminal showing access to Postgres in Docker with persistent storage](/blog/2022/07/running-postgresql-on-docker/term02.webp)

### Cleaning up the running container

Stop the container:

```plain
docker stop real-postgres
```

Delete the container:

```plain
docker rm real-postgres
```


Delete the volume:

```plain
docker volume rm pg-data
```

### Managing Postgres container with Docker Compose

Managing a container with a long list of arguments to Docker is tedious and error prone. Instead of the Docker CLI command we could use Docker Compose, which is a tool for managing containers from a YAML manifest file.

Create the following file named `docker-compose.yaml`:

```yaml
version: '3.1'
services:
  db:
    container_name: real-postgres-2
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

To start the Postgres container with Docker Compose, execute the following command in the same location as `docker-compose.yaml`:

```plain
docker-compose up -d
```

Where `-d` runs the container in detached mode.

Execute `docker ps` to check on running Docker containers. Take note that `real-postgres-2` was created by Docker Compose.

To stop Postgres container with Docker Compose, execute the following command in the same location as `docker-compose.yaml`:

```plain
docker-compose down
```

Sample output:

![Screen shot of terminal showing Postgres container deployed by Docker Compose](/blog/2022/07/running-postgresql-on-docker/term03.webp)

### Conclusion

That’s all, folks. We have successfully deployed PostgreSQL on Docker.

Now we are able to reap the benefits of container technology for PostgreSQL, including portability, agility, and better management.
