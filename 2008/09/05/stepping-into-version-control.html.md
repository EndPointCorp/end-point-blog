---
author: David Christensen
gh_issue_number: 57
tags: git
title: Stepping into version control
---

It’s no secret that we here at End Point love and encourage the use of version control systems to generally make life easier both on ourselves and our clients. While a full-fledged development environment is ideal for maintaining/​developing new client code, not everyone has the time to be able to implement these.

A situation we’ve sometimes found is clients editing/​updating production data directly. This can be through a variety of means: direct server access, scp/​sftp, or web-based editing tools which save directly to the file system.

I recently implemented a script for a client who uses a web-based tool for managing their content in order to provide transparent version control. While they are still making changes to their site directly, we now have the ability to roll back any changes on a file-by-file basis as they are created, modified, or deleted.

I wanted something that was: (1) fast, (2) useful, and (3) stayed out of the user’s way. I turned naturally to Git.

In the user’s account, I executed `git init` to create a new Git repository in their home directory. I then `git add`ed the relevant parts that we definitely wanted under version control. This included all of the relevant static content, the app server files, and associated configuration: basically anything we want to track changes to.

Finally, I determined the list of directories in which we would like to automatically detect any newly created files. These corresponded to the usual places where new content was apt to show up. I codified the automatic update of the Git repo in a script called git_heartbeat, which is called periodically from cron.

The basic listing for git_heartbeat:

```
#!/bin/bash

# automatically add any new files in these space-separated directories
AUTO_ADD_DIRS="catalogs/acme/pages htdocs"

# make sure we’re in the proper Git checkout directory
cd /home/acme

# actually add any newly created files in $AUTO_ADD_DIRS
find $AUTO_ADD_DIRS -print0 | xargs -0 git add

DATE=`date`

git commit -q -a -m "Acme Co Git heartbeat - $DATE" > /dev/null
```

A few notes:

1. `git commit -a` takes care of the modification/​deletion of any already tracked files. The `git add` ensures that any newly created files are currently in the index and will be included with the commit.
1. if no files have been added, removed, or deleted, no checkpoint is created. This ensures that every commit in the log is meaningful and corresponds to an actual change to the site itself.
1. Compared to other VCSs which keep metadata in each versioned subdirectory (such as Subversion), this approach stays out of the user’s way; we don’t have to worry about the user accidentally overwriting/​deleting data in their upload directories and thus corrupting the repository.
1. This approach is fast; it runs near instantaneously for thousands of files, so we could even push the cron interval to every minute if desired.
1. Once the Git tools are installed, there is no need to set up a central repository; Git repos are very cheap to create/​use and for a use case such as this, require little to no maintenance beyond the initial setup.

Areas of improvement/​known issues:

1. This script could definitely be improved to provide more information about which files were added/​modified/​deleted. However, Git’s own tools work for this: For instance, `git log --stat` will show the files which each heartbeat commit affected.

1. Since this is set up as a general cron job running every hour (the period is configurable, obviously), it does preclude extended stagings for non-heartbeat commits; basically, anything which takes longer than the heartbeat interval will be inadvertently committed.
