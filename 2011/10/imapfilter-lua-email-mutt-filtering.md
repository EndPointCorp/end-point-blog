---
author: Greg Sabino Mullane
title: Using the new version of imapfilter with mutt
github_issue_number: 508
tags:
- email
- linux
date: 2011-10-17
---



<a href="/blog/2011/10/imapfilter-lua-email-mutt-filtering/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5664298724633134418" src="/blog/2011/10/imapfilter-lua-email-mutt-filtering/image-0.jpeg"/></a>

Image by Flickr user [p886](https://www.flickr.com/photos/p886/)

My beloved [mutt](http://www.mutt.org/)/imapfilter combo recently stopped working after an operating system switch. (tl;dr: that combo rocks; use *ipairs* instead of *pairs*) When my laptop wireless stopped working, and after spending some time fighting with it, I decided to simply install a new OS. As all of my important data is on a separate partition, this was not that big a deal. I ended up using [Scientific Linux](https://www.scientificlinux.org/), as I’d heard good things about it, and it was one of the few distros that actually would install on my laptop (failures for one reason or another: Fedora, FreeBSD, Ubuntu, and OpenBSD). After the install, I simply copied my ~/.mutt directory and ~/.muttrc file into place, and similarly copied my ~/.imapfilter directory, which contained the all important config.lua file. The [imapfilter program](https://github.com/lefcha/imapfilter) itself was not available via the normal [yum](https://fedoraproject.org/wiki/Yum) repositories, so I simply grabbed the latest and greatest and did a manual install:

```bash
$ git clone https://github.com/lefcha/imapfilter.git
$ cd imapfilter
$ sudo yum install gcc lua-devel openssl-devel pcre-devel
$ make
$ sudo make install
```

I’ve used a lot of email clients over the years (and may have been using email longer than most people reading this). I started out (because that’s all there was) with non-graphical clients such as mail, pine, elm, and mutt. Over the years I also tried out many graphical clients, such as Evolution, Kmail, Eudora, Thunderbird, and Claws Mail. However, nothing ever worked quite right, so I eventually ended up back with mutt, and have been happy with it ever since. The one drawback (or strength) of mutt is its single-mindedness. It does email very well, but lets other tools handle the ancillary tasks. One of those tasks is filtering, and that’s where imapfilter comes in. I like to view all email that comes in, so mutt generally runs with my INBOX open. I scan through the items, marking them urgent if I need to keep them around, and deleting them if they are obvious trash. As needed, I’ll kick off a imapfilter run, which then puts all my read, non-urgent, non-deleted email into the appropriate [IMAP folders](https://en.wikipedia.org/wiki/Internet_Message_Access_Protocol) for me (mutt is even smart enough to realize that the folder was externally changed by imapfilter).

So I tried running imapfilter per usual on my new system and noticed an odd thing: each item in my filter was getting a minimum of 66 ‘hits’, even when there was not even 66 total emails in my inbox! I output the number of matches to each filter I use, so instead of seeing what I was usually did:

```plain
Mediawiki emails moved:    1
Backcountry emails moved:  10
Perl QA messages moved:    0
...
Wiki alerts deleted:       0
Bucardo emails moved:      5
Maatkit emails moved:      0
Mail filtering complete
```

I saw everything at N+66 instead:

```plain
Mediawiki emails moved:   67
Backcountry emails moved: 76
Perl QA messages moved:   66
...
Wiki alerts deleted:      66
Bucardo emails moved:     71
Maatkit emails moved:     66
Mail filtering complete
```

Obviously, something was wonky. Glancing at the release notes showed that version 2.2 changed the format of the search results:

> * Since version 2.2, a different format is used for the returned structures of the searching methods, due to the introduction of multiple mailbox searching and meta-searching, and thus any configuration files that rely on them should be updated*

Okay, but where was the 66 coming from? I created a ~/.imapfilter/test.lua file to show me exactly what was happening inside the loop over the results table. (imapfilter is written in a nice language called [Lua](https://www.lua.org/), which calls its main data structures [“tables”](https://www.lua.org/pil/2.5.html). Probably to the chagrin of those using Lua/database crossover tools like [Pl/Lua](https://github.com/pllua) :) The test.lua file looked like this:

```plain
myaccount = IMAP {
  server   = 'mail.example.com',
  username = 'greg',
  password = 'secret',
  ssl      = 'tls1'
}
inbox = myaccount['INBOX']
result = inbox:contain_subject('bats')

count = 0
for k,v in pairs(result) do 
  count = count + 1 
  if count < 10 then
    print(count, "Call to pairs:",k,v)
  end
end
print("Total count for pairs: " .. count);

count = 0
for k,v in ipairs(result) do 
  count = count + 1 
  if count < 10 then
    print(count, "Call to ipairs:",k,v)
  end
end
print("Total count for ipairs: " .. count);
```

I downloaded and compiled version 2.0 of imapfilter and ran the above code, knowing that there were exactly two emails in my inbox that had a subject containing the string ‘bats’:

```bash
[~/code/imapfilter-2.0] ./imapfilter -c ~/.imapfilter/test.lua
  1      Call to pairs:    9         true
  2      Call to pairs:    32        true
Total count for pairs: 2
Total count for ipairs: 0
```

So it looked like the results table simply contained two entries, with keys of 9 and 32 (which correspond to where those emails happened to appear in my inbox). Calling ipairs yielded zero matches, which makes sense: there is no key of 1 (which is what Lua tables start with by convention, rather than 0 like almost everything else in the computer world :). The ipairs function goes through each key in order starting with 1 until a nil (undefined) key is found. In this case, 1 itself is nil. The output looks much different when I ran it using the new version (2.3) of imapfilter:

```plain
[~/code] imapfilter -c ~/.imapfilter/test.lua
  1      Call to pairs:    1              table: 0x82b0bd8
  2      Call to pairs:    2              table: 0x82b0c48
  3      Call to pairs:    _union         function: 0x81d48d0
  4      Call to pairs:    _mt            table: 0x82a32d0
  5      Call to pairs:    mark_answered  function: 0x81cefe0
  6      Call to pairs:    send_query     function: 0x81d8180
  7      Call to pairs:    is_flagged     function: 0x81c1878
  8      Call to pairs:    unmark_deleted function: 0x81bd890
  9      Call to pairs:    match_message  function: 0x81cd7f8
Total count for pairs: 68
  1      Call to ipairs:    1        table: 0x82b0bd8
  2      Call to ipairs:    2        table: 0x82b0c48
Total count for ipairs: 2
```

This tells us a quite a few things, and solves the mystery of the 66, which represents some meta-data stored in the results table. So rather than treating results as a simple key/value hash with one entry per match, the results table is now a dual-purpose table where the hash part of it contains some meta-data, while the actual matches are stored in the array (indexed) part of the table. Note how the counting of the matches now starts at 1 and increments, rather than using the position in the inbox, as it did before. Which means we must use ipairs to iterate through the table and get our matching entries, in this case with keys 1 and 2.

(If the “table” structure in Lua looks odd to you, that’s because it is. I don’t think I would have designed things that way myself—​while it’s clever to have a single structure that behaves as both an array with indices and a btree hash, it can lead to confusion and some ugly corner cases).

The next step was to get my filters working again—​this was simply a matter of a global search and replace (M-x query-replace-regexp) from “pairs” to “ipairs”.This is a good a point as any to explain what my file looks like (stored as ~/.imapfilter/config.lua). The first part simply sets some common options—​for details on what they do, check out the [manpage for imapfilter_config](http://manpages.ubuntu.com/manpages/bionic/en/man5/imapfilter_config.5.html).

```plain
options.cache        = true
options.certificates = true
options.create       = false
options.info         = false
options.close        = true
options.expunge      = false
```

Next, a new table is created with the IMAP function. After that, we exclude all messages that are already marked as deleted, that have not yet been read, and have not been flagged. In other words, everything in my inbox I’ve already seen, but not flagged as urgent or deleted. The ‘*’ in this case is a logical ‘AND’, and the output is the search result table we saw in the above code.

```plain
myaccount = IMAP {
  server   = 'mail.example.com',
  username = 'greg',
  password = 'secret,
  ssl      = 'tls1'
}

baseresult = inbox:is_seen() * inbox:is_unflagged() * inbox:is_undeleted()
```

Now that we have a search result, we simply start looking for things of interest and handling them. For example, to move messages to an existing IMAP folder:

```plain
-- Put Mediawiki messages into their folder
result = baseresult
  * (
    inbox:contain_to('@lists.wikimedia.org')
    + inbox:contain_to('@lists.wikimedia.org')
  )
count = 0 for k,v in ipairs(result) do count = count + 1 end
if count > 0 then
  inbox:move_messages(myaccount['INBOX/mediawiki'], result)
end
print('Mediawiki emails moved:        ' .. count)
```

Searches can be applied to an existing search result to create a new table. In the code above, a new table named ‘result’ is created that is based off of our ‘baseresult’ table, with the condition that only entries matching a specific “To” or “Cc” field are added.The ‘+’ acts as as a logical ‘OR’.

Deletion is handled in a similar way:

```plain
-- Delete wiki alerts
result = baseresult
  * inbox:contain_from('WikiAdmin <wikiadmin@example.com>')
  * inbox:contain_subject('has been')
count = 0 for k,v in ipairs(result) do count = count + 1 end
if count > 0 then
  inbox:delete_messages(result)
end
print('Wiki alerts deleted:           ' .. count)
</wikiadmin@example.com>
```

The rest of my config.lua file is more filtering sections, similar to the above. Adding a new filter is as easy as creating a new section similar to the above by editing the ~/.imapfilter/config.lua file. While that’s not as automated as it could be, filter adjustment happens so rarely I have never been bothered by that step.

If you are not using imapfilter, you should check it out, even if you are not using mutt; imapfilter is completely independent of your email reading program, and can be run from anywhere, as it doesn’t save or read anything locally. I find that imapfilter is very fast, so even when I used mail programs with built-in filters, I still employed imapfilter from time to time for bulk deletes and moves. Plus, it’s a great way to dip your toe into Lua if you are not familiar with it (although without using some of its more interesting features, such as coroutines).


