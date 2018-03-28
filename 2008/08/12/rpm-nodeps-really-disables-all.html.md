---
author: Jon Jensen
gh_issue_number: 42
tags: interchange, redhat
title: 'RPM --nodeps really disables all dependency logic'
---

I was surprised about something non-obvious in RPM’s dependency handling for the second time today, the first time having been so many years ago that I had completely forgotten.

When testing out an RPM install without having all the required dependencies installed on the system, it’s natural to do:

```
rpm -ivh $package --nodeps
```

The --nodeps option allows RPM to continue installing despite the fact that I’m missing a handful of packages that $package depends on. This shouldn’t be done as a matter of course, but for a quick test, is fine. So far so good.

However, I found out by confusing experience that --nodeps not only allows otherwise fatal dependency errors to be skipped, but it also disables RPM’s entire dependency tracking system!

I was working with 3 RPMs, a base interchange package and 2 ancillary interchange-* packages which depend on the base package, such as here:

```
interchange-5.6.0-1.x86_64.rpm
interchange-standard-5.6.0-1.x86_64.rpm
interchange-standard-demo-5.6.0-1.x86_64.rpm
```

Then when I installed them all at once:

```
rpm -ivh interchange-*.rpm --nodeps
```

I expected interchange to be installed first, followed by either of the interchange-standard-* packages that depend on it.

However, --nodeps disables RPM’s tracking of those dependencies, causing them to be installed in what happened to be a pessimistic order that breaks many things. Since the interch user and group that the interchange package creates doesn’t exist yet, files can’t be owned by the correct user/group. And since the configuration file /etc/interchange.cfg doesn’t exist yet, the interchange-standard-demo package can’t register itself there.

I wasn’t able to see this till I had Kiel Christofferson join me in a shared screen and watch as I typed my install command. As I spoke aloud --nodeps to Kiel, I suddenly remembered my past experience with this and felt appropriately stupid.

What I really want is not to have no dependency checking at all, but rather something like a hypothetical --ignore-deps-errors option. Changing the behavior of --nodeps to do just that would probably be friendlier overall, but perhaps there’s a reason for its current behavior ...

As an aside, I will note that the RPM specfile PreReq tag [has been deprecated](http://ftp.rpm.org/max-rpm/s1-rpm-depend-manual-dependencies.html#S3-RPM-DEPEND-PREREQ) and is now a synonym for Requires.
