---
author: Matt Vollrath
gh_issue_number: 644
tags: git, tips, tools
title: 'EP Meeting: Clean Editor and Git Workflows'
---



Having good editor configurations and Git habits is a great way to make work easier and less tedious. David Christensen showed us how to reduce cruft and leverage advanced features of Git to take control of the code.

<a href="https://www.flickr.com/photos/80083124@N08/7187478135/" title="IMG_0830.JPG by endpoint920, on Flickr"><img alt="IMG_0830.JPG" height="375" src="/blog/2012/06/14/ep-meeting-clean-editor-and-git/image-0.jpeg" width="500"/></a>

Indentation is a big part of reading and understanding code, too important to be ignored. Tabs can be interpreted differently in different editors, so using spaces makes life easier for you and your coworkers. Most editors have automatic indentation and tab translation settings to standardize the workflow. Remember, code should be optimized for humans.

Commit often! If your commit can not be summarized in one sentence, it is probably not granular enough. Don’t hesitate to make multiple commits per work session as you accomplish separate tasks. In your commit messages, describe the ‘why,’ not the ‘how.’ Don’t mix trivial style or whitespace tweaks with actual code modifications, because it makes it harder to catch important changes in diffs. If you make multiple changes to a single file, you can use -p/--interactive mode to commit hunks of code separately.


