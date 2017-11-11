---
author: Greg Sabino Mullane
gh_issue_number: 1211
tags: mediawiki
title: 'MediaWiki extension EmailDiff: notification emails improved'
---

<div class="separator" style="clear: both; float:right; padding: 0 0 .5em 1.5em; text-align: center;"><a href="/blog/2016/03/11/mediawiki-extension-emaildiff/image-0.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2016/03/11/mediawiki-extension-emaildiff/image-0.jpeg"/></a><br/><small><a href="https://flic.kr/p/bdWyHP">Photo</a> by <a href="https://www.flickr.com/photos/karenandbrademerson/">Karen and Brad Emerson</a></small></div>

One of the nice things about MediaWiki is the ability to use 
[extensions](https://www.mediawiki.org/wiki/Manual:Extensions) to extend the core functionality in many ways. I've just released a 
new version of an extension I wrote called EmailDiff that helps provide a much needed 
function. When one is using a MediaWiki site, and a page is on your 
watchlist - or your username is inside  
[the 'UsersNotifiedOnAllChanges' array](https://www.mediawiki.org/wiki/Manual:$wgUsersNotifiedOnAllChanges) - you will receive an email whenever a page 
is changed. However, this email simply gives you the editor's summary and states 
"the page has been changed, here's some links if you want to see exactly what". 
With the EmailDiff extension enabled, a full diff of what exactly has changed is sent 
in the email itself. This is extremely valuable because you can quickly see exactly what has 
changed, without leaving your email client to open a browser (and potentially have to login), 
and without breaking [your flow](https://en.wikipedia.org/wiki/Flow_%28psychology%29).

Normally, a MediaWiki notification email for a page change will look something like this:

```
Subject: MediaWiki page Project:Sandbox requirements has been changed by Zimmerman

Dear Turnstep,

The MediaWiki page Project:Sandbox requirements has been changed on
16 November 2015 by Zimmerman, see
https://www.mediawiki.org/wiki/Project:Sandbox for the
current revision. 

See
https://www.mediawiki.org/w/index.php?title=Project:Sandbox&diff=next&oldid=7076877
to view this change.

See
https://www.mediawiki.org/w/index.php?title=Project:Sandbox&diff=0&oldid=8657769
for all changes since your last visit.

Editor's summary: important thoughts

Contact the editor:
mail: https://www.mediawiki.org/wiki/Special:EmailUser/Zimmerman
wiki: https://www.mediawiki.org/wiki/User:Zimmerman

There will be no other notifications in case of further activity unless
you visit this page while logged in. You could also reset the
notification flags for all your watched pages on your watchlist.

Your friendly MediaWiki notification system

--
To change your email notification settings, visit
https://www.mediawiki.org/wiki/Special:Preferences

To change your watchlist settings, visit
https://www.mediawiki.org/wiki/Special:EditWatchlist

To delete the page from your watchlist, visit
https://www.mediawiki.org/w/index.php?title=Project:Sandbox&action=unwatch

Feedback and further assistance:
https://www.mediawiki.org/wiki/Special:MyLanguage/Help:Contents
```

The above is the default email message for page changes on mediawiki.org. As you can 
see, it is very wordy, but conveys little actual information. In contrast, 
here is the EmailDiff extension, along with the suggested changes in the 
notification email template mentioned below:

```
Subject: MediaWiki page Project:Sandbox requirements has been changed by Zimmerman (diff)

Page: Project:Sandbox
Summary: important thoughts
User: Zimmerman  Time: 11 November 2015

Version differences:
@@ -846,5 +887,3 @@
 In cattle, temperament can affect production traits such as carcass and meat 
 quality or milk yield as well as affecting the animal's overall health and 
-reproduction. Cattle temperament is defined as "the consistent behavioral and physiological 
-difference observed between individuals in response to a stressor or environmental 
+reproduction. If you succeed in tipping a cow only partway, such that only one 
+of its feet is still on the ground, you have created lean beef. Such a feat is 
+well done. Naturally, being outside, the cow is unstable. When it falls over, 
+it becomes ground beef. Cattle temperament is defined as "the consistent behavioral 
+and physiological difference observed between individuals in response to a stressor or environmental 
 challenge and is used to describe the relatively stable difference in the behavioral 
 predisposition of an animal, which can be related to psychobiological mechanisms.
```

That is so much better: short, sweet, and showing exactly the information you need. The 
lack of a diff has long been a pet peeve of mine, so much so that I wrote this 
functionality a long time ago as some hacks to the core code. Now, however, 
everything is bottled up into one neat extension.

This extension works by use of the great 
[hook system of MediaWiki](https://www.mediawiki.org/wiki/Manual:Hooks). In particular, it uses the **SendPersonaliedNotificationEmail** 
hook. It is not yet included in MediaWiki, but I am hoping it will get included for version 1.27. 
The hook fires just before the normal notification email is about to be sent. The extension generates 
the diff, and sticks it inside the email body. It will also append the string '(diff)' to the subject 
line, but that is configurable (see below).

The extension has changed a lot over the years, moving forward along 
with MediaWiki, whose support of extensions gets better all the time. 
The current version of the EmailDiff extension, 1.7, requires a 
MediaWiki version of 1.25 or better, as it uses the 
[new extension.json format](http://blog.endpoint.com/2015/10/mediawiki-extensionjson-change-in-125.html).

Installation is pretty straightforward with four steps. First, visit the 
[official extension page](https://www.mediawiki.org/wiki/Extension:EmailDiff) at mediawiki.org, download the tarball, and untar 
it into your extensions directory. Second, add this line to your 
LocalSettings.php file:

```
wfLoadExtension( 'EmailDiff' );
```

If you need to change any of the configuration settings, add them to 
LocalSettings.php right below the wfLoadExtension 
line. Currently, the only two configuration items are:

- **$wgEmailDiffSubjectSuffix** This is a string that gets added to the 
end of any notification emails that contain a diff. Defaults to ***(diff)***.

- **$wgEmailDiffCommand** This is the command used to execute the diff. 
It should not need to be changed for most systems. Defaults to 
***"/usr/bin/diff -u OLDFILE NEWFILE | /usr/bin/tail --lines=+3 > DIFFFILE"***

As mentioned above, this extension requires the **SendPersonaliedNotificationEmail** hook to exist. 
For the third step, you need to add the hook in if it does not exist by editing the 
includes/mail/EmailNotification.php file. Insert this line at the 
bottom of the **sendPersonalized** function, just before the final return:

```
Hooks::run( 'SendPersonalizedNotificationEmail',
    [ $watchingUser, $this->oldid, $this->title, &$headers, &$this->subject, &$body ] );
```

The final step is to modify the template used to send the notification emails. You can find it 
by editing this page on your wiki: **MediaWiki::Enotif_body**, and adding the string **$PAGEDIFF** 
where you want the diff to appear. I recommend cleaning up the template while you are in there. Here is 
my preferred template:

```
Page: $PAGETITLE
Summary: $PAGESUMMARY $PAGEMINOREDIT
User: $PAGEEDITOR  Time: $PAGEEDITDATE
$PAGEDIFF
 
$NEWPAGE
```

Once installed, you will need to activate the email diffs for one or more users. A new 
[user preference](https://www.mediawiki.org/wiki/Help:Preferences) that allows emailing of diffs has been added. It is off by default; to turn 
it on, a user should visit their "Preferences" link, go to the "User profile" section, and look inside 
the "Email options" for a new checkbox that says "Send a diff of changes" (or the same but in a 
different language, if the 
[localization](https://www.mediawiki.org/wiki/Localisation) has been set up). The checkbox will look like this:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2016/03/11/mediawiki-extension-emaildiff/image-1-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2016/03/11/mediawiki-extension-emaildiff/image-1.png"/></a></div>

Just check the box, click the "Save" button, and your notification emails become 
much more awesome. To enable email diffs for everyone on your wiki, add this line to your 
LocalSettings.php file:

```
$wgDefaultUserOptions['enotifshowdiff'] = true;
```

There are some limitations to this extension that should be mentioned. As each 
page edit will potentially cause three files to be created on the operating system 
as well as invoking an external diff command, large and extremely busy wikis may see a 
performance impact. However, file creations are cheap and the diff command is 
fast, so unless you are Wikipedia, it's probably worth at least testing out to 
see if the impact is meaningful.

I also like these emails as a kind of audit trail for the wiki. On that note, 
email notifications do NOT get sent to changes you have made yourself! Well, they do 
for me, but that has required some hacking of the core MediaWiki code. Maybe someday 
I will attempt to make that into a user preference and/or extension as well. :)
