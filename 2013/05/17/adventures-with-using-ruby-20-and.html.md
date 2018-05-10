---
author: Kamil Ciemniewski
gh_issue_number: 802
tags: shell, environment, ruby, rails
title: Adventures with using Ruby 2.0 and libreadline
---

I was asked to develop a prototype app for one of our clients lately. The basis for this app was an old Rails app:

- Rails 3.2.8
- RailsAdmin
- MySQL
- rbenv + ruby-build

I wanted to upgrade the stack to work with latest toys all cool kids are so thrilled about. I also didn’t have Rails console facility at my disposal since the Ruby version installed on the development machine hadn’t been compiled against libreadline.

Not having root or sudo access on the machine I embarked on a sligthly hacky journey to make myself a better working environment.

### Ruby 2.0

After reading Mike Farmer’s [blog post](/blog/2013/04/04/today-first-speaker-at-mwrc-is-one-and) about Ruby 2.0 and tons of other material about it on the Internet, I wanted to get a feeling of how faster & greater the new Ruby is. It’s always great also to stay up-to-date with latest technologies. It’s great for me as a developer, and more importantly—​it’s great for our clients.

### Importance of libreadline in development with Ruby

To be productive developing any Rails-based application, we have to have Rails-console available at any moment. It serves a multitude of purposes. It’s also a great scratch-pad when developing methods.

While you don’t need your Ruby to support libreadline for basic uses of **irb**, you need it when using with Rails.

### Installing Ruby 2.0.0 with rbenv (ruby-build)

If you’ve installed ruby-build some time ago, chances are that you need to update it in order to be able to install latest build of Ruby 2.0.0

To do it:

```bash
cd ~/.rbenv/plugins/ruby-build
git pull
```

And you should be able now to have available latest Ruby build to install:

```bash
rbenv install 2.0.0-p195
```

If you want to install Ruby compiled with support for libreadline, you have to have it installed in your system **before** compiling the build with *rbenv install*.

If you have access to root or sudo on your system, the easiest way is to e. g:

on Debian-related Linuxes:

```bash
apt-get install libreadline-dev
```

or on Fedora:

```bash
yum install readline-devel
```

### Installing libreadline from sources

In my case—​I had to download sources and compile them myself. Luckily the system had all needed essential packages installed for building it.

```bash
wget "ftp://ftp.cwru.edu/pub/bash/readline-6.2.tar.gz"
tar xvf readline-6.2.tar.gz
cd readline-6.2
./configure --prefix=/home/kamil/libs
make
make install
```

I had to specify *–prefix* option pointing at the path where I wanted the libreadline library to be installed after compilation.

Then, I was able to actually build Ruby with readline support “on”:

```bash
CONFIGURE_OPTS="--with-readline-dir=/home/kamil/libs" rbenv install 2.0.0-p195
```

**Notice:** I was making myself a development environment and compiling from sources was my last resort. It is **not** a good practice for production environments.

Last thing I needed to do was to get rb-readline working with the project I was working on.

It turnes out that latest rb-readline doesn’t play well with latest Ruby. Also, when using Ruby 2.0.0 one have to explicitely specify it in the Gemfile, or else it won’t be loaded for the console.

Gemfile:

```ruby
gem 'rb-readline', '~> 0.4.2'
```

### This still isn’t perfect

While this setup works, it won’t let you use arrow keys. The irb process crashes quickly after even first try to navigate through the text.

For some reason, after upgrading Ruby, the RailsAdmin stylesheets stopped working. I noticed that they are being served with comments which should be replaced by other stylesheets like:

```css
/* ...
*= require_self
*= require_tree .
*/
```

I had to update Rails version in the Gemfile to have my admin back:

Gemfile:

```ruby
gem 'rails', '3.2.13'
```

Console:

```bash
bundle
```

Last thing I wanted to do, was to try if I could upgrade Rails even further and have a working Rails4 setup. This was impossible unfortunately since RailsAdmin isn’t yet compatible with it [as stated here](https://github.com/sferik/rails_admin/issues/1443).

I conclude that latest Ruby is quite usable right now. If you don’t mind the quirks with the readline—​you’re pretty safe to upgrade. This assumes though that your app doesn’t use any incompatible elements.

The main Ruby site describes them like so:

There are five notable incompatibilities we know of:

- The default encoding for ruby scripts is now UTF-8 [[#6679](https://bugs.ruby-lang.org/issues/6679)]. Some people report that it affects existing programs, such as some benchmark programs becoming very slow [ruby-dev:46547].
- Iconv was removed, which had already been deprecated when M17N was introduced in ruby 1.9. Use String#encode, etc. instead.
- There is ABI breakage [ruby-core:48984]. We think that normal users can/should just reinstall extension libraries. You should be aware: DO NOT COPY .so OR .bundle FILES FROM 1.9.
- #lines, #chars, #codepoints, #bytes now returns an Array instead of an Enumerator [[#6670](https://bugs.ruby-lang.org/issues/6670)]. This change allows you to avoid the common idiom “lines.to_a”. Use #each_line, etc. to get an Enumerator.
- Object#inspect does always return a string like `#<ClassName:0x…>` instead of delegating to #to_s. [[#2152](https://bugs.ruby-lang.org/issues/2152)]
- There are some comparatively small incompatibilities. [ruby-core:49119]
