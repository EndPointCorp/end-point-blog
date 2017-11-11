---
author: Selvakumar Arumugam
gh_issue_number: 1268
tags: database, java
title: Connect Multiple JPA repositories using Static and Dynamic Methods
---

The JPA Repository is a useful Spring Framework library that provides object-relational mapping for Java web applications to be able to connect to a wide variety of databases. Most applications need to establish a connection with one database to store and retrieve the data though sometimes there could be more than one database to read and write. There could also be some cases where the application needs to choose which database should be used dynamically, based on each request's parameters. Let's see how to configure and establish connections for these three cases.

### 1. Single Static Connection

In order to use JPA the following configurations are required to get the database connection handle and define the interface to map a database table by extending JpaRepository class.

UserRepository.java - this part of the code configures how to map the user table

```java
package com.domain.data;

import com.domain.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository <User, Integer> {
}
```
persistent-context.xml - the dataSourceReadWrite bean class defines the database connection while the entityManagerFactoryReadWrite bean helps to access the database from the base package com.domain

```xml
...
<jpa:repositories base-package="com.domain" entity-manager-factory-ref="entityManagerFactoryReadWrite" transaction-manager-ref="transactionManager">
</jpa:repositories>

<bean abstract="true" class="org.apache.commons.dbcp.BasicDataSource" destroy-method="close" id="abstractDataSource" p:driverclassname="${jdbc.driverClassName}" p:maxactive="20" p:maxidle="20" p:minidle="20" p:testonborrow="true" p:validationquery="SELECT 1" />

<bean id="dataSourceReadWrite" p:password="${jdbc.password}" p:url="${jdbc.url}" p:username="${jdbc.username}" parent="abstractDataSource" />

<bean abstract="true" class="org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean" id="abstractEntityManagerFactory" p:jpadialect-ref="hibernateJpaDialect" p:jpavendoradapter-ref="jpaAdapter">
  <property name="jpaProperties">
    <props>
      <prop key="hibernate.use_sql_comments">true</prop>
      <prop key="hibernate.temp.use_jdbc_metadata_defaults">false</prop>
    </props>
  </property>
</bean>

<bean id="entityManagerFactoryReadWrite" p:datasource-ref="dataSourceReadWrite" p:persistenceunitname="readWritePU" parent="abstractEntityManagerFactory">
  <property name="packagesToScan">
    <list>
      <value>com.domain</value>
    </list>
  </property>
</bean>

<bean class="org.springframework.orm.jpa.JpaTransactionManager" id="transactionManager" p:datasource-ref="dataSourceReadWrite" p:entitymanagerfactory-ref="entityManagerFactoryReadWrite" />
...
```
UserController.java - the userRepository object access defines how to use a static database configuration to fetch the User object record

```java
@Api(name = "User", description = "User API Service")
@Controller
public class UserController {

  @Autowired
  private UserRepository userRepository;

  @ApiMethod(
    description = "Return the user object using the userId in the URL",
    produces = {MediaType.APPLICATION_JSON_VALUE},
    roles = {"read", "write"}
  )
  @RequestMapping(value = "/users/{userId}", method = RequestMethod.GET, produces = "application/json")
  @ResponseBody
  public UserModel getUser(@PathVariable @ApiParam(name = "userId", description = "User ID") Integer userId) throws ServiceException {
    User user = (userRepository.findOne(userId));
    if (user != null) {
    return new UserModel(user);
  }
  else {
    throw new ResourceNotFoundServiceException("UserId " + userId + " was not found");
  }
}
}
```

### 2. Multiple Static Connections

In some cases, we may need to connect more than one database in our application. Usually there will be a primary database and a secondary one which syncs data from the primary, most likely as a readonly replica load balancing approach. In this case the application needs to be configure to establish connection with two different datasources.

To achieve this result it's possible to define ReadWrite and ReadOnly datasources in the spring configuration and then declare the specific Repository classes for each specific datasource.

UserRepository.java - ReadWrite repository definition under the package com.domain.data

```java
package com.domain.data;

import com.domain.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Integer> {
}
```
UserReadonlyRepository.java - ReadOnly repository definition under the package com.domain.data.readonly

```java
package com.domain.data.readonly;

import com.domain.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserReadonlyRepository extends JpaRepository<User, Integer> {
}
```
persistent-context.xml - this file defines two different datasources (dataSourceReadWrite and dataSourceReadOnly) while jpa repositories specify the repositories package path

