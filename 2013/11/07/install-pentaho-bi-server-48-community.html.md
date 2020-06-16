---
author: Selvakumar Arumugam
gh_issue_number: 878
tags: analytics, pentaho, postgres
title: Install Pentaho BI Server 4.8 Community Edition with PostgreSQL Repository
---

Pentaho BI server community edition can be installed through an archive file available from SourceForge.

Prerequisites

- Java 6
- PostgreSQL

Download Pentaho BI Server installation file (biserver-ce-4.8.0-stable.zip) from SourceForge: http://sourceforge.net/projects/pentaho/files/Business%20Intelligence%20Server/4.8.0-stable

Unzip the archive file and navigate inside biserver-ce to set sh files to executable mode:

```bash
$ unzip biserver-ce-4.8.0-stable.zip
$ cd biserver-ce
$ find . -type f -iname '*.sh' -exec chmod a+x {} \;
```

Pentaho community edition uses hsql database as default. Need to create two databases in Postgres for Pentaho. Find the SQL files to create databases under biserver-ce/data/postgresql. database_name, user_name and password are configurable through SQL files. Fix two errors before creating database using SQL files. Comment two lines in below files tables as commented.

- create_quartz_postgresql.sql

```sql
ALTER TABLE qrtz_fired_triggers
    ALTER TRIGGER_NAME  TYPE VARCHAR(200),
    ALTER TRIGGER_GROUP TYPE VARCHAR(200),
    ALTER INSTANCE_NAME TYPE VARCHAR(200),
    ALTER JOB_NAME      TYPE VARCHAR(200),
    ALTER JOB_GROUP     TYPE VARCHAR(200),
    ADD COLUMN PRIORITY INTEGER NULL;
--    ADD COLUMN PRIORITY INTEGER NOT NULL;
```
- migrate_quartz_postgresql.sql

```sql
ALTER TABLE qrtz_fired_triggers
    ALTER TRIGGER_NAME  TYPE VARCHAR(200),
    ALTER TRIGGER_GROUP TYPE VARCHAR(200),
    ALTER INSTANCE_NAME TYPE VARCHAR(200),
    ALTER JOB_NAME      TYPE VARCHAR(200),
    ALTER JOB_GROUP     TYPE VARCHAR(200);
--    ADD COLUMN PRIORITY INTEGER NOT NULL;
--    ALTER COLUMN PRIORITY SET NULL;
```

Modify database name, username & password if necessary and create databases for configuration and scheduling by running below commands.

```bash
$ psql -U postgres -a -f create_quartz_postgresql.sql
$ psql -U postgres -a -f create_repository_postgresql.sql
$ psql -U postgres -a -f create_sample_datasource_postgresql.sql
$ psql -U postgres -a -f migrate_quartz_postgresql.sql
$ psql -U postgres -a -f migration.sql
```

Verify databases quartz (scheduling) and hibernate (configuration) and their tables.

Now database name, username, password and driver should be configured in following places in files. By default hsql drivers, settings enabled in config files so comment hsql configurations and enable Postgres settings.

- biserver-ce/tomcat/webapps/pentaho/META-INF/context.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Context path="/pentaho" docbase="webapps/pentaho/">
        <Resource name="jdbc/Hibernate" auth="Container" type="javax.sql.DataSource"
                factory="org.apache.commons.dbcp.BasicDataSourceFactory" maxActive="20" maxIdle="5"
                maxWait="10000" username="hibuser" password="password"
                driverClassName="org.postgresql.Driver" url="jdbc:postgresql://localhost:5432/hibernate"
                validationQuery="select 1" />
               
        <Resource name="jdbc/Quartz" auth="Container" type="javax.sql.DataSource"
                factory="org.apache.commons.dbcp.BasicDataSourceFactory" maxActive="20" maxIdle="5"
                maxWait="10000" username="pentaho_user" password="password"
                driverClassName="org.postgresql.Driver" url="jdbc:postgresql://localhost:5432/quartz"
                validationQuery="select 1"/>
</Context>
```
- biserver-ce/pentaho-solutions/system/applicationContext-spring-security-jdbc.xml

```xml
        <bean id="dataSource"
                class="org.springframework.jdbc.datasource.DriverManagerDataSource">
                <property name="driverClassName" value="org.postgresql.Driver" />
                <property name="url" value="jdbc:postgresql://localhost:5432/hibernate" />
                <property name="username" value="hibuser" />
                <property name="password" value="password" />
        </bean>
```

- biserver-ce/pentaho-solutions/system/applicationContext-spring-security-hibernate.properties

```nohighlight
jdbc.driver=org.postgresql.Driver
jdbc.url=jdbc:postgresql://localhost:5432/hibernate
jdbc.username=hibuser
jdbc.password=password

hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
```
- biserver-ce/pentaho-solutions/system/hibernate/hibernate-settings.xml

```xml
<config-file>system/hibernate/postgresql.hibernate.cfg.xml</config-file>
```
- biserver-ce/pentaho-solutions/system/hibernate/postgresql.hibernate.cfg.xml

```xml
<property name="connection.driver_class">org.postgresql.Driver</property>
    <property name="connection.url">jdbc:postgresql://localhost:5432/hibernate</property>
    <property name="dialect">org.hibernate.dialect.PostgreSQLDialect</property>
    <property name="connection.username">hibuser</property>
    <property name="connection.password">password</property>
```
- biserver-ce/pentaho-solutions/system/simple-jndi/jdbc.properties

```nohighlight
Hibernate/type=javax.sql.DataSource
Hibernate/driver=org.postgresql.Driver
Hibernate/url=jdbc:postgresql://localhost:5432/hibernate
Hibernate/user=hibuser
Hibernate/password=password
Quartz/type=javax.sql.DataSource
Quartz/driver=org.postgresql.Driver
Quartz/url=jdbc:postgresql://localhost:5432/quartz
Quartz/user=pentaho_user
Quartz/password=password
```
Specify the pentaho solutions path, server url and port in web.xml of tomcat webapp

- biserver-ce/tomcat/webapps/pentaho/WEB-INF/web.xml

```xml
        <context-param>
                <param-name>solution-path</param-name>
                <param-value>/opt/avr-new/biserver-ce/pentaho-solutions</param-value>
        </context-param>

        <context-param>
                <param-name>fully-qualified-server-url</param-name>
                <param-value>http://localhost:8080/pentaho/</param-value>
        </context-param>
```

Pentaho can be run tomcat custom ports by modifying the ports in server.xml and web.xml

- biserver-ce/tomcat/conf/server.xml

```xml
    <Connector URIEncoding="UTF-8" port="9090" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="8443" />
```

- biserver-ce/tomcat/webapps/pentaho/WEB-INF/web.xml 

```xml
         <context-param>
                <param-name>fully-qualified-server-url</param-name>
                <param-value>http://localhost:8080/pentaho/</param-value>
        </context-param>
```
Let’s start the Pentaho BI server and try out its great features. Commands to start and stop the BI server:

```bash
biserver-ce$ ./start-pentaho.sh
biserver-ce$ ./stop-pentaho.sh
```

Troubleshooting:

```bash
biserver-ce$ tail -f tomcat/logs/catalina.out
biserver-ce$ tail -f tomcat/logs/pentaho.out
```
