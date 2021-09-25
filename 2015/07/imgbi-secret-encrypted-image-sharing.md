---
author: Emanuele “Lele” Calò
title: img.bi, a secret encrypted image sharing service tool
github_issue_number: 1143
tags:
- nodejs
- python
date: 2015-07-30
---



After a fairly good experience with [dnote](https://github.com/atoponce/d-note) installed on our own servers as an encrypted notes sharing service, my team decided that it would have been nice to have a similar service for images.

We found a nice project called [img.bi](https://github.com/imgbi/img.bi) that is based on **NodeJS**, **Python**, **Redis** and a lot of client-side **JavaScript**.

The system is divided into two components: the **HTML/JS** frontend and a **Python FastCGI API**.

Unfortunately the documentation is a still in its very early stage and it’s lacking a meaningful structure and a lot of needed information.

Here’s an overview of the steps we followed to setup img.bi on our own server behind **nginx**.

First of all we chose that we wanted to have as much as possible running and confined to a regular user, which is always a good idea with such young and potentially vulnerable tools. We chose to use the *imgbi* user.

Then since we wanted to keep as clean as possible the root user environment (and system status), we also decided to use **pyenv**. To be conservative we chose the latest Python 2.7 stable release, *2.7.10*.

```plain
git clone https://github.com/yyuu/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
echo $SHELL -l
pyenv install -l  | grep 2\\.7
pyenv install 2.7.10
pyenv global 2.7.10
pyenv version
which python
python --version
```

In order to use img.bi, we also needed NodeJS and following the same approach we chose to use [nvm](https://github.com/creationix/nvm) and install the latest NodeJS stable version:

```plain
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.25.4/install.sh | bash
nvm install stable
nvm list
nvm use stable
nvm alias default stable
node --version
```

As a short note to the usage of the **bad practice** of blindly using:

```plain
curl -o- https://some_obscure_link_or_not | bash
```

We want to add that we do **not** endorse this practice as it’s dangerous and exposes your system to many security risks. On the other hand, though, it’s true that cloning the source via Git and compile/installing it blindly is not much safer, so it’s always up to how much you trust the peer review on the project you’re about to use. And at least with an https URL you should be talking to the destination you want, whereas an http URL is much more dangerous.

Furthermore going through the entire Python and NodeJS installation as a regular user, was far beyond the scope of this post and the steps proposed here *assumes* that you’re doing everything as the regular user, except where specifically stated differently.

Anyway after that we updated **pip** and then installed all the needed Python modules:

```plain
pip install --upgrade pip
pip install redis m2crypto web.py bcrypt pysha3 zbase62 pyutil flup
```

Then it’s time to clone the actual img.bi code from the **GitHub** repo, install a few missing dependencies and then use the bower and npm .json files to add the desired packages:

```plain
git clone https://github.com/imgbi/img.bi.git
cd img.bi/
npm install -g bower grunt grunt-cli grunt-multiresize
npm install -g grunt-webfont --save-dev
npm install
bower install
```

We also faced an issue which made **Grunt** fail to start correctly. Grunt was complaining about an “undefined property” called “prototype”. If you happen to have the same problem just type

```plain
cd node_modules/grunt-connect-proxy/node_modules/http-proxy
npm install eventemitter3@0.1.6
cd -
```

That’ll basically install the eventemitter3 NodeJS package module locally to the *grunt-connect-proxy* module so to overcome the compatibility issues which in turn causes the error mentioned above.

You should use your favourite editor to change the file *config.json*, which basically contains all your local needed configuration. In particular our host is not exposed on the I2P or Tor network, so we "visually" disabled those options.

```plain
# lines with "+" needs to be replace the ones starting with a "-"
-  "name": "img.bi",
+  "name": "img.bi - End Point image sharing service",

-  "maxSize": "3145728",
+  "maxSize": "32145728",

-  "clearnet": "https://img.bi",
+  "clearnet": "https://imgbi.example",

-  "i2p": "http://imgbi.i2p",
+  "i2p": "http://NOTAVAILABLE.i2p",

-  "tor": "http://imgbifwwqoixh7te.onion",
+  "tor": "http://NOTAVAILABLE.onion",
```

Save and close the file. At this point you should be able to run “grunt” to build the project but if it fails on the multiresize task, just run

```plain
grunt --force
```

to ignore the warnings.

That’s about everything you need for the *frontend* part, so it’s now time to take care of the API.

```plain
cd
git clone https://github.com/imgbi/img.bi-api.git
cd /home/imgbi/img.bi-api/
```

You now need to edit the two Python files which are the core of the API.

```plain
# edit code.py expired.py
-upload_dir = '/home/img.bi/img.bi-files'
+upload_dir = '/home/imgbi/img.bi-files'
```

Verify that you’re not having any Python import related error, due to missing modules or else, by running the Python code.py file directly.

```plain
./code.py
```

If that’s working okay, just create a symlink in the build directory in order to have the API created files available to the frontend

```plain
ln -s /home/imgbi/img.bi-files /home/imgbi/img.bi/build/download
```

And then it’s time to spawn the actual Python daemon:

```plain
spawn-fcgi -f /home/imgbi/img.bi-api/code.py -a 127.0.0.1 -p 1234
```

The expired.py file is used by a cronjob which periodically checks if there’s any image/content that should be removed because its time has expired. First of all let’s call the script directly and if there’s no error, let’s create the crontab:

```plain
python /home/imgbi/img.bi-api/expired.py

crontab -e

@reboot spawn-fcgi -f /home/imgbi/img.bi-api/code.py -a 127.0.0.1 -p 1234
30 4 * * * python /home/imgbi/img.bi-api/expired.py
```

It’s now time to install nginx and Redis (if you still haven’t done so), and then configure them. For Redis you can just follow the usual simple, basic installation and that’ll be just okay. Same is true for nginx but we’ll add our configuration/vhost file content here as an example /etc/nginx/sites-enabled/imgbi.example.conf for everyone who may need it:

```plain
upstream imgbi-fastcgi {
  server 127.0.0.1:1234;
}

server {
  listen 80;
  listen [::]:80;
  server_name imgbi.example;
  access_log /var/log/nginx/sites/imgbi.example/access.log;
  error_log /var/log/nginx/sites/imgbi.example/error.log;
  rewrite ^ https://imgbi.example/ permanent;
}

server {
  listen 443 ssl spdy;
  listen [::]:443 ssl spdy;
  server_name  imgbi.example;
  server_name  imgbi.example;
  access_log /var/log/nginx/sites/imgbi.example/access.log;
  error_log /var/log/nginx/sites/imgbi.example/error.log;

  client_max_body_size 4G;

  include include/ssl-wildcard-example.inc;

  add_header Strict-Transport-Security max-age=31536000;
  add_header X-Frame-Options SAMEORIGIN;
  add_header X-Content-Type-Options nosniff;
  add_header X-XSS-Protection "1; mode=block";

  location / {
    root /home/imgbi/img.bi/build;
  }

  location /api {
    fastcgi_param QUERY_STRING $query_string;
    fastcgi_param REQUEST_METHOD $request_method;
    fastcgi_param CONTENT_TYPE $content_type;
    fastcgi_param CONTENT_LENGTH $content_length;

    fastcgi_param SCRIPT_NAME "";
    fastcgi_param PATH_INFO $uri;
    fastcgi_param REQUEST_URI $request_uri;
    fastcgi_param DOCUMENT_URI $document_uri;
    fastcgi_param DOCUMENT_ROOT $document_root;
    fastcgi_param SERVER_PROTOCOL $server_protocol;

    fastcgi_param GATEWAY_INTERFACE CGI/1.1;
    fastcgi_param SERVER_SOFTWARE nginx/$nginx_version;

    fastcgi_param REMOTE_ADDR $remote_addr;
    fastcgi_param REMOTE_PORT $remote_port;
    fastcgi_param SERVER_ADDR $server_addr;
    fastcgi_param SERVER_PORT $server_port;
    fastcgi_param SERVER_NAME $server_name;
    fastcgi_param HTTPS on;

    fastcgi_pass imgbi-fastcgi;
    fastcgi_keep_conn on;
  }
}
```

Well, that should be enough to get you started and at least have all the components in place. Enjoy your secure image sharing now.


