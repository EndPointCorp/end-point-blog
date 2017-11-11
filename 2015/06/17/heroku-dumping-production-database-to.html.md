---
author: Marina Lohova
gh_issue_number: 1135
tags: database, heroku
title: 'Heroku: dumping production database to staging'
---



If you need to dump the production database locally Heroku has a nice set of tools to make this as smooth as humanly possible. In short, remember these two magic words: pg:pull and pg:push. This article details the process [https://devcenter.heroku.com/articles/heroku-postgresql#pg-push-and-pg-pull](https://devcenter.heroku.com/articles/heroku-postgresql#pg-push-and-pg-pull)

However, when I first tried it I had to resolved few issues.

My first problem was:

```
pg:pull not found
```

To fix this:

1. Uninstall the 'heroku' gem with

```
gem uninstall heroku (Select 'All Versions')
```

2. Find your Ruby 'bin' path by running 

```
gem env
```
(it's under 'EXECUTABLE DIRECTORY:')

3. Cd to the 'bin' folder.

4. Remove the Heroku executable with 

```
rm heroku
```

5. Restart your shell (close Terminal tab and re-open)

6. Type 

```
heroku version
```
you should now see something like:

```
heroku-toolbelt/2.33.1 (x86_64-darwin10.8.0) ruby/1.9.3
```

Now you can proceed with the transfer:

1. Type 

```
heroku config --app production-app
```

Note the DATABASE_URL, for example let's imagine that the production database url is HEROKU_POSTGRESQL_KANYE_URL, and the staging database url is HEROKU_POSTGRESQL_NORTH

2. Run

```
heroku pg:pull HEROKU_POSTGRESQL_KANYE rtwtransferdb --app production-app
heroku config --app staging-app
heroku pg:push rtwtransferdb HEROKU_POSTGRESQL_NORTH --app rtwtest
```

This is when I hit the second problem:

```
database is not empty
```

I fixed it by doing:

```
heroku pg:reset HEROKU_POSTGRESQL_NORTH
```

Happy database dumping!


