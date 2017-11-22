---
author: Jon Jensen
title: "Logstash: Removing fields with empty values"
tags: hosting, logging
gh_issue_number: 1341
---

The [Elastic stack](https://www.elastic.co/products) is a nice toolkit for collecting, transporting, transforming, aggregating, searching, and reporting on log data from many sources. It was formerly known as the ELK stack, after its main components Elasticsearch, Logstash, and Kibana, but with the addition of Beats and other tools, the company now calls it simply the Elastic stack.

We are using it in a common configuration, on a central log server that receives logs via rsyslog over TLS, which are then stored in local files and processed further by Logstash.

### When conservation is recommended

When forwarding logs on to SaaS log services such as Logentries, SumoLogic, etc., we have a limited amount of data transfer and storage allotted to us. So we need to either economize on what we send them, pay for a more expensive plan, or retain a shorter period of history.

For some very busy logs (nginx logs in JSON format) we decided to delete fields with empty values from the log event during the filter phase in Logstash. This removes a lot of data from the log message we send to the log service over the wire, and reduces the size of each log event stored in their system.

I expected this to be simple, but that expectation sometimes proves to be false. :)

### Trying the prune filter

The most obvious way would be to use the Logstash `prune` filter, which is designed for just such a use case. However, the `prune` filter doesn’t handle nested keys. This is [only noted in the Logstash prune filter source code](https://github.com/logstash-plugins/logstash-filter-prune/blob/b01ed5e4bcada138654195a3f410801f5670720a/lib/logstash/filters/prune.rb#L38-L40) in a comment!

```ruby
# NOTE: This filter currently only support operations on top-level fields,
# i.e. whitelisting and blacklisting of subfields based on name or value
# does not work.
```

Too bad.

### Pruning with custom Ruby code

Several people have posted alternative solutions to this in the past. A representative recipe to have [Logstash delete empty fields](https://manwhoami.wordpress.com/2014/11/25/logstash-delete-empty-fields/) looked like this:

```ruby
# This doesn’t work in Logstash 5 and newer ...
filter {
  ruby {
    code => "event.to_hash.delete_if {|field, value| value == '' }"
  }
}
```

And sadly, it doesn’t work.

### Logstash 5 event API changes

It used to work with older versions of Logstash, but no longer. Logstash was originally written in Ruby, specifically JRuby for running on the JVM. But for Logstash 5 it was rewritten in Java, and though JRuby extensions are still possible, the [Ruby event API has changed](https://www.elastic.co/guide/en/logstash/5.0/breaking-changes.html#_ruby_filter_and_custom_plugin_developers) so that the log data is no longer provided as a mutable hash that the above code expects. (See also [the Logstash event API documentation](https://www.elastic.co/guide/en/logstash/current/event-api.html).)

### Custom Ruby code to prune in Logstash 5+

So I came up with Ruby code that works using the new Logstash event API. It is more complicated , but it is still pretty straightforward:

```ruby
filter {
  # remove fields with empty values
  ruby {
    code => "
      def walk_hash(parent, path, hash)
        path << parent if parent
        hash.each do |key, value|
          walk_hash(key, path, value) if value.is_a?(Hash)
          @paths << (path + [key]).map {|p| '[' + p + ']' }.join('')
        end
        path.pop
      end

      @paths = []
      walk_hash(nil, [], event.to_hash)

      @paths.each do |path|
        value = event.get(path)
        event.remove(path) if value.nil? || (value.respond_to?(:empty?) && value.empty?)
      end
    "
  }
}
```

We first recursively walk through the whole data structure that the API converts to a Ruby hash for us. We get all nested field names and store in an array their Logstash-style paths like `"[nginx][access][upstream_addr]"` that the API expects. Then we walk through the paths and use the API to check for empty values, and remove them. This way we also avoid changing the hash while still walking through it.

With that configuration and code in a file in `/etc/logstash/conf.d/` (this is on CentOS 7 using the logstash RPM from Elastic) all the fields with empty values are removed.

### Some other log event trimming

In addition we added a few other filters to remove or limit the size of fields that we are happy to have on our own central log server for archival or forensic purposes, but that we don’t need to send to our paid log service for the kinds of reporting we are doing there:

```
mutate {
  remove_field => [
    "@version", "beat", "host", "input_type", "offset", "source", "type",
    "[geoip][location]",
    "[nginx][access][pipe]",
    "[nginx][access][remote_port]",
    "[nginx][access][ssl_session_id]",
    "[nginx][access][ssl_session_reused]",
    "[nginx][access][upstream_bytes_received]",
    "[nginx][access][upstream_connect_time]",
    "[nginx][access][upstream_response_length]",
    "[nginx][access][upstream_status]"
  ]
}

if "beats_input_codec_plain_applied" in [tags] {
  mutate {
    remove_tag => ["beats_input_codec_plain_applied"]
  }
}

truncate {
  length_bytes => 1024
}
```

For example, sometimes the client sends an absurdly long HTTP `Referer` request header, or the URI requested is very long — we see plenty longer than 5000 characters. We are happy to truncate those to save space.

We also do not need to waste space in our paid log service with the repetitive tag `beats_input_codec_plain_applied` or the same Filebeat version in every single log event.

### Finis

This is working for us on Logstash 5.6.3, but should work on Logstash 5.0 and newer.
