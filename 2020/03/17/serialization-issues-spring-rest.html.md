---
title: "Serialization and Deserialization Issues in Spring REST"
author: Kürşat Kutlu Aydemir
tags: json, java, frameworks, spring
gh_issue_number: 1607
---

![Mosaic pattern](/blog/2020/03/17/serialization-issues-spring-rest/image-0.jpg)

[Photo](https://unsplash.com/photos/hCzHhu1v0fA) by [Annie Spratt](https://unsplash.com/@anniespratt)

[Spring Boot](https://spring.io/projects/spring-boot) projects primarily use the JSON library [Jackson](https://github.com/FasterXML/jackson) to serialize and deserialize objects. It is especially useful that Jackson automatically serializes objects returned from REST APIs and deserializes complex type parameters like `@RequestBody`.

In a Spring Boot project the automatically registered `MappingJackson2HttpMessageConverter` is usually enough and makes JSON conversions simple, but this may have some issues which need custom configuration. Let’s go over a few good practices for them.

### Configuring a Custom Jackson ObjectMapper

In Spring REST projects a custom implementation of `MappingJackson2HttpMessageConverter` helps to create the custom `ObjectMapper`, as seen below. Whatever custom implementation you need to add to the custom `ObjectMapper` can be handled by this custom converter:

```java
public class CustomHttpMessageConverter extends MappingJackson2HttpMessageConverter {

    private ObjectMapper initCustomObjectMapper() {
        ObjectMapper customObjectMapper = new ObjectMapper();
        return customObjectMapper;
    }

    // ...
}
```

Additionally, some `MappingJackson2HttpMessageConverter` methods, such as `writeInternal`, can be useful to override in certain cases. I’ll give a few examples in this article.

In Spring Boot you also need to register a custom `MappingJackson2HttpMessageConverter` like below:

```java
@Bean
MappingJackson2HttpMessageConverter mappingJackson2HttpMessageConverter() {
    return new CustomHttpMessageConverter();
}
```

### Serialization

#### Pretty-printing

Pretty-printing in Jackson is disabled by default. By enabling `SerializationFeature.INDENT_OUTPUT` in the `ObjectMapper` configuration pretty-print output is enabled (as in the example below). Normally a custom `ObjectMapper` is not necessary for setting the pretty-print configuration. In some cases, however, like one case of mine in a recent customer project, this configuration might be necessary.

For example, passing a URL parameter can enable pretty-printing. In this case having a custom `ObjectMapper` with pretty-print enabled and keeping the default `ObjectMapper` of `MappingJackson2HttpMessageConverter` as is could be a better option.

```java
public class CustomHttpMessageConverter extends MappingJackson2HttpMessageConverter {

    private ObjectMapper initiatePrettyObjectMapper() {
        ObjectMapper customObjectMapper = new ObjectMapper();
        customObjectMapper.configure(SerializationFeature.INDENT_OUTPUT, true);

        // additional indentation for arrays
        DefaultPrettyPrinter pp = new DefaultPrettyPrinter();
        pp.indentArraysWith(new DefaultIndenter());
        customObjectMapper.setDefaultPrettyPrinter(pp);

        return customObjectMapper;
    }

}
```

#### Conditionally Filtering the Fields

When serializing a response object you may need to include or ignore one or more fields depending on their values. Let’s assume a model class `UserResponse` like below.

Notice that we used `@JsonIgnore` which is completely discarding the annotated field from serialization. Conditional filtering is different and it can be done using `SimpleBeanPropertyFilter` objects set to the filter provider of the `ObjectMapper` objects. Also notice that `@JsonFilter` annotation is used for `UserResponse` which points to which filter will be used by `ObjectMapper` during the serialization.

```java
@JsonFilter("userCodeFilter")
public class UserResponse {

    public Integer userId;
    public String username;
    public Integer code;

    @JsonIgnore
    public String status;

}
```

Here we add a filter called `userCodeFilter`—like the one we added to the custom `ObjectMapper` of `CustomHttpMessageConverter`—which will include the `UserResponse` class’s code field in the serialization if its value is greater than 0. You can add multiple filters to `ObjectMapper` for different models.

```java
public class CustomHttpMessageConverter extends MappingJackson2HttpMessageConverter {

    private ObjectMapper initiatePrettyObjectMapper() {
        ObjectMapper customObjectMapper = new ObjectMapper();
        customObjectMapper.configure(SerializationFeature.INDENT_OUTPUT, true);

        // additional indentation for arrays
        DefaultPrettyPrinter pp = new DefaultPrettyPrinter();
        pp.indentArraysWith(new DefaultIndenter());
        customObjectMapper.setDefaultPrettyPrinter(pp);

        PropertyFilter userCodeFilter = new SimpleBeanPropertyFilter() {
            @Override
            public void serializeAsField(Object pojo, JsonGenerator jgen, SerializerProvider provider, PropertyWriter writer)
                    throws Exception {
                if (include(writer)) {
                    if (!writer.getName().equals("code")) {
                        writer.serializeAsField(pojo, jgen, provider);
                        return;
                    }
                    int intValue = ((UserResponse) pojo).code;
                    if (intValue > 0) {
                        writer.serializeAsField(pojo, jgen, provider);
                    }
                } else if (!jgen.canOmitFields()) {
                    writer.serializeAsOmittedField(pojo, jgen, provider);
                }
            }

            @Override
            protected boolean include(BeanPropertyWriter writer) {
                return true;
            }

            @Override
            protected boolean include(PropertyWriter writer) {
                return true;
            }
        };

        FilterProvider filters = new SimpleFilterProvider().addFilter("userCodeFilter", userCodeFilter);
        customObjectMapper.setFilterProvider(filters);

        return customObjectMapper;
    }

}
```

### Deserialization

#### JSON String Parse Error Handling in Spring Boot

This one is a little tricky. Deserialization of a JSON `@RequestParam` object can cause parsing errors if the JSON object is not well-formed. The errors thrown in Jackson’s deserialization level just before it’s pushed to Spring Boot occur at that level, so Spring Boot doesn’t catch these errors.

Deserialization of Jackson maps JSON to POJOs and finally returns the expected Java class object. If the JSON is not well-formed, parsing cannot be done and `MappingJackson2HttpMessageConverter` internally throws a parsing error. Since this exception is not caught by Spring Boot and no object is returned, the REST controller would be unresponsive, having a badly-formed JSON payload.

Here we can override the internal `read` method of `MappingJackson2HttpMessageConverter`, hack the `ReadJavaType` with a `customReadJavaType` method, and make it return an internal error when the deserialization fails to parse the JSON input, rather than throwing an exception which is not seen or handled by Spring Boot.

```java
@Override
public Object read(Type type, @Nullable Class<?> contextClass, HttpInputMessage inputMessage)
        throws IOException, HttpMessageNotReadableException {

    objectMapper.enable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);

    JavaType javaType = getJavaType(type, contextClass);
    return customReadJavaType(javaType, inputMessage);
}

private Object customReadJavaType(JavaType javaType, HttpInputMessage inputMessage) throws IOException {
    try {
        if (inputMessage instanceof MappingJacksonInputMessage) {
            Class<?> deserializationView = ((MappingJacksonInputMessage) inputMessage).getDeserializationView();
            if (deserializationView != null) {
                return this.objectMapper.readerWithView(deserializationView).forType(javaType).
                        readValue(inputMessage.getBody());
            }
        }
        return this.objectMapper.readValue(inputMessage.getBody(), javaType);
    }
    catch (InvalidDefinitionException ex) {
        //throw new HttpMessageConversionException("Type definition error: " + ex.getType(), ex);
        return "Type definition error";
    }
    catch (JsonProcessingException ex) {
        //throw new HttpMessageNotReadableException("JSON parse error: " + ex.getOriginalMessage(), ex, inputMessage);
        return "JSON parse error";
    }
}
```

This way you can return errors occurring at the deserialization level to Spring Boot, which expects a deserialized object but gets a `String` value which can be caught and translated into a `ControllerAdvice` handled exception. This also makes it easier to catch JSON parsing errors without using any third party JSON libraries like Gson.