```xml
...
<jpa:repositories base-package="com.domain" entity-manager-factory-ref="entityManagerFactoryReadWrite" transaction-manager-ref="transactionManager">
  <repository:exclude-filter expression="com.domain.data.readonly" type="regex"></repository:exclude-filter>
</jpa:repositories>

<jpa:repositories base-package="com.domain.data.readonly" entity-manager-factory-ref="entityManagerFactoryReadOnly" transaction-manager-ref="transactionManagerReadOnly">

<bean abstract="true" class="org.apache.commons.dbcp.BasicDataSource" destroy-method="close" id="abstractDataSource" p:driverclassname="${jdbc.driverClassName}" p:maxactive="20" p:maxidle="20" p:minidle="20" p:testonborrow="true" p:validationquery="SELECT 1" />
<bean id="dataSourceReadWrite" p:password="${jdbc.password}" p:url="${jdbc.url}" p:username="${jdbc.username}" parent="abstractDataSource" />
<bean id="dataSourceReadOnly" p:password="${jdbc.readonly.password}" p:url="${jdbc.readonly.url}" p:username="${jdbc.readonly.username}" parent="abstractDataSource" />
<bean abstract="true" class="org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean" id="abstractEntityManagerFactory" p:jpadialect-ref="hibernateJpaDialect" p:jpavendoradapter-ref="jpaAdapter">
  <property name="jpaProperties">
    <props>
      <prop key="hibernate.use_sql_comments">true</prop>
      <prop key="hibernate.temp.use_jdbc_metadata_defaults">false</prop>
    </props>
  </property>
</bean>

<bean id="entityManagerFactoryReadWrite" p:datasource-ref="dataSourceReadWrite" p:persistenceunitname="readWritePU" parent="abstractEntityManagerFactory">
  <property name="packagesToScan">
    <list>
      <value>com.domain</value>
    </list>
  </property>
</bean>

<bean id="entityManagerFactoryReadOnly" p:datasource-ref="dataSourceReadOnly" p:persistenceunitname="readOnlyPU" parent="abstractEntityManagerFactory">
  <property name="packagesToScan">
    <list>
      <value>com.domain</value>
    </list>
  </property>
</bean>

<bean class="org.springframework.orm.jpa.JpaTransactionManager" id="transactionManager" p:datasource-ref="dataSourceReadWrite" p:entitymanagerfactory-ref="entityManagerFactoryReadWrite" />

<bean class="org.springframework.orm.jpa.JpaTransactionManager" id="transactionManagerReadOnly" p:datasource-ref="dataSourceReadOnly" p:entitymanagerfactory-ref="entityManagerFactoryReadOnly" />
...
```
UserController.java - in this definition it's interesting to note the the readonly flag, which will establish a connection with ReadWrite or ReadOnly database, based on that flag value

```java
@Api(name = "User", description = "User API Service")
@Controller
public class UserController {

  @Autowired
  private UserRepository userRepository;
  @Autowired
  private UserReadOnlyRepository userReadOnlyRepository;

  @ApiMethod(
  description = "Return the user object using the userId in the URL",
  produces = {MediaType.APPLICATION_JSON_VALUE},
  roles = {"read", "write"}
  )
  @RequestMapping(value = "/users/{userId}", method = RequestMethod.GET, produces = "application/json")
  @ResponseBody
  public UserModel getUser(@PathVariable @ApiParam(name = "userId", description = "User ID") Integer userId, @ApiParam(name = "readOnly", description = "Param to set data source to read from") Boolean readOnly) throws ServiceException {
    User user = (readOnly ?
    userReadOnlyRepository.findOne(userId) : userRepository.findOne(userId));

    if (user != null) {
      return new UserModel(user);
    }
    else {
      throw new ResourceNotFoundServiceException("UserId " + userId + " was not found");
    }
  }
}
```

### 3. Multiple Dynamic Connections

Recently there was an application that needed to choose the database during API request processing. Unfortunately defining multiple datasources and choosing the database based on the hard coded checks in the code is really cumbersome. Instead it's possible to use JPA Repository which provides a feature to override the database lookup dynamically using AbstractRoutingDataSource when a request is sent to the application.

UserRepository.java - defines mapping to the user table

```java
package com.domain.data;

import com.domain.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Integer> {
}
```
persistence-context.xml - dataSourceRootDB and dataSourceLiveDB beans defines two different databases. MultitenantRoutingDataSource holds the datasources available to chose dynamically from the code

