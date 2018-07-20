---
author: David Christensen
gh_issue_number: 331
tags: postgres
title: 'PostgreSQL: per-version .psqlrc'
---



File this under “you learn something new every day.” I came across this little tidbit while browsing the source code for psql: you can have a per-version .psqlrc file which will be executed only by the psql associated with that major version. Just name the file .psqlrc-$version, substituting the major version for the $version token. So for PostgreSQL 8.4.4, it would look for a file named .psqlrc-8.4.4 in your $HOME directory.

It’s worth noting that the version-specific .psqlrc file requires the full minor version, so you cannot currently define (say) an 8.4-only version which applies to all 8.4 psqls. I don’t know if this feature gets enough mileage to make said modification worth it, but it would be easy enough to just use a symlink from the .psqlrc-$majorversion to the specific .psqlrc file with minor version.

This seems of most interest to developers, who may simultaneously run many versions of psql which may have incompatible settings, but also could come in handy to regular users as well.


