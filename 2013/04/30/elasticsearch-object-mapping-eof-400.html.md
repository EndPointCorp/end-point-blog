---
author: Miguel Alatorre
gh_issue_number: 792
tags: elasticsearch, json, search
title: 'Elasticsearch: Give me object!'
---



I'm currently working on a project where Elasticsearch is used to index copious amounts of data with sometimes deeply nested JSON. A recurring error I've experienced is caused by a field not conforming to the type listed in the mapping. Let's reproduce it on a small scale.

Assuming you have Elasticsearch installed, let's create an index and mapping:

```bash
$ curl -XPUT 'http://localhost:9200/test' -d '
{
    "mappings": {
        "item": {
            "properties": {
                "state": {
                    "properties": {
                        "name": {"type": "string"}
                    }
                }
            }
        }
    }
}
'
{"ok":true,"acknowledged":true}
```

Since we've defined properties for the "state" field, Elasticsearch will automatically treat it as an object.* Let's now add some documents:

```bash
$ curl -XPUT 'http://localhost:9200/test/item/1' -d '
{
    "state": {
        "name": "North Carolina"
    }
}
'
{"ok":true,"_index":"test","_type":"item","_id":"1","_version":1}
```

Success! Let's now get into trouble:

```bash
$ curl -XPUT 'http://localhost:9200/test/item/2' -d '
{
    "state": "California"
}
'
{"error":"MapperParsingException[object mapping for [state] tried to parse as object, but got EOF, has a concrete value been provided to it?]","status":400}
```

The solution: check any non-objects in your data against your mapping schema and you'll be sure to find a mismatch.

One thing to note is that the explicit creation of the mapping is unnecessary since Elasticsearch creates it using the first added document. Try this:

```bash
$ curl -XPUT 'http://localhost:9200/test2/item/1' -d '
{
    "state": {
        "name": "North Carolina"
    }
}
'
{"ok":true,"_index":"test2","_type":"item","_id":"1","_version":1}
$ curl -XGET 'http://localhost:9200/test2/_mapping'
{
    "test2": {
        "item": {
            "properties": {
                "state": {
                    "dynamic":"true",
                    "properties": {
                        "name": {"type":"string"}
                    }
                }
            }
        }
    }
}
```

So, this stays true to the statement: ["Elasticsearch is schema-less, just toss it a typed JSON document and it will automatically index it."](http://elasticsearch.com/products/elasticsearch/) You can throw your car keys at Elasticsearch and it will index, however, as noted above, just be sure to keep throwing nothing but car keys.

*Anything with one or more nested key-value pairs is considered an object in Elasticsearch. For more on the object type, see [here](http://www.elasticsearch.org/guide/reference/mapping/object-type/).


