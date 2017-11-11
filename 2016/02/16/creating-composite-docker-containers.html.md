---
author: Kirk Harr
gh_issue_number: 1202
tags: containers, sysadmin
title: Creating Composite Docker Containers with Docker Compose
---

### Composite Docker Containers

[Docker](https://docker.com) is an application container system which allows logical isolation and automation of software components into isolated instances similar in some ways to a virtual server. This model is quite powerful for creating new instances of a given application rapidly, and creating automated system stacks from high-availability to high-performance clusters. Even though there is no technical limitation, the idea behind this model is that these containers should be in a 1:1 relationship with each application component. If you deploy a Docker image for Apache Tomcat, the container will contain Tomcat, and only Tomcat and its core dependencies. If you needed a Tomcat application server, and a PostgreSQL database to go with that application server; in general you would need to create two separate containers, one with the Tomcat image and the other with the PostgreSQL image. This can lead to an undesirable situation with complexity where you must manage both containers separately, even though they are both part of the same stack. In order to solve this problem, recently the Docker team developed Docker Compose to allow these complex applications to all live inside one distinct container configuration.

### Creating a composite stack with separated containers

Using the standard Dockerfile configurations and continuing the example above, you could create a Tomcat application server with a corresponding PostgreSQL database server using two separate containers. Here is an example of the Tomcat Dockerfile:

```nohighlight
FROM java:8-jre

ENV CATALINA_HOME /usr/local/tomcat
ENV PATH $CATALINA_HOME/bin:$PATH
RUN mkdir -p "$CATALINA_HOME"
WORKDIR $CATALINA_HOME

# see https://www.apache.org/dist/tomcat/tomcat-8/KEYS
RUN gpg --keyserver pool.sks-keyservers.net --recv-keys \
 05AB33110949707C93A279E3D3EFE6B686867BA6 \
 07E48665A34DCAFAE522E5E6266191C37C037D42 \
 47309207D818FFD8DCD3F83F1931D684307A10A5 \
 541FBE7D8F78B25E055DDEE13C370389288584E7 \
 61B832AC2F1C5A90F0F9B00A1C506407564C17A3 \
 79F7026C690BAA50B92CD8B66A3AD3F4F22C4FED \
 9BA44C2621385CB966EBA586F72C284D731FABEE \
 A27677289986DB50844682F8ACB77FC2E86E29AC \
 A9C5DF4D22E99998D9875A5110C01C5A2F6059E7 \
 DCFD35E0BF8CA7344752DE8B6FB21E8933C60243 \
 F3A04C595DB5B6A5F1ECA43E3B7BBB100D811BBE \
 F7DA48BB64BCB84ECBA7EE6935CD23C10D498E23

ENV TOMCAT_MAJOR 8
ENV TOMCAT_VERSION 8.0.30
ENV TOMCAT_TGZ_URL https://www.apache.org/dist/tomcat/tomcat-$TOMCAT_MAJOR/v$TOMCAT_VERSION/bin/apache-tomcat-$TOMCAT_VERSION.tar.gz

RUN set -x \
 && curl -fSL "$TOMCAT_TGZ_URL" -o tomcat.tar.gz \
 && curl -fSL "$TOMCAT_TGZ_URL.asc" -o tomcat.tar.gz.asc \
 && gpg --verify tomcat.tar.gz.asc \
 && tar -xvf tomcat.tar.gz --strip-components=1 \
 && rm bin/*.bat \
 && rm tomcat.tar.gz*

EXPOSE 8080
CMD ["catalina.sh", "run"]
```

Here is an example of the PostgreSQL Dockerfile:

```nohighlight
# vim:set ft=dockerfile:
FROM debian:jessie

# explicitly set user/group IDs
RUN groupadd -r postgres --gid=999 && useradd -r -g postgres --uid=999 postgres

# grab gosu for easy step-down from root
RUN gpg --keyserver pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates wget && rm -rf /var/lib/apt/lists/* \
 && wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/1.2/gosu-$(dpkg --print-architecture)" \
 && wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/1.2/gosu-$(dpkg --print-architecture).asc" \
 && gpg --verify /usr/local/bin/gosu.asc \
 && rm /usr/local/bin/gosu.asc \
 && chmod +x /usr/local/bin/gosu \
 && apt-get purge -y --auto-remove ca-certificates wget

# make the "en_US.UTF-8" locale so postgres will be utf-8 enabled by default
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
 && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

RUN mkdir /docker-entrypoint-initdb.d

RUN apt-key adv --keyserver ha.pool.sks-keyservers.net --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8

ENV PG_MAJOR 9.5
ENV PG_VERSION 9.5.0-1.pgdg80+2

RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main' $PG_MAJOR > /etc/apt/sources.list.d/pgdg.list

RUN apt-get update \
 && apt-get install -y postgresql-common \
 && sed -ri 's/#(create_main_cluster) .*$/\1 = false/' /etc/postgresql-common/createcluster.conf \
 && apt-get install -y \
  postgresql-$PG_MAJOR=$PG_VERSION \
  postgresql-contrib-$PG_MAJOR=$PG_VERSION \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/postgresql && chown -R postgres /var/run/postgresql

ENV PATH /usr/lib/postgresql/$PG_MAJOR/bin:$PATH
ENV PGDATA /var/lib/postgresql/data
VOLUME /var/lib/postgresql/data

COPY docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 5432
CMD ["postgres"]
```

### Creating a composite container with Docker Compose

Using [Docker Compose](https://docs.docker.com/compose/) you can define multiple container images within a single configuration file so to keep them together as a single logical unit. In order to do so you give each container a name, and then provide within the definition for each container the same Docker parameters you would use in a regular Dockerfile. Here is an example of the situation discussed earlier where you have a Tomcat image and a PostgreSQL image container which go together:

```nohighlight
db:
  image: postgres
web:
  build: .
  command: /usr/local/tomcat/bin/catalina.sh run
  volumes:
    - .:/code
  ports:
    - "8080:8080"
  links:
    - db
  log_driver: "syslog"
  log_opt:
    syslog-facility: "daemon"
```

Within these configuration values, there are a number of things being defined. Firstly the database container is created and defined with the default postgres image. Then the web application container defines that the docker image will be built using the application code and Dockerfile present in the CWD. After both containers are built, Docker will perform some actions to get things ready like starting Catalina and copying the code from the CWD into /code on the new container volume. In addition there are some values to configure application logging and to allow for the database container to be linked to the web container. After the file is created, all that is required to start the containers is to call 'docker-compose up' from the CWD where the docker-compose.yml file and the application code are located.

After starting the containers you should see output in 'docker ps' showing the new containers. Here is the output from my test with Tomcat/PostgreSQL from when I was doing some testing on the Struts 2 web framework for Java:

```nohighlight
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
3e3656879a7b        strutsdocker_web    "/usr/local/tomcat/bi"   3 weeks ago         Up 3 weeks          0.0.0.0:8080->8080/tcp   strutsdocker_web_1
cb756e473ed8        postgres            "/docker-entrypoint.s"   8 weeks ago         Up 3 weeks          5432/tcp                 strutsdocker_db_1
```

Both containers keep the naming convention of the directory name of the CWD where the application source code and Docker configuration files are located, along with the composite container name (db and web in this case) and an incrementing number for each instance you create. This can be really helpful in case you need to update any of the application source code and rebuild, as the DB container will be retained and all of its volume data will still be intact. It's worth noting though that in the opposite situation, where the database needs to be rebuilt, you could do this without impacting the web container data but they would both be shutdown and startup together as they are seen by Docker as two containers with a dependency which make up one logical application.

### Conclusions

The concept of using individual images for applications, and distributing those images by using the public software ecosystem makes the initial deployment phase very easy as much of the initial work is already done. However the 1:1 relationship of one application per container does not really reflect the current state of web development. For complex applications that need a data layer in a database, a presentation layer in an application server as well as components like search indexing, having individual containers for each one would be unmanageable. Using a composite container allows you to keep the same benefits of the Docker image ecosystem, while adding in the ease of managing all the pieces of the application holistically as one container.