```xml
...
<jpa:repositories base-package="com.domain" entity-manager-factory-ref="genericEntityManagerFactory" transaction-manager-ref="transactionManager">
</jpa:repositories>

<bean abstract="true" class="org.apache.commons.dbcp.BasicDataSource" destroy-method="close" id="abstractDataSource" p:driverclassname="${jdbc.driverClassName}" p:maxactive="20" p:maxidle="20" p:minidle="20" p:testonborrow="true" p:validationquery="SELECT 1" />

<bean id="dataSourceRootDB" p:password="${jdbc.password}" p:url="${jdbc.url}" p:username="${jdbc.username}" parent="abstractDataSource" />

<bean id="dataSourceLiveDB" p:password="${jdbc.livedb.password}" p:url="${jdbc.livedb.url}" p:username="${jdbc.livedb.username}" parent="abstractDataSource" />

<bean class="com.domain.route.MultitenantRoutingDataSource" id="dataSource">
  <property name="targetDataSources">
    <map key-type="java.lang.String">
      <entry key="rootdb" value-ref="dataSourceRootDB"></entry>
      <entry key="livedb" value-ref="dataSourceLiveDB"></entry>
    </map>
  </property>
  <property name="defaultTargetDataSource" ref="dataSourceRootDB">
  </property>
</bean>

<bean class="org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean" id="genericEntityManagerFactory" p:datasource-ref="dataSource" p:jpadialect-ref="hibernateJpaDialect" p:jpavendoradapter-ref="jpaAdapter" p:persistenceunitname="readWriteDynamicPU">
  <property name="jpaProperties">
    <props>
      <prop key="hibernate.use_sql_comments">true</prop>
      <prop key="hibernate.temp.use_jdbc_metadata_defaults">false</prop>
    </props>
  </property>
  <property name="packagesToScan">
    <list>
      <value>com.data.domain</value>
    </list>
  </property>
</bean>

<bean class="org.springframework.orm.jpa.JpaTransactionManager" id="transactionManager" p:datasource-ref="dataSource" p:entitymanagerfactory-ref="genericEntityManagerFactory" />
...
```
UserController.java - this class choose the datasource dynamically based on the request and calls the selected service to complete the action

```java
...
@Api(name = "User", description = "User API Service")
@Controller public class UserController {
    @Autowired     private UserService userService;

    @ApiMethod(
            description = "Return the user object using the userId in the URL",
            produces = {MediaType.APPLICATION_JSON_VALUE},
            roles = {"oms-read", "oms-write"}
    )
    @RequestMapping(value = "/users/{userId}", method = RequestMethod.GET, produces = "application/json")
    @ResponseBody
    public UserModel getUser(@PathVariable @ApiParam(name = "userId", description = "User ID") Integer userId, @RequestHeader(value="X-Database", defaultValue= DatabaseEndpointUtils.ROOT_DB, required=false) String databaseEndpoint) throws ServiceException {
        MultiTenantContext.setCurrentTenant(databaseEndpoint);
        return userService.getUser(userId, true);
    }
}
...
```
MultiTenantContext.java - this code sets the datasource connection based on the request from Controller

```java
package com.domain.common;

import com.domain.util.DatabaseEndpointUtils;
import com.domain.supplychain.app.ws.exceptions.InvalidDatabaseEndpointException;
import com.domain.exceptions.ServiceException;

public class MultiTenantContext {
    private static ThreadLocal<Object> currentTenant = new ThreadLocal<>();

    public static Logger logger = LoggerFactory.getLogger(MultiTenantContext.class.getName());
    public static void setCurrentTenant(Object tenant) throws ServiceException {
        logger.info("MultiTenantContext setCurrentTenant: [{}]", tenant);
        if(DatabaseEndpointUtils.isValidEndpoint(tenant.toString())) {
            currentTenant.set(tenant);
        } else {
            throw new InvalidDatabaseEndpointException("Invalid database endpoint");
        }
    }

    public static Object getCurrentTenant() {
        logger.info("MultiTenantContext getCurrentTenant: [{}]", currentTenant.get());
        return currentTenant.get();
    }

}
```
MultitenantRoutingDataSource.java - here there's the definition which determines how the datasource establish the connection. Specifically it will get the datasource which was set previously based on the request parameters

```java
package com.domain.route;
import com.domain.common.MultiTenantContext;
import org.springframework.jdbc.datasource.lookup.AbstractRoutingDataSource;

public class MultitenantRoutingDataSource extends AbstractRoutingDataSource {

    private Logger logger = LoggerFactory.getLogger(MultitenantRoutingDataSource.class.getName());
    @Override
    protected Object determineCurrentLookupKey() {
        logger.info("MultitenantRoutingDataSource determineCurrentLookupKey: [{}]", MultiTenantContext.getCurrentTenant());
        return MultiTenantContext.getCurrentTenant();
    }

}
```
DefaultUserService.java - Fetch the user data from the dynamically chosen database.

```java
@Service
public class DefaultUserService implements UserService {

    @Autowired
    private UserRepository userRepository;

    @Override
    @Transactional
    public UserModel getUser(Integer userId, boolean readOnly) throws ServiceException {
        User user = (userRepository.findOne(userId));
        if (user != null) {
            return new UserModel(user);
        }
        else {
            throw new ResourceNotFoundServiceException("UserId " + userId + " was not found");
        }
    }
}
```

### Conclusion

The application establishes a connection with database through any one of these methods, based on the requirement. The single or multiple static connections are commonly used in most of the applications. But when there is a requirement to choose the database dynamically to establish a connection, AbstractRoutingDataSource class in spring framework features a wonderful way to implement the functionality as explained above.


