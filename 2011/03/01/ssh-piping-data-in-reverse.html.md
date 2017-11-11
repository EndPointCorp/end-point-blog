---
author: David Christensen
gh_issue_number: 421
tags: sysadmin, tips
title: 'SSH: piping data in reverse'
---



I found myself ssh'd several hops away and needing to copy output from a script back to localhost.  Essentially what I wanted was a way to get the data in question piped backwards from my SSH connection so I could capture it locally.  Since I utilize .ssh/config extensively, I could connect to the server in question from localhost with a single ssh command, however bringing the data back the other way would make it a multi-step process of saving a temporary file, copying it to a commonly accessible location which had the permissions/authentication setup or intermediately sshing to each node along the path -- in short it exceeded my laziness threshold.  So instead, I did the following:

```bash
[me@localhost]$ ssh user@remote nc -l 11235 > output.file  # long, complicated connection hidden behind .ssh/config + ProxyCommand

[me@remotehost]$ perl -ne 'print if /startpat/ .. /endpat/' file/to/be/extracted | nc localhost 11235
```

I ended up choosing an arbitrary port and ran a remote listen process via ssh to pass on any output directed to the specific remote port and capturing as STDOUT on my local machine.  There are a couple reasons I think this setup is nicer when compared to just running ssh user@remote perl -ne ... directly:

- You can take your time to figure out the exact command invocation you would like to use—i.e., you can twiddle with the local command output, then when you're happy with the output, pipe it back.
- You avoid extra worries about escaping/quoting issues.  Particularly if you're running a complicated pipeline remotely, it's hard to craft the exact remote command you would like ssh to execute without a few missteps, or at least a concerted effort to review/verify.  (Anyone who's tried to pass arguments containing whitespace to a remote command will know the pain I'm talking about.)


