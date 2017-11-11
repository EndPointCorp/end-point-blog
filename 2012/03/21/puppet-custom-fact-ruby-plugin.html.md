---
author: Greg Sabino Mullane
gh_issue_number: 574
tags: automation, ruby, sysadmin
title: Puppet custom facts and Ruby plugins to set a homedir
---



<a href="/blog/2012/03/21/puppet-custom-fact-ruby-plugin/image-0-big.jpeg" imageanchor="1" style="margin-left:1em; margin-bottom:1em"><img border="0" height="249" src="/blog/2012/03/21/puppet-custom-fact-ruby-plugin/image-0.jpeg" width="235"/></a>

Photo of [Swedish Chef](http://www.flickr.com/photos/akuchling/190704045/)
 by [A. M. Kuchling](http://www.flickr.com/photos/akuchling/)

[Puppet](http://docs.puppetlabs.com/learning/) is an indispensable tool for system admins, but it can be tricky 
at times to make it work the way you need it to. One such problem one of our clients 
had recently was that they needed to track a file inside a user's home directory 
via Puppet (a common event). However, for various reasons the user's home directory 
was not the same on all the servers! As Puppet uses hard-coded paths to track files, 
this required the use of a custom Puppet "fact" and a helper Ruby script plugin to solve.

Normally, you can use Puppet to track a file by simply adding a file 
resource section to a puppet manifest. For example, we might control 
such a file inside a manifest named "foobar" by writing the file 
**puppet/modules/foobar/init.pp** as so:

```nohighlight
class foobar {

  user {
    "postgres":
      ensure     =&gt; present,
      managehome =&gt; true;
  }

  file {
    "/home/postgres/.psqlrc":
      ensure      =&gt; present,
      owner       =&gt; postgres,
      group       =&gt; postgres,
      mode        =&gt; 644,
      source      =&gt; [
                      "puppet:///foobar/$pg_environment/psqlrc",
                      "puppet:///foobar/psqlrc",
                      ],
      require     =&gt; User["postgres"];
  }
}
```

This is a bare-bones example (the actual username and file were different), but gets the idea across. 
While we want to ensure that the postgres user has the correct .psqlrc file, we also need to make sure that 
the postgres user itself exists. Hence the **user** section at the top 
of the script. This will ask puppet to create that user if it does not already exist. 
We also added the "managehome" parameter, to ensure that the new user also has a home directory. 
If this parameter is false (or missing), puppet runs a plain 
[useradd](http://www.linfo.org/useradd.html) command (or its equivalent); if the 
parameter is true, it adds the -m or --create-home argument, which is what we need, as we need 
to monitor a file in that directory.

As there is no point in trying to manage the .psqlrc file before the user is created, 
we make the User creation check a pre-requisite via the "require" parameter; basically, 
this helps puppet determine the order in which it runs things (using a directed acyclic 
graph, a feature that should be familiar to git fans).

The **file** resource in this manifest, named "/home/postgres/.psqlrc", ensures 
that the file exists and matches the version stored in puppet. Most of the parameters are 
straightforward, but the **source** is not quite as intuitive. Here, rather than giving 
a simple string as the value for the parameter **source**, we give it an array of 
strings. Puppet will walk through the list until it finds the first one that exists, and use that 
for the actual file to use as **/home/postgres/.psqlrc** on each box using this manifest. 
This allows us to have different versions of the .psqlrc file for different arbitrary classes of boxes, 
but without having to write a separate manifest for each one. Instead, they all use the same manifest 
and simply change the $pg_environment variable, usually at the puppet "role" level.

The syntax **puppet:///foobar/** is a way of telling puppet that the file is 
underneath the main puppet directory, inside the "foobar" directory, and in a subdirectory called 
"files". The level above "files" is where one would create different subdirectories based on 
$pg_environment, so your module might look like this:

```nohighlight
modules/
   └──foobar/
         ├─manifests/
         │     └─init.pp
         └──files/
              ├─psqlrc
              ├─production/
              │     └─psqlrc
              └──development/
                    └─psqlrc
```

In the above, we have three versions of the psqlrc file stored: one for boxes 
with a $pg_environment of "production", one for a $pg_environment of "development", 
and a default one for boxes that do not have $pg_environment set (or whose 
$pg_environment string does not have a matching subdirectory).

All well and good, but the problem comes when the user in question already exists 
on more than one server, and has a different home directory depending on the server! 
We can no longer say "/home/postgres/.psqlrc", because on some boxes, what we really 
want is "/var/lib/pgsql/.psqlrc". There are a couple of wrinkles that prevent us 
from simply saying something like "$HOME/.psqlrc".

The first wrinkle is that Puppet runs as root, and what we need here is the 
$HOME of the postgres user, not root. The second wrinkle is that, even if we were 
to come up with a clever way to figure it out (say, by parsing /etc/passwd with an 
exec resource), we cannot add run-time code to our manifest and have it get stored into a 
variable. The reason is that the first thing Puppet does on a client is compiles all the 
manifests into a static catalog, that is then applied. Which introduces another wrinkle: even 
if we were to somehow know this information beforehand, what about the case where the user does not 
exist? We can ask puppet to create the user, but it is way, way too late in the game 
at that point to apply the location of the new home directory into our manifest.

We stated that the first thing puppet does is compile a catalog, but that's not strictly 
true: it actually walks through the manifests and does a few other things as well, including 
executing any plugins. We can use this fact to create a 
[custom fact](http://docs.puppetlabs.com/guides/custom_facts.html) for each 
client server - this new fact will contain the location of the home directory for the postgres user 
on that server.

There's a few steps to get it all working. The first thing to know is that puppet provides a number of 
"facts" that get stored as simple key/value pairs, and these are available as variables 
you can use inside of your manifests. For example, you can put 
[PostGIS](http://postgis.refractions.net/) on any of your hosts that contain 
the string "gis" somewhere in their hostname by saying:

```ruby
  if $::hostname =~ /gis/ {
    package {
      'postgis':
        ensure =&gt; latest;
    }
  }
```

This list of facts can be expanded by the use of "custom facts", which basically means we add our own 
variables that we can access in our manifests. In this particular case, we are going to create a variable 
named "$postgres_homedir", which we can then utilize in our manifest.

A custom fact is created by a Ruby function: this function should be in its own file, located 
in the "lib/facter" directory of the relevant module. So in our case, we will create a small 
ruby file named "postgres_homedir.rb" and stick it here:

```nohighlight
modules/
   └──foobar/
         ├─lib/
         │  └─facter/
         │       └─postgres_homedir.rb
         ├─manifests/
         │     └─init.pp
         └──files/
              ├─psqlrc
              ├─production/
              │     └─psqlrc
              └──development/
                    └─psqlrc
              
```

The function itself follows a fairly standard format: The only unique parts are 
the actual system calls and the name of the variable:

```ruby
# postgres_homedir.rb

Facter.add("postgres_homedir") do
  setcode do
    system('useradd -m postgres 2&gt;/dev/null')
    Facter::Util::Resolution.exec('/bin/grep "^postgres:" /etc/passwd | cut -d: -f6').chomp
  end
end
```

Since we've already shown how having Puppet create the user happens way too late 
in the game, and because we know that the foobar module always needs that user to exist, 
we've moved the user creation to a simple system call in this Ruby script. The **-m** 
makes sure that a home 
directory is created, and then the next line extracts the home directory and stores it 
in the global puppet variable $postgres_homedir. The 'useradd' line feels the least clean 
of all of this, and alternatives are welcome, but having the system do a 'useradd' and 
returning a (silenced) error each time the puppet client is run seems a fairly 
small price to pay for having this all work (and shorter than checking for existence, 
doing a conditional, etc).

Now that we have a way of knowing what the home directory of the postgres user 
will be *before* the manifest is compiled into a catalog, we can rewrite 
**puppet/foobar/manifests/init.pp** like so:

```nohighlight
class foobar {

  file {

    postgres_psqlrc:
      path        =&gt; "${::postgres_homedir}/.psqlrc",
      ensure      =&gt; present,
      owner       =&gt; postgres,
      group       =&gt; postgres,
      mode        =&gt; 644,
      source      =&gt; [
                      "puppet:///postgres/$pg_environment/psqlrc",
                      "puppet:///postgres/psqlrc",
                      ];
  }
}
```

Voila! We no longer have to worry about the user existing, because we have already 
done that in the Ruby script. We also no longer have to worry about what the 
home directory is set to, for we have a handy top-level variable we can use. Note 
the use of the :: to indicate this is in the root namespace; Puppet variables have 
a scope and a name, such as $alpha::bravo.

Rather than leave the title of this resource as the "path" (most puppet 
resources have sane defaults like that), we have explicitly set the path, as having 
a variable in the resource title is ugly and can make referring to it elsewhere 
very tricky. We also changed the on-disk copy of .psqlrc to psqlrc: while normally 
the files are the same, there is no reason to keep it as a "hidden" file inside the 
puppet repo.

Let's take a look at this module in action. We'll manually run **puppetd** on 
one of our clients, using the 
handy --test argument, which expands to --onetime --verbose --ignorecache 
--no-daemonize --no-usecacheonfailure. Notice how our plugins are retrieved and 
loaded before the catalog is built, and that our postgres user now has the 
file in question:

```bash
$ puppetd --test
info: Retrieving plugin
notice: /File[/var/lib/puppet/lib/facter/postgres_homedir.rb]/ensure: 
  content changed '{md5}0642408678c90dced5c3e34dc40c3415'
    to '{md5}0642408678c90dced5c3e34dc40c3415'
info: Loading downloaded plugin /var/lib/puppet/lib/facter/postgres_homedir.rb
info: Caching catalog for somehost.example.com
info: Applying configuration version '1332065118'
notice: //foobar/File[postgres_psqlrc]/ensure: content changed 
  '{md5}08731a768885aa295d3f0856748f31d5'
    to '{md5}08731a768885aa295d3f0856748f31d5'
Changes:
            Total: 1
Resources:
          Applied: 1
      Out of sync: 1
        Scheduled: 195
            Total: 179
Time:
 Config retrieval: 1.63
             Exec: 0.00
             File: 6.28
       Filebucket: 0.00
            Group: 0.00
        Mailalias: 0.00
          Package: 0.13
         Schedule: 0.00
          Service: 0.51
             User: 0.01
            Total: 8.56
notice: Finished catalog run in 13.26 seconds
```

So we were able to solve out original problem via the use of custom facts, a Ruby 
plugin, and some minor changes to our manifest. While you don't have to go through 
all of this effort often, it's nice that Puppet is flexible enough to allow you 
do so!


