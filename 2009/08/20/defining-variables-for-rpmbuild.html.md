---
author: Jon Jensen
gh_issue_number: 189
tags: hosting, redhat
title: Defining variables for rpmbuild
---

RPM spec files offer a way to define and test build variables with a directive like this:

```bash
%define <variable> <value>
```

Sometimes it’s useful to override such variables temporarily for a single build, without modifying the spec file, which would make the changed variable appear in the output source RPM. For some reason, how to do this has been hard for me to find in the docs and hard for me to remember, despite its simplicity.

Here’s how. For example, to override the standard _prefix variable with value /usr/local:

```bash
rpmbuild -ba SPECS/$package.spec --define '_prefix /usr/local'
```
