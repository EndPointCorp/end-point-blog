---
author: Selvakumar Arumugam
gh_issue_number: 879
tags: analytics, pentaho, postgres
title: Install Pentaho BI Server 5 Enterprise Edition with PostgreSQL repository
---

Pentaho provides different ways to install Pentaho BI server. Each method has its own flexibility in installation.

1. Installer mode—​Easy to install BA & DI server & tools in one flow with default PostgreSQL repo & default Tomcat server. (New Postgres installed on port 5432.)

2. Archive mode—​BA server installed with own BA repository & default Tomcat server. Necessary tools need to be installed manually.

3. Manual mode—​BA server installed with own BA repository & own application server (Tomcat or JBoss). Necessary tools need to installed manually.

We have a Postgres instance running on our server and are good with Tomcat as application server so Archive mode of installation is suitable for us. Pentaho installation requires two things be installed before starting with Pentaho installation.

- Java 7
- PostgreSQL

Archive mode installation files can be accessible only to license purchased users. Download biserver-ee-5.x-dist.zip from Pentaho customer portal with account credentials here: [https://support.pentaho.com/forums/20413716-Downloads](https://support.pentaho.com/forums/20413716-Downloads)

Unzip the archive file and you can see the installation files inside extracted directory.

```bash
$ unzip biserver-ee-5.x-dist.zip
$ cd biserver-ee-5.x;ls
install.bat  installer.jar  install.sh  license.txt  README.txt
```

In remote servers Pentaho can be installed on console mode with -console’. Accept the license and provide the installation path to install Pentaho BI server.

```bash
$ java -jar installer.jar -console
```

Find biserver-ee directory under the installation path and set sh files to executable mode.

```bash
$ cd biserver-ee;
$ find . -type f -iname '*.sh' -exec chmod a+x {} \;
```

Let’s create repository databases by running queries in SQL files located at biserver-ee/data/postgresql.

quartz, hibernate and jackrabbit databases will be created by executing these SQL files. Database names, usernames and password can be changed by modifying in SQL files if required.

```bash
$ cd biserver-ee/data/postgresql
$ psql -U postgres -p 5432 -a -f create_jcr_postgresql.sql
$ psql -U postgres -p 5432 -a -f create_quartz_postgresql.sql
$ psql -U postgres -p 5432 -a -f create_repository_postgresql.sql
$ psql -U postgres -p 5432 -a -f pentaho_mart_postgresql.sql
```

Pentaho uses postgresql as default database and files are configured to use postgresql. So just verify the database_name, username and password to work with installed postgresql and databases created.

- biserver-ee/pentaho-solutions/system/quartz/quartz.properties

```nohighlight
org.quartz.jobStore.driverDelegateClass = org.quartz.impl.jdbcjobstore.PostgreSQLDelegate
```

- biserver-ee/pentaho-solutions/system/hibernate/hibernate-settings.xml

```xml
    <config-file>system/hibernate/postgresql.hibernate.cfg.xml</config-file>
```

- biserver-ee/pentaho-solutions/system/hibernate/postgresql.hibernate.cfg.xml

```xml
    <property name="connection.driver_class">org.postgresql.Driver</property>
    <property name="connection.url">jdbc:postgresql://localhost:5432/hibernate</property>
    <property name="dialect">org.hibernate.dialect.PostgreSQLDialect</property>
    <property name="connection.username">pentaho_user</property>
    <property name="connection.password">password</property>
```

There are more occurrences in this file. Carefully do the necessary changes in all the places.

- biserver-ee/pentaho-solutions/system/jackrabbit/repository.xml
- biserver-ee/pentaho-solutions/system/jackrabbit/repository/workspaces/default/workspace.xml
- biserver-ee/tomcat/webapps/pentaho/META-INF/context.xml

```xml
<Resource name="jdbc/PDI_Operations_Mart" auth="Container" type="javax.sql.DataSource"
            factory="org.apache.commons.dbcp.BasicDataSourceFactory" maxActive="20" maxIdle="5"
            maxWait="10000" username="pentaho_user" password="password"
            driverClassName="org.postgresql.Driver" url="jdbc:postgresql://localhost:5432/hibernate"
            validationQuery="select 1"/>
```

```xml
Download postgresql and h2 drivers then place it under biserver-ee/tomcat/lib
```

postgresql-9.x.jdbc4.jar

h2-1.2.x.jar

Change Tomcat port on these two files to run Pentaho on different port.

Specify the Pentaho solutions path, server URL and port in web.xml of Tomcat webapp.

biserver-ee/tomcat/webapps/pentaho/WEB-INF/web.xml

```xml
        <context-param>
                <param-name>solution-path</param-name>
                <param-value>$INSTALLATION_PATH/biserver-ee/pentaho-solutions</param-value>
        </context-param>

        <context-param>
                <param-name>fully-qualified-server-url</param-name>
                <param-value>http://localhost:8080/pentaho/</param-value>
        </context-param>
```

Pentaho can be configured to run on different ports by changing ports on Tomcat server.xml and web.xml

- biserver-ee/tomcat/biserver-ee/tomcat/server.xml

```xml
    <Connector URIEncoding"UTF-8" port"9090" protocol"HTTP/1.1"
               connectionTimeout"20000"
               redirectPort"8443" />
```

```xml
- biserver-ee/tomcat/webapps/pentaho/WEB-INF/web.xml
         <context-param>
                <param-name>fully-qualified-server-url</param-name>
                <param-value>http://localhost:9090/pentaho/</param-value>
        </context-param>
```

Install license

A license needs to be installed to use Pentaho. Navigate to the license-installer directory in installation path. Feed license file to install_license.sh, separating more than one license file with spaces.

```bash
$ ./install_license.sh install ../license/Pentaho\ BI\ Platform\ Enterprise\ Edition.lic
```

Install plugins

Archive mode of installation installs only BI Server. Necessary plugins can to be installed manually. Here install the plugins for reporting, analyzer and dashboard. Plugins are available at the same place where download BI server. Download these three files and place at any path on server:

* Reporting—​pir-plugin-ee-5.x-dist.zip
* Analyzer—​pdd-plugin-ee-5.0.0.1-dist.zip
* Dashboard—​paz-plugin-ee-5.0.0.1-dist.zip

All the plugins installed through same procedure.

- Unzip the plugins and navigate to extracted directory

- run installer on console, accept the license and provide $INSTALLATION_PATH/biserver-ee/pentaho-solutions/system as location to install plugins

```bash
$ java -jar installer.jar -console
```

Let’s start the BI server

```bash
biserver-ee$ ./start-pentaho.sh
```

Install the licenses for the plugins by login as admin user (default—​Admin:password) or install through the command line:

Administration -> License -> install licenses for plugin by click +

Troubleshooting:

```bash
biserver-ee$ tail -f tomcat/logs/catalina.out
biserver-ee$ tail -f tomcat/logs/pentaho.log
```

If the pentaho.xml is present at tomcat/conf/Catalina directory, delete it. It will be generated again when you start the BA Server.

Start and stop the BI server:

```bash
biserver-ee$ ./start-pentaho.sh
biserver-ee$ ./stop-pentaho.sh
```
