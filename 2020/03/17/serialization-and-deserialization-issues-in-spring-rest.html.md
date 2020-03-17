---
title: "Serialization and Deserialization Issues in Spring-REST"
author: Kursat Aydemir
tags: Spring-Boot, REST, Jackson, JSON, Serialization, Deserialization
---
![Serialization Deserialization](/2020/03/17/serialization-and-deserialization-issues-in-spring-rest/serializedeserialize.png)



Spring-Boot projects primarily use Jackson JSON library to serialize and deserialize the objects. Especially it is very useful that Jackson automatically serializes the returning output objects of REST APIs and deserializes the complex type parameters like `@RequestBody`.

In a Spring-Boot project automatically registered `MappingJackson2HttpMessageConverter` usually is enough and makes everything simple for a Spring-Boot project for JSON conversions, but still it may have some issues which needs custom configurations. Here let's see a few good practices of them.



## Configuring a Custom Jackson ObjectMapper

In a Spring REST project a custom implementation of `MappingJackson2HttpMessageConverter` as below simply helps creating the custom `ObjectMapper`. Whatever custom implementation you need to add to the custom `ObjectMapper` can be handled within this custom `MappingJackson2HttpMessageConverter`.



```java
public class CustomHttpMessageConverter extends MappingJackson2HttpMessageConverter {

    private ObjectMapper initCustomObjectMapper() {
        ObjectMapper customObjectMapper = new ObjectMapper();

        return customObjectMapper;
    }

    // ...
}
```


Additionally some overridable `MappingJackson2HttpMessageConverter` methods like `writeInternal`,  can be useful to override in certain cases as a few samples will be given in this article.

In Spring-Boot you also need to register this custom MappingJackson2HttpMessageConverter like below. This makes sure the MappingJackson2HttpMessageConverter of the Spring-boot project is registered as your CustomHttpMessageConverter object.



```java
@Bean
MappingJackson2HttpMessageConverter mappingJackson2HttpMessageConverter() {
    return new CustomHttpMessageConverter();
}
```




## Serialization



### Pretty Printing

By default Jackson pretty printing is disabled. By enabling the `SerializationFeature.INDENT_OUTPUT` of the `ObjectMapper` configuration the pretty printing output is enabled as below example. Normally a custom `ObjectMapper` is not essentially needed for setting the pretty print configuration. In some cases, like I needed in a recent customer project, this configuration can be required optionally.

For example passing a URL parameter can enable pretty printing. In this case having a custom `ObjectMapper` having pretty print configuration enabled and keep the default `ObjectMapper` of `MappingJackson2HttpMessageConverter` as it is could be better option.



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



### Conditionally Filtering the Fields

When serializing a response object sometimes you may need to include or ignore one or more fields in serialization depending on their values. Let's assume a model class `UserResponse` like below.

Here notice that we used `@JsonIgnore` which is completely discarding the annotated field from serialization. The conditional filtering is different and it can be done using `SimpleBeanPropertyFilter` objects set to the filter provider of the `ObjectMapper` objects. Also notice that `@JsonFilter` annotation is used for `UserResponse` which points which filter will be used by `ObjectMapper` during the serialization.



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


Here we add a filter called `userCodeFilter` as we used in the `@JsonFilter` annotation above `UserResponse` to the custom `ObjectMapper` of `CustomHttpMessageConverter` to include the code field of the `UserResponse` class in the serialization if its value is only greater than 0. There can be added multiple filters to ObjectMapper for different models.

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





## Deserialization



### JSON String Parse Error Handling In Spring-Boot

Ok this one is a little tricky. During the deserialization of a JSON `@RequestParam` object can cause parsing errors if the JSON object is not well formed. The errors thrown in the Jackson's deserialization level just before pushed to Spring-Boot so that Spring-Boot doesn't catch this kind of exceptions occurred at that level.

Deserialization of Jackson maps JSON to POJOs and finally returns the expected Java class object. If a JSON is not well formed parsing cannot be done and `MappingJackson2HttpMessageConverter` internally throws parsing errors. Since this exception is not caught at Spring-Boot and no object is returned the REST controller would unresponsive for the controller request having non-well formed JSON payload.

Here we can override the internal `read` method of `MappingJackson2HttpMessageConverter`, and hack the `ReadJavaType` with a `customReadJavaType` method and make it return the internal error when the deserialization couldn't actually parse the JSON input rather than throwing the exception which is not handled by Spring-Boot.



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


This way you can return errors occurred at the deserialization level to Spring-Boot which actually expects a deserialized object but gets a `String` value which can be caught and translated into a `ControllerAdvice` handled exception. This also makes it more comfortable to catch JSON parsing errors without using any third party JSON libraries like Gson.