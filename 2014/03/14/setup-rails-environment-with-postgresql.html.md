---
author: Selvakumar Arumugam
gh_issue_number: 947
tags: mac, postgres, rails, tls
title: Setup Rails Environment with PostgreSQL on Apple Mac OS X
---

Setting up Rails on Mac OS X to have a Rails application is a tedious process. It’s a kind of road block for newbies. Here I have listed the steps to have Rails application running with a PostgreSQL database on the Mac OS X.

### 1. Rails

Before installing Rails, We need couple of things installed on Mac OS X. 

##### Ruby

Luckily Mac OS X comes with preinstalled Ruby. 

```bash
$ ruby -v
ruby 2.0.0p247 (2013-06-27 revision 41674) [universal.x86_64-darwin13]
```
##### Xcode and Command Line Tools

Install [Xcode](https://itunes.apple.com/app/xcode/id497799835?l=en&mt=12) from Mac Store. Xcode contains some system libraries which are required for Rails. 

To install Command Line Tools, Open Xcode -> Xcode(menu bar) -> Preferences -> Downloads -> Install ‘Command Line Tools’

##### Homebrew

Homebrew helps to install gems with ‘gem’ and its dependencies with help of brew. Homebrew makes our life easier by handling dependencies for us during installation.

```bash
$ ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
```
Note:-- Xcode already comes bundled with gcc. But install gcc using homebrew if you face any gcc problems while installing Rails.

```bash
$ brew tap homebrew/dupes
$ brew install apple-gcc42
$ sudo ln -s /usr/local/bin/gcc-4.2 /usr/bin/gcc-4.2
```
##### RVM

RVM (Ruby Version Manager) is a must have tool to easily manage multiple Ruby environments. Let’s install RVM:

```bash
$ curl -L https://get.rvm.io | bash -s stable --ruby
$ rvm -v
rvm 1.25.19 (stable) by Wayne E. Seguin <wayneeseguin@gmail.com>, Michal Papis <mpapis@gmail.com> [https://rvm.io/]
$ echo '[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm"' >> ~/.bashrc
$ source ~/.bashrc
```
Gemsets are very helpful to manage multiple applications with different sets of gems packed. So let’s create a gemset to work on:

```bash
$ rvm use ruby-2.1.1@endpoint --create
$ rvm gemset list
gemsets for ruby-2.1.1 (found in /Users/selva/.rvm/gems/ruby-2.1.1)
   (default)
=> endpoint
   global
```
(See also the similar [rbenv](http://rbenv.org/), which some people prefer.)

##### Rails

We are all set to install Rails now: 

```bash
$ gem install rails
$ rails -v
Rails 4.0.3
```

### 2. Install PostgreSQL

Download and Install PostgreSQL database from [Postgres.app](http://postgresapp.com/) which provides PostgresSQL in a single package to easily get started with Max OS X. After the installation, open Postgres located under Applications to start PostgreSQL database running. Find out the PostgreSQL bin path and append to ~/.bashrc for accessing commands through the shell.

```bash
$ echo 'PATH="/Applications/Postgres.app/Contents/Versions/9.3/bin:$PATH"' >> ~/.bashrc
$ source ~/.bashrc
```
Next create a user in PostgreSQL for Rails application.

```bash
$ createuser -P -d -e sampleuser
Enter password for new role:
Enter it again:
CREATE ROLE sampleuser PASSWORD 'md5afd8d364af0c8efa11183c3454f56c52' NOSUPERUSER CREATEDB NOCREATEROLE INHERIT LOGIN;
```

### 3. Create Application

Rails environment is ready with PostgreSQL database. Let’s create a sample web application

```bash
$ rails new SampleApp
```
Configure database details under SampleApp/config/database.yml

```nohighlight
development:
  adapter: postgresql
  encoding: unicode
  database: sampledb
  username: sampleuser
  password: samplepassword
```
Start the Rails server and hit [http://0.0.0.0:3000](http://0.0.0.0:3000/) on your browser to verify Rails app is running on your computer.

```bash
$ cd SampleApp
$ ./bin/rails server
```

### 4. Version Control System

It is always good to develop an application with version control system. Here I am using ‘Git’.

```bash
$ cd SampleApp
$ git init
$ git add . && git commit -m "Initial Commit"
```

### 5. Server on https (optional)

Sometimes the application needs to be run on the https protocol for security reasons to if third-party services require the application to be served over https. So we should setup https (SSL Security). First, create an self-signed SSL certificate. To create a self-signed certificate we should have RSA key and Certificate request in place beforehand.

```bash
$ mkdir ~/.ssl && cd ~/.ssl

# creating 2048 bit rsa key
$ openssl genrsa -out server.key 2048 
Generating RSA private key, 2048 bit long modulus
..........++++++
.........++++++
e is 65537 (0x10001)

# creating certificate request
$ openssl req -new -key server.key -out server.csr 
........
# Common Name value should be FQDN without protocol
 Common Name (eg, your name or your server's hostname) []:mydomain.com 
........

# creating self-signed certificate
$ openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt 
```
WEBrick server can be configured to use SSL key and certificate by adding below lines of code into bin/rails after ‘#!/usr/bin/env ruby’. Provide the locations of RSA key and certificate in the Ruby code. 

```ruby
require 'rubygems'
require 'rails/commands/server'
require 'rack'
require 'webrick'
require 'webrick/https'

module Rails
    class Server < ::Rack::Server
        def default_options
            super.merge({
                :Port => 3000,
                :environment => (ENV['RAILS_ENV'] || "development").dup,
                :daemonize => false,
                :debugger => false,
                :pid => File.expand_path("tmp/pids/server.pid"),
                :config => File.expand_path("config.ru"),
                :SSLEnable => true,
                :SSLVerifyClient => OpenSSL::SSL::VERIFY_NONE,
                :SSLPrivateKey => OpenSSL::PKey::RSA.new(
                       File.open("/path/to/server.key").read),
                :SSLCertificate => OpenSSL::X509::Certificate.new(
                       File.open("/path/to/server.crt").read),
                :SSLCertName => [["CN", WEBrick::Utils::getservername]]
            })
        end
    end
end 
```
Next start the Rails server. 

```bash
$ ./bin/rails server
```
It will use the SSL certificate and run the application over https protocol as we configured above. We can verify at [https://0.0.0.0:3000](https://0.0.0.0:3000/).

We are ready with a Rails development environment on our Mac to do magic.
