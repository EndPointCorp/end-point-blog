---
author: David Christensen
title: 'Tip: Find all non-UTF-8 files'
github_issue_number: 287
tags:
- hosting
- interchange
- tips
date: 2010-04-09
---



Here’s an easy way to find all non-UTF-8 files for later perusal:

```bash
find . -type f | xargs -I {} bash -c "iconv -f utf-8 -t utf-16 {} &>/dev/null || echo {}" > utf8_fail
```

I’ve needed this before for converting projects over into UTF-8; obviously certain files are going to be binary and will show up in this list, so manual vetting will need to be done before converting all your images over into UTF-8.


