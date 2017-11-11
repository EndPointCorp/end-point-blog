---
author: Marco Matarazzo
gh_issue_number: 1230
tags: nginx
title: A caching, resizing, reverse proxying image server with Nginx
---



While working on a complex project, we had to set up a caching reverse proxying image server with the ability of automatically resize any cached image on the fly.

Looking around on the Internet, we discovered [an amazing blog post](http://charlesleifer.com/blog/nginx-a-caching-thumbnailing-reverse-proxying-image-server-/) describing how Nginx could do that with a neat [Image Filter module](http://nginx.org/en/docs/http/ngx_http_image_filter_module.html) capable of resizing, cropping and rotating images, creating an Nginx-only solution.

### What we wanted

What we wanted to achieve in our test configuration was to have a URL like:

**http://www.example.com/image/<width>x<height>/<URL>**

...that would retrieve the image at:

**https://upload.wikimedia.org/<URL>**

...then resize it on the fly, cache it and serve it.

Our setup ended up being almost the same as the one in that blog post, with some slight differences.

### Requirements installation

First, as the post points out, the Image Filter module is **not** installed by default on many Linux distributions. As we're using Nginx's official repositories, it was just a matter of installing the *nginx_module_image_filter* package and restarting the service.

### Cache Storage configuration

Continuing following the post's great instructions, we set up the cache in our main http section, tuning each parameter to fit ur specific needs. We wanted a 10MB storage space for keys and 100MB for actual images, that will be removed after not being accessed for 40 days. The main configuration entry was then:

```bash
proxy_cache_path /tmp/nginx_cache levels=1:2 keys_zone=nginx_cache:10M max_size=100M inactive=40d;
```

This went straight in the http section of nginx.conf.

### Caching Proxy configuration

Next, we configured our front facing virtual host. In our case, we needed the reverse proxy to live within an already existing site, and that's why we chose the /image/ path prefix.

```bash
server {
      ...
  
      location /image/ {
          proxy_pass http://127.0.0.1:20000;
          proxy_cache nginx_cache;
          proxy_cache_key "$proxy_host$uri$is_args$args";
      }
  
      location / {
          # other locations we may need for the site.
          root /var/www/whatever;
      }
  
  }
```

  

Every URL starting with /image/ would be server from the cache if present, otherwise it would be proxied to our Resizing Server, and cached for 30 days, as desired.

### Resizing Server configuration

We then configured the resizing server, using a regexp to extract the width, height and URL of the image we desire.

The server will proxy the request to https://upload.wikimedia.org/ looking for the image, resize it and then serve it back to the Caching Proxy. We preferred to keep it simple and tidy, as we didn't actually need any aws-related configuration as the blog post did.

```bash
server {
      ...
  
      location ~ ^/image/([0-9]+)x([0-9]+)/(.+) {
          image_filter_buffer 20M; # Will return 415 if image is bigger than this
          image_filter_jpeg_quality 75; # Desired JPG quality
          image_filter_interlace on; # For progressive JPG
  
          image_filter resize $1 $2;
  
          proxy_pass https://upload.wikimedia.org/$3;
      }
  
  }
```

Note that we may also use [image_filter](http://nginx.org/en/docs/http/ngx_http_image_filter_module.html#image_filter) resize and crop options, should we need different results than just resizing.

### Testing the final result

You should now be able to fire up your browser and access an URL like:

```nohighlight
http://www.example.com/image/150x150/wikipedia/commons/0/01/Tiger.25.jpg
```

...and enjoy your caching, resizing, reverse proxying image server.

### Optionally securing access to your image server

As this was not a public server, we didn't use any security mechanism to validate the request.

The original blog post, though, reports a very simple and clever way to prevent abuse from unauthorized access, using the [Secure Link module](http://nginx.org/en/docs/http/ngx_http_secure_link_module.html).

To access your server you will now need to add an auth parameter to the request, with a secure token that can be [easily calculated as an MD5 hash](http://nginx.org/en/docs/http/ngx_http_secure_link_module.html#secure_link_md5).

This is the simple Bash command we used to test it:

```bash
echo -n '/image/150x150/wikipedia/commons/0/01/Tiger.25.jpg your_secret' | openssl md5 -binary | openssl base64 | tr +/ -_ | tr -d =
```

...and the resulting URL would be:

**http://www.example.com/image/150x150/wikipedia/commons/0/01/Tiger.25.jpg?auth=TwcXg954Rhkjt1RK8IO4jA**

### Conclusions

Thanks to Charles Leifer for explaining his findings so well and giving us a smooth path with only minor tweaks to make our project work.


