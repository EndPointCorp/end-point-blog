---
author: Richard Templet
gh_issue_number: 369
tags: interchange, seo
title: SEO friendly redirects in Interchange
---



In the past, I've had a few [Interchange](http://www.icdevgroup.org/) clients that would like the ability to be able to have their site do a SEO friendly 301 redirect to a new page for different reasons.  It could be because either a product had gone out of stock and wasn't going to return or they completely reworked their url structures to be more SEO friendly and wanted the link juice to transfer to the new URLs.  The normal way to handle this kind of request is to set up a bunch of Apache rewrite rules.

There were a few issues with going that route.  The main issue is that to add or remove rules would mean that we would have to restart or reload Apache every time a change was made.  The clients don't normally have the access to do this so it meant they would have to contact me to do it.  Another issue was that they also don't have the access to modify the Apache virtual host file to add and remove rules so again, they would have to contact me to do it.  To avoid the editing issue, we could have put the rules in a .htaccess file and allow them to modify it that way, but this can present its own challenges because some text editors and FTP clients don't handle hidden files very well.  The other issue is that even though overall basic rewrite rules are pretty easy to copy, paste and reuse, they still can have nasty side effects if not done properly and can also be difficult to troubleshoot so I devised a way to allow them to be able to manage their 301 redirects using a simple database table and Interchange's Autoload directive.

The database table is a very simple table with two fields.  I called them old_url and new_url with the primary key being old_url.  The Autoload directive accepts a list of subroutines as its arguments so this requires us to create two different GlobalSubs.  One to actually do the redirect and one to check the database and see if we need to redirect.  The redirect sub is really straight forward and looks like this:

```perl
sub redirect {
   my ($url, $status) = @_;
   $status ||= 302;
   $Vend::StatusLine = qq|Status: $status moved\nLocation: $url\n|;
   $::Pragma->{download} = 1;
   my $body = '';
   ::response($body);
   $Vend::Sent = 1;
   return 1;
}
```

The code for the sub that checks to see if we need to redirect looks like this:

```perl
sub redirect_old_links {
   my $db = Vend::Data::database_exists_ref('page_redirects');
   my $dbh = $db->dbh();
   my $current_url = $::Tag->env({ arg => "REQUEST_URI" });
   my $normal_server = $::Variable->{NORMAL_SERVER};
   if ( ! exists $::Scratch->{redirects} ) {
       my $sth = $dbh->prepare(q{select * from page_redirects});
       my $rc  = $sth->execute();
       while ( my ($old,$new) = $sth->fetchrow_array() ) {
           $::Scratch->{redirects}{"$old"} = $new;
       }
       $sth->finish();
   }
   if ( exists $::Scratch->{redirects}  ) {
       if ( exists $::Scratch->{redirects}{"$current_url"} ) {
           my $path = $normal_server.$::Scratch->{redirects}{"$current_url"};
           my $Sub = Vend::Subs->new;
           $Sub->redirect($path, '301');
           return;
       } else {
          return;
       }
   }
}
```

We normally create these as two different files and put them into our own directory structure under the Interchange directory called custom/GlobalSub and then add this, include custom/GlobalSub/*.sub, to the interchange.cfg file to make sure they get loaded when Interchange restarts.  After those files are loaded, you'll need to tell the catalog that you want it to Autoload this subroutine and to do that you use the Autoload directive in your catalog.cfg file like this:

```nohighlight
Autoload redirect_old_links
```

After modifying your catalog.cfg file, you will need to reload your catalog to ensure to change takes effect.  Once these things are in place, you should just be able to add data into the page_redirects table and start a new session and it will redirect you properly.  When I was working on the system, I just created an entry that redirected /cgi-bin/vlink/redirect_test.html to /cgi-bin/vlink/index.html so I could ensure that it was redirecting me properly.


