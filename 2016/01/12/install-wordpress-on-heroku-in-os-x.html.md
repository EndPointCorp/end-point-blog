---
author: Marina Lohova
gh_issue_number: 1191
tags: apache, heroku, php, wordpress
title: Install WordPress on Heroku in OS X Yosemite
---

I wanted to install WordPress locally for my blog (about programming!), but using MAMP, XAMP or even Vagrant for this seemed overkill. I wanted a light setup. PHP and Apache are already integrated into Mac OS X, so why not use them? I wanted to deploy the app to Heroku, so that was another thing, since Heroku only provides PostgreSQL, not MySQL, out of the box. I’d like to share my research on how I did it.

### WordPress with Heroku support

I found [this handy WordPress template with built-in Heroku support](https://github.com/mhoofman/wordpress-heroku). It has everything one needs to run WordPress on Heroku: PostgreSQL for WordPress (because MySQL on Heroku is a paid service), Amazon S3 and Cloudfront for your uploads since Heroku has an ephemeral file system, WP Sendgrid to send emails and WordPress HTTPS. Check out a copy with this command:

```bash
git clone https://github.com/mhoofman/wordpress-heroku.git
```

Let’s run the project locally first because a file cannot be written to Heroku’s file system, and updating and installing plugins or themes should be done locally anyways and then pushed to Heroku. I’m using [PhpStorm](https://www.jetbrains.com/phpstorm/) for my PHP development.

### Configuring Apache

```bash
mkdir -p ~/Sites
echo "<html><body><h1>my site works</h1></body></html>" > ~/sites/index.html.en
```

Enable PHP support:

```bash
sudo vi /etc/apache2/httpd.conf
```

Uncomment the following lines to look like this:

```nohighlight
LoadModule php5_module libexec/apache2/libphp5.so
LoadModule userdir_module libexec/apache2/mod_userdir.so
Include /private/etc/apache2/extra/httpd-userdir.conf
```

Save and exit. Open the following file:

```bash
sudo vi /etc/apache2/extra/httpd-userdir.conf
```

Uncomment the following line to look like this:

```nohighlight
Include /private/etc/apache2/users/*.conf
```

Save and exit. Open or create:

```bash
sudo vi /etc/apache2/users/~YOURUSERNAME.conf
```

Type the following in there:

```nohighlight
<Directory "/Users/~YOURUSERNAME/Sites/">
    AddLanguage en .en
    LanguagePriority en fr de
    ForceLanguagePriority Fallback
    Options Indexes MultiViews
    AllowOverride None
    Order allow,deny
    Allow from localhost
    Require all granted
</Directory>
```

Restart Apache with:

```bash
sudo apachectl restart
```

Go to http://localhost/~YOURUSER/wordpress-heroku/ and enjoy the results of your work! OK, not so fast! There are more steps to make it happen ;)

### Enabling PostgreSQL for PHP

```nohighlight
Your PHP installation appears to be missing the PostgreSQL extension which is required by WordPress with PG4WP.
```

Here is a handy script to fix this problem [Install PHP PGSQL extensions on Mac OS X Yosemite (change PHP_VER with your PHP version)](https://gist.github.com/marinalohova/ec5d77ffd9d8e8acce2c).

### Creating the database

Hit http://localhost/~YOURUSER/blog-heroku/wp-admin/install.php

```html
Error establishing a database connection
```

The template we are using is tailored for the deployment to Heroku, which means wp-config.php takes its values from the DATABASE_URL environment variable that Heroku config creates in local environment pointing to the database source on Heroku servers.

```bash
pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
> createdb wordpress
> psql wordpress
CREATE USER wordpress WITH PASSWORD 'wordpress';
GRANT ALL PRIVILEGES ON DATABASE wordpress to wordpress; 
```

In wp-config.php, edit as follows. Make sure it matches the database and user that you just created.

```php
$db = parse_url($_ENV["DATABASE_URL"] ? $_ENV["DATABASE_URL"] : "postgres://wordpress:wordpress@localhost:5432/wordpress");
```

Now 5 hours later, you are completely ready for the famous 5-min install ;D. Go to http://localhost/~YOURUSER/blog-heroku/wp-admin/install.php

### Uploading the custom theme/plugin

What to do next? Of course, upload a custom theme or plugin.

```nohighlight
Unable to create directory wp-content/uploads/2015/08. Is its parent directory writable by the server?
$ cd ~/Sites/THESITE
$ sudo chown -R _www wordpress
$ sudo chmod -R g+w wordpress
```

If you encounter an error asking you for FTP credentials in order to do this:

```nohighlight
To perform the requested action, WordPress needs to access your web server.
Please enter your FTP credentials to proceed.

If you do not remember your credentials, you should contact your web host.
```

The problem is that Apache HTTP Server in Mac OS X runs under the user account _www which belongs to the group _www. To allow WordPress to perform operations with Apache, one way to do this is to change the owner of the wordpress directory and its contents to _www. Keep the group as staff, a group to which your user account belongs and give write permissions to the group.

```bash
$ cd ~/Sites/THESITE
$ sudo chown -R _www wordpress
$ sudo chmod -R g+w wordpress
```

This way, no file nor directory is world-writable.

Remember to commit your plugins/themes because due to the nature of Heroku all of the files will be overwritten there if uncommitted or not in the database, effectively wiping out all of your changes at each server restart if you do them on the server.

I installed this pretty theme for myself called Literatum—​just bragging.

### Deployment to Heroku

One of the most exciting last steps. This will make your blog visible to the world! Commit the changes:

```bash
rm -rf .git
git init
git add .
git commit -m "Initial commit"
```

Create Heroku app:

```bash
$ cd wordpress-heroku
$ heroku create
$ heroku addons:create heroku-postgresql
$ heroku pg:promote HEROKU_POSTGRESQL_INSTANCE
$ heroku addons:create sendgrid:starter
```

Your first deployment!

```bash
git push heroku master
```

Go to http://YOURAPP.herokuapp.com/wp-admin/install.php and run the famous 5-minute setup again, activate all the plugins and the chosen custom theme aaand... You are done!

Hope you will find this write-up useful and it will help you create your blog on the web!
