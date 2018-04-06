---
author: Marina Lohova
gh_issue_number: 757
tags: cloud, hosting
title: Getting started with Heroku
---

It’s becoming increasingly popular to host applications with a nice cloud-based platform like Engine Yard or Heroku.

Here is a little guide showing how to join the development of a Heroku-based project. In Heroku terms it’s called “collaborating on the project”. [The official tutorial](https://devcenter.heroku.com/articles/collab) does provide answers to most of the questions, but I would like to enhance it with my thoughts and experiences.

### First essential question: how to get your hands on the app source code?

I wish Heroku had something like [devcamps](http://www.devcamps.org/) service provided, so you wouldn’t need to experience the hassle of launching the application locally, dealing with the database and system processes needed for development. With Heroku the code does need to be cloned to the local environment like this:

```bash
$ heroku git:clone --app my_heroku_app
```

### Second, how to commit the changes?

I got this error when trying to push to the repository:

```bash
! Your key with fingerprint xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx is not authorized
to access my_heroku_app.
fatal: The remote end hung up unexpectedly
```

Turned out I needed to add the new identity to my local machine.

Also, if you previously had accounts with Heroku with different email address, it’s essential to create the new ssh key just for that application you are collaborating on. Heroku does not allow to use the same ssh key for different accounts.

Here is the full sequence:

```bash
$ ssh-keygen -t rsa -C "yourname@yourdomain.com" -f  ~/.ssh/id_rsa_heroku
$ ssh-add ~/.ssh/id_rsa_heroku
```

and, finally

```bash
$ heroku keys:add ~/.ssh/id_rsa_heroku.pub
$ git push heroku master
```

The code is not only pushed with this command, but it also gets immediately deployed on the server.

### Finally, how to run the application console?

I use application console a lot to debug/troubleshoot/check things after the deployment.

For Heroku it’s the Heroku Toolbelt “run” command that triggers all the usual command line routines. The “-a” parameter is necessary to define the application.

```bash
heroku run -a my_heroku_app script/rails console
```

That’s it! Nice & easy!
