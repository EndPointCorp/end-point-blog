---
author: "Matt Vollrath"
title: "From Zero to HTTPS in an afternoon"
tags: hosting, security, tls, nginx
gh_issue_number: 1339
---

I’ve been hosting my own [humble personal web site](https://mvollrath.net) since 2012. I had never bothered setting up HTTPS for my domain, but after hearing about the [Let’s Encrypt](https://letsencrypt.org/) project, I was completely out of excuses.

For the unfamiliar, Let’s Encrypt offers free and fully automatic HTTPS certificates. The web cares about HTTPS now more than ever. Deeply interactive interfaces like geolocation and user media (camera, microphone) are too sensitive to trust an insecure transport. By leveraging the security features present in modern browsers, users can expect a reasonable safety from attacks that would exploit the weaknesses of HTTP.

To take the security mission even further, I decided to completely containerize my server and expose only a couple of ports. Using a Docker composition made it very easy to deploy up-to-date nginx and keep it isolated from the rest of my host shard.

The first mission was to set up certificates with `certbot`, the EFF’s free certificate tool. `certbot` has a plugin that writes nginx configuration for you, but in this case I didn’t want nginx installed on my host at all. Instead of following the nginx-specific instructions for my platform, I opted for the [webroot plugin](https://certbot.eff.org/docs/using.html#webroot) to just give me a certificate and let me figure out how to set it up. A `certbot` invocation and a few seconds later I have certificates for my site in `/etc/letsencrypt/live/www.mvollrath.net`.

Next I went shopping for nginx Docker images. The [official nginx image](https://store.docker.com/images/nginx) has everything I want: the latest and greatest mainline nginx based on stable Debian. I considered the Alpine variant, but felt like Debian was a better choice for me; familiarity outweighs a few tens of MB of image size.

The nginx image ships with a default configuration serving a single root directory over HTTP. Since HTTPS was the point of this experiment, I set out to correct this. I started by creating a project directory on the host to house all the configuration needed to build out my server. Then I started up a container with the vanilla configuration and copied config files `/etc/nginx/nginx.conf` and `/etc/nginx/conf.d/default.conf` out of the container to the project directory. With those config files now in my possession, I created a simple Dockerfile to inject them into a new image based on the library nginx image.

```docker
FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf
```

With that out of the way, I started hacking config to create my ideal HTTPS server. First I set up a redirect to force all traffic to the HTTPS site.

```nginx
server {
    listen 80;
    server_name mvollrath.net www.mvollrath.net;
    return 301 https://$server_name$request_uri;
}
```

Now I would need a good way to get my certificates into the container. Docker compose has a handy `secrets` directive to make this really painless.

```yaml
version: '3.1'  # must be at least 3.1 for secrets feature
secrets:
  ssl_privkey:
    file: "/etc/letsencrypt/live/www.mvollrath.net/privkey.pem"
  ssl_fullchain:
    file: "/etc/letsencrypt/live/www.mvollrath.net/fullchain.pem"
services:
  nginx:
    container_name: "nginx"
    build: "."
    ports:
    - "80:80"
    - "443:443"
    volumes:
    - "/home/matt/htdocs:/usr/share/nginx/html:ro"
    restart: "on-failure"
    secrets:
    - "ssl_privkey"
    - "ssl_fullchain"
```

This mounts the provided secrets in `/run/secrets` to be scooped up by the site config.

```nginx
server {
    listen 443 ssl http2 default_server;

    server_name mvollrath.net www.mvollrath.net;
    ssl_certificate /run/secrets/ssl_fullchain;
    ssl_certificate_key /run/secrets/ssl_privkey;

    [...]
}
```

Now I can update my server by running `docker-compose build --pull` and then `docker-compose up -d`. This may cause a momentary outage while the containers are being swapped, but for a personal site this is nothing to sweat over. I dropped these commands in a cron script since I like updates but would rather not have to think about updates.

With my new HTTPS site now exposed to the world, I found some free HTTPS validation tools to check my work and optimize the configuration a few notches beyond the “pretty good” nginx defaults. If you’ve deployed an HTTPS site for work or pleasure, check out the [collection of web security tools](/blog/2017/09/19/web-security-services-roundup) rounded up by Phin in September.

I was really happy with the Let’s Encrypt tools and user experience. If you’re still hosting HTTP with no HTTPS option, consider using the free tools to get your free certificate and help your users protect their privacy. If you’re interested in using HTTPS wherever available, consider using the [HTTPS Everywhere](https://www.eff.org/https-everywhere) extension offered by the EFF.
