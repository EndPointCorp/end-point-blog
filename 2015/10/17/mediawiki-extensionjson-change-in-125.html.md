---
author: Greg Sabino Mullane
gh_issue_number: 1164
tags: json, mediawiki, extensions
title: MediaWiki extension.json change in 1.25
---

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/10/17/mediawiki-extensionjson-change-in-125/image-0-big.png" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/10/17/mediawiki-extensionjson-change-in-125/image-0.png"/></a></div>

I recently released a new version of the
[MediaWiki](https://www.mediawiki.org/wiki/MediaWiki)
[“Request Tracker” extension](https://www.mediawiki.org/wiki/Extension:RequestTracker), which provides
a nice interface to your
[RequestTracker](https://bestpractical.com/rt/) instance, allowing you to view the tickets right
inside of your wiki. There are two major changes I want to point out. First, the name has
changed from **“RT”** to **“RequestTracker”**. Second, it is using the brand-new way of writing
MediaWiki extensions, featuring the extension.json file.

The name change rationale is easy to understand: I wanted it to be more intuitive and easier to find. A search for
“RT” on mediawiki.org ends up finding references to the WikiMedia RequestTracker system,
while a
[search for “RequestTracker”](https://www.mediawiki.org/w/index.php?search=RequestTracker)
finds the new extension right away. Also, the name was
too short and failed to indicate to people what it was. The “rt” tag used by the extension stays
the same. However, to produce a table showing all open tickets for user “alois”, you still write:

```
<rt u='alois'></rt>
```

The other major change was to modernize it. As of version 1.25 of MediaWiki,
extensions are encouraged to use a new system to register themselves with MediaWiki. Previously,
an extension would have a PHP file named after the extension that was responsible for doing
the registration and setup—usually by mucking with global variables! There was no
way for MediaWiki to figure out what the extension was going to do without parsing the entire file, and
thereby activating the extension. The new method relies on a standard JSON file called
extension.json. Thus, in the RequestTracker extension, the file RequestTracker.php has
been replaced with the much smaller and simpler extension.json file.

Before going further, it should be pointed out that this is a big change for extensions,
and was not without controversy. However, as of MediaWiki 1.25 it is the new standard for extensions, and I think
the project is better for it. The old way will continue to be supported, but extension
authors should be using extension.json for new extensions, and converting existing
ones over. As an aside, this is another indication that [JSON](http://json.org/) has won the data format war.
Sorry, [XML](http://www.json.org/xml.html), you were too big and bloated. Nice try [YAML](http://yaml.org/), but you were a little *too* free-form. JSON isn’t perfect,
but it is the best solution of its kind. For further evidence, see Postgres,
which now has [outstanding support for JSON and JSONB](https://www.postgresql.org/docs/current/static/datatype-json.html). I added support for YAML output to EXPLAIN
in Postgres some years back, but nobody (including me!) was excited enough about YAML to do
more than that with it. :)

The extension.json file asks you to fill in some standard metadata fields about the extension, which are then used by MediaWiki to register and set up the extension. Another advantage
of doing it this way is that you no longer need to add a bunch of ugly include_once()
function calls to your LocalSettings.php file. Now, you simply call the name of the extension as an argument to the wfLoadExtension() function. You can even load multiple extensions at once with wfLoadExtensions():

```
## Old way:
require_once("$IP/extensions/RequestTracker/RequestTracker.php");
$wgRequestTrackerURL = 'https://rt.endpoint.com/Ticket/Display.html?id';

## New way:
wfLoadExtension( 'RequestTracker' );
$wgRequestTrackerURL = 'https://rt.endpoint.com/Ticket/Display.html?id';

## Or even load three extensions at once:
wfLoadExtensions( array( 'RequestTracker', 'Balloons', 'WikiEditor' ) );
$wgRequestTrackerURL = 'https://rt.endpoint.com/Ticket/Display.html?id';

```

Note that configuration changes specific to the extension still must be defined in
the LocalSettings.php file.

So what should go into the extension.json file? The
[extension development documentation](https://www.mediawiki.org/wiki/Manual:Developing_extensions) has some suggested
fields, and you can also view the [canonical extension.json schema](https://phabricator.wikimedia.org/diffusion/MW/browse/master/docs/extension.schema.v2.json). Let’s take a quick look at the RequestTracker/extension.json file. Don’t worry, it’s not
too long.

```perl
{
    "manifest_version": 1,
    "name": "RequestTracker",
    "type": "parserhook",
    "author": [
        "Greg Sabino Mullane"
    ],
    "version": "2.0",
    "url": "https://www.mediawiki.org/wiki/Extension:RequestTracker",
    "descriptionmsg": "rt-desc",
    "license-name": "PostgreSQL",
    "requires" : {
        "MediaWiki": ">= 1.25.0"
    },
    "AutoloadClasses": {
        "RequestTracker": "RequestTracker_body.php"
    },
    "Hooks": {
        "ParserFirstCallInit" : [
            "RequestTracker::wfRequestTrackerParserInit"
        ]
    },
    "MessagesDirs": {
        "RequestTracker": [
            "i18n"
            ]
    },
    "config": {
        "RequestTracker_URL": "http://rt.example.com/Ticket/Display.html?id",
        "RequestTracker_DBconn": "user=rt dbname=rt",
        "RequestTracker_Formats": [],
        "RequestTracker_Cachepage": 0,
        "RequestTracker_Useballoons": 1,
        "RequestTracker_Active": 1,
        "RequestTracker_Sortable": 1,
        "RequestTracker_TIMEFORMAT_LASTUPDATED": "FMHH:MI AM FMMonth DD, YYYY",
        "RequestTracker_TIMEFORMAT_LASTUPDATED2": "FMMonth DD, YYYY",
        "RequestTracker_TIMEFORMAT_CREATED": "FMHH:MI AM FMMonth DD, YYYY",
        "RequestTracker_TIMEFORMAT_CREATED2": "FMMonth DD, YYYY",
        "RequestTracker_TIMEFORMAT_RESOLVED": "FMHH:MI AM FMMonth DD, YYYY",
        "RequestTracker_TIMEFORMAT_RESOLVED2": "FMMonth DD, YYYY",
        "RequestTracker_TIMEFORMAT_NOW": "FMHH:MI AM FMMonth DD, YYYY"
    }
}
```

The first field in the file is manifest_version, and simply indicates the extension.json schema version. Right now it is marked as required, and I figure it does no harm to throw it in there. The name field should be self-explanatory, and should match your CamelCase extension name, which will also be the subdirectory where your extension will live under the extensions/ directory.
The type field simply tells what kind of extension this is, and is mostly used to determine which section of the Special:Version page an extension will appear under. The author is also self-explanatory, but note that this is a JSON array, allowing for multiple items if needed. The version and url are highly recommended. For the license, I chose the dirt-simple [PostgreSQL license](https://opensource.org/licenses/postgresql), whose only fault is its name. The descriptionmsg is what will appear as the description of the extension on the Special:Version page. As it is a user-facing text, it is subject to
internationalization, and thus **rt-desc** is converted to your current language by looking up the language file inside of the extension’s i18n directory.

The requires field only supports a “MediaWiki” subkey at the moment. In this case, I have it
set to require at least version 1.25 of MediaWiki—as anything lower will not even be able to read
this file! The AutoloadClasses key is the new way of loading code needed by the extension. As before, this should be stored in a php file with the name of the extension, an underscore, and the word “body” (e.g. RequestTracker_body.php). This file contains all of the functions that perform the actual work of the extension.

The Hooks field is one of the big advantages of the new extension.json format. Rather than
worrying about modifying global variables, you can simply let MediaWiki know what functions
are associated with which hooks. In the case of RequestTracker, we need to do some magic whenever
a **<rt>** tag is encountered. To that end, we need to instruct the parser that we will be handling
any **<rt>** tags it encounters, and also tell it what to do when it finds them. Those details
are inside the wfRequestTrackerParserInit function:

```php
function wfRequestTrackerParserInit( Parser $parser ) {

    $parser->setHook( 'rt', 'RequestTracker::wfRequestTrackerRender' );

    return true;
}
```

The config field provides a list of all user-configurable variables used by the extension, along with their default values.

The MessagesDirs field tells MediaWiki where to find your localization files. This
should always be in the standard place, the i18n directory.
Inside that directory are localization files, one for each language, as well as a special
file named qqq.json, which gives information about each message
string as a guide to translators. The language files are of the format “xxx.json”, where
“xxx” is the language code. For example, RequestTracker/i18n/en.json
contains English versions of all the messages used by the extension. The i18n files look like this:


```
$ cat en.json
{
  "rt-desc"       : "Fancy interface to RequestTracker using <code>&lt;rt&gt;</code> tag",
  "rt-inactive"   : "The RequestTracker extension is not active",
  "rt-badcontent" : "Invalid content args: must be a simple word. You tried: <b>$1</b>",
  "rt-badquery"   : "The RequestTracker extension encountered an error when talking to the RequestTracker database",
  "rt-badlimit"   : "Invalid LIMIT (l) arg: must be a number. You tried: <b>$1</b>",
  "rt-badorderby" : "Invalid ORDER BY (ob) arg: must be a standard field (see documentation). You tried: <b>$1</b>",
  "rt-badstatus"  : "Invalid status (s) arg: must be a standard field (see documentation). You tried: <b>$1</b>",
  "rt-badcfield"  : "Invalid custom field arg: must be a simple word. You tried: <b>$1</b>",
  "rt-badqueue"   : "Invalid queue (q) arg: must be a simple word. You tried: <b>$1</b>",
  "rt-badowner"   : "Invalid owner (o) arg: must be a valud username. You tried: <b>$1</b>",
  "rt-nomatches"  : "No matching RequestTracker tickets were found"
}

$ cat fr.json
{
  "@metadata": {
     "authors": [
         "Josh Tolley"
      ]
  },
  "rt-desc"       : "Interface sophistiquée de RequestTracker avec l'élement <code>&lt;rt&gt;</code>.",
  "rt-inactive"   : "Le module RequestTracker n'est pas actif.",
  "rt-badcontent" : "Paramètre de contenu « $1 » est invalide: cela doit être un mot simple.",
  "rt-badquery"   : "Le module RequestTracker ne peut pas contacter sa base de données.",
  "rt-badlimit"   : "Paramètre à LIMIT (l) « $1 » est invalide: cela doit être un nombre entier.",
  "rt-badorderby  : "Paramètre à ORDER BY (ob) « $1 » est invalide: cela doit être un champs standard. Voir le manuel utilisateur.",
  "rt-badstatus"  : "Paramètre de status (s) « $1 » est invalide: cela doit être un champs standard. Voir le manuel utilisateur.",
  "rt-badcfield"  : "Paramètre de champs personalisé « $1 » est invalide: cela doit être un mot simple.",
  "rt-badqueue"   : "Paramètre de queue (q) « $1 » est invalide: cela doit être un mot simple.",
  "rt-badowner"   : "Paramètre de propriétaire (o) « $1 » est invalide: cela doit être un mot simple.",
  "rt-nomatches"  : "Aucun ticket trouvé"
}
```

One other small change I made to the extension was to allow both ticket numbers and queue names
to be used inside of the tag. To view a specific ticket, one was always able to do this:

```
<rt>6567</rt>
```

This would produce the text “RT #6567”, with information on the ticket available on mouseover,
and hyperlinked to the ticket inside of RT. However, I often found myself using this extension
to view all the open tickets in a certain queue like this:

```
<rt q="dyson"></rt>
```

It seems easier to simply add the queue name inside the tags, so in this new version
one can simply do this:

```
<rt>dyson</rt>
```

If you are running MediaWiki 1.25 or better, try out the new RequestTracker extension! If
you are stuck on an older version, use the RT extension and upgrade as soon as you can. :)
