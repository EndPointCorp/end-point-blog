---
title: "Running Ruby in Podman (When rbenv install Fails on Apple Silicon)"
author: Seth Jensen
date: 2026-01-12
description: "A simple containerized Ruby setup + mysterious Ruby failures on a MacBook M2"
featured:
  image_url: /blog/2026/01/ruby-in-podman-apple-silicon/newish-ruins.webp
github_issue_number: 2168
tags:
- ruby
- rails
- macos
---

![Amidst dry, leafless brush, a tall structure of dilapidated bricks stands, with a small archway at the bottom in the center of the image](/blog/2026/01/ruby-in-podman-apple-silicon/newish-ruins.webp)

<!-- Photo by Seth Jensen, 2025 -->

I recently worked on a legacy Ruby backend app which hadn't been changed for years. A Ruby development environment used to be provided by [DevCamps](/expertise/version-control-devcamps/) for this site, but over the years we stopped using Ruby other than this small backend, so we also stopped using camps.

The frontend development now uses its own local dev server, so I decided to do the same for the backend by running the Unicorn server locally. I'm on a MacBook M2, so I should just be able to install `rbenv` using Homebrew. Easy, right?

Unfortunately not. I had a great deal of trouble getting any version of Ruby to run natively on my MacBook M2, so I eventually resorted to using Podman. You can [skip to the end for my solution](#third-try-podman).

### First try: native rbenv

The `rbenv` installation went just fine:

```
brew install rbenv ruby-build
```

And after adding `eval "$(rbenv init -)"` to my `~/.zshrc` file, I tried to install the old version of Ruby:

```
rbenv install 2.4.10
```

However, this returned a `BUILD FAILED` message. Strangely, it also failed with a new version of Ruby (3.3.10). I tried debugging for a while before giving up — I figured this project isn't worth multiple hours of getting a local Ruby installation to work (despite my obstinate attempts to do so).

### Second try: mise

Several people on forums & blogs recommended using mise, a language-agnostic version manager. After installing it with Homebrew, I ran:

```
mise use --global ruby@2.4.10
```

This failed too! There was a good explanation, though: older Ruby versions don't run on ARM processors. Of course, that makes sense. So I just needed to install a newer version from after Apple silicon was supported:

```
mise use --global ruby@3.3.10
```

However, this failed as well, just like rbenv:

```
mise ERROR Failed to install core:ruby@3.3.10:
   0: ~/Library/Caches/mise/ruby/ruby-build/bin/ruby-build exited with non-zero status: exit code 1
```

I'm sure there is a way to get Ruby running through a version manager on Apple silicon; I found several [tutorials](https://gorails.com/setup/macos/15-sequoia) claiming you can just run these commands as normal and it'll work. However, after spending longer than I'd like to admit, I was completely unable to do so despite trying many fixes found online.

This may be a unique problem on my machine, or I may be missing something. But the fact was, I'd waited through about a dozen failed Ruby installs (which take a long time!) and I just needed the app to work now. So I moved to a third option: run Ruby in a container.

### Third try: Podman

[Podman](https://podman.io/) is a fully open-source containerization system which can run Dockerfiles and docker-compose.yml files. The app is a lightweight Sinatra backend with Unicorn as a server, and I just needed to add CloudFlare Turnstile to reduce bot traffic.

The app uses two main files: `unicorn.rb` (which holds the configuration for the Unicorn server) and `config.ru` (which defines and runs the Sinatra app). The command to start the app is pretty simple: `bundle exec unicorn -c unicorn.rb config.ru`. I also set up two files for the container: `Containerfile` and `container-compose.yml`.

> Note: Podman does find files named Dockerfile and docker-compose.yml, but here I'm using Podman's convention of Containerfile and container-compose.yml, which takes precedence if both are present in the folder.

To run this, I just needed to set up the environment in my `Containerfile`.

#### `Containerfile`

```containerfile
FROM ruby:2.4.10

WORKDIR /usr/src/app

COPY . .

RUN mkdir -p /var/log && \
 gem i bundler && \
 bundle install

EXPOSE 8080

CMD ["bundle", "exec", "unicorn", "-c", "unicorn.rb", "config.ru"]
```

It's a pretty simple setup:

* set the working directory
* copy files from the source directory into the container
* create the log directory defined in `unicorn.rb`
* install bundler
* install gems from Gemfile.lock
* expose the port defined in `unicorn.rb`
* define the server start command using a `CMD` instruction

#### `container-compose.yml`

```yaml
services:
  backend:
    build:
        context: .
        dockerfile: Containerfile
    volumes:
        - .:/usr/src/app
    ports:
        - "8080:8080"
```

The `volumes` section means that changes on the host machine will be propogated to the container (and vice versa). This means you don't need to rebuild the container when you change the app, instead you can use a change-watching Gem like [rerun](https://github.com/alexch/rerun).

> Note: You can run this without a compose file, the compose file just stores the volume & port information so you can run it more easily.
>
> ```
> podman run -d --name mybackend -v .:/usr/src/app -p 8080:8080 <image_id>
> ```

#### Minimal `unicorn.rb` configuration file

```rb
listen "0.0.0.0:8080"
working_directory "/usr/src/app"
```

This is simple:

* Use `0.0.0.0` to connect to the container's network interface
* Define our listening port
* Set the working directory to the same value as in our `Containerfile`

> Note: When we forward port 8080 to our Podman container, that traffic arrives on the container's network interface, not on its internal loopback (localhost). If your app only listens on localhost, it's essentially saying "I only accept connections from myself," so the forwarded traffic gets rejected. By binding to 0.0.0.0, your app listens on all interfaces, which includes the one Podman uses to route external traffic into the container.

#### Simple `config.ru`

```
require 'sinatra'
get '/' do
  "Hello from Sinatra in Podman!\n"
end
run Sinatra::Application
```

This is also very simple:

* After importing sinatra, define a GET route for the `/` location (so this will be accessed from `localhost:8080/` on the host machine)

```
$ podman build .
$ podman run -p 8080:8080 <image-id>
```

This returned a successful response on my host machine:

```
$ curl localhost:8080
Hello from Sinatra in Podman!
```

When the app failed to run, it kept trying to restart until I moved a .env file into place and it worked. That shows that the volume is working correctly.

I'm not a Ruby expert, but with this setup I was able to convert the JavaScript code for Turnstile to Ruby and get it working!
