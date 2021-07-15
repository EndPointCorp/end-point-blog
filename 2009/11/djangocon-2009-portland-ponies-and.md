---
author: Adam Vollrath
title: 'DjangoCon 2009: Portland, Ponies, and Presentations'
github_issue_number: 217
tags:
- conference
- django
- python
date: 2009-11-04
---

I attended [DjangoCon](https://web.archive.org/web/20091110110923/http://www.djangocon.org/) this year for the first time, and found it very informative and enjoyable. I hoped to round out my knowledge of the state of the Django art, and the conference atmosphere made that easy to do.

### Presentations

[Avi Bryant](https://about.me/avibryant)’s opening keynote was on the state of web application development, and what Django must do to remain relevant. In the past, web application frameworks did things in certain ways due to the constraints of CGI. Now they’re structured around relational databases. In the future, they’ll be arranged around Ajax and other asynchronous patterns to deliver just content to browsers, not presentation. To wit, “HTML templates should die”, meaning we’ll see more Gmail-style browser applications where the HTML and CSS is the same for each user, and JavaScript fetches all content and provides all functionality. During Q&A, he clarified that most of what he said applies to web applications, not content-driven sites which must be SEO-friendly and so arranged much differently. Many of these themes were serendipitously also in Jacob Kaplan-Moss’ “[Snakes on the Web](https://jacobian.org/writing/snakes-on-the-web/)” talk, which he gave at PyCon Argentina the same week as DjangoCon.

[Ian Bicking](http://www.ianbicking.org/)’s keynote was on open-source as a philosophy; very abstract and philosophical but also interesting. It has been [described](http://www.sauria.com/blog/2009/09/12/djangocon-2009/) as “a free software programmer’s midlife crisis”. [Frank Wiles](https://www.revsys.com/about/bio/frankwiles) of Revolution Systems gave a barn-burner talk on how Django converted him from Perl to Python, followed by another on [Postgres optimization](/technology/postgresql). The latter reflected a theme that all [web developers are now expected to do Operations](http://times.usefulinc.com/2008/06/16-ops-now) as well, with several talks devoted to simple systems administration concepts.

### Deployment

While working on Django projects we’ve been doing this year, I’ve been watching developments around deployment of Python web applications, particularly with Apache. The overwhelming consensus: Without active development, [mod_python](http://www.modpython.org/) is going the way of the dodo. Although [WSGI is architecturally similar to CGI](https://www.b-list.org/weblog/2009/aug/10/wsgi/), the [performance difference can be striking](https://collingrady.wordpress.com/2009/01/06/mod_python-versus-mod_wsgi/). [mod_wsgi](https://code.google.com/archive/p/modwsgi/)’s daemon mode running as a separate user is more secure and flexible than mod_python processes running as the Apache user. Given mod_wsgi’s momentum, it makes sense to use it and avoid mod_python for new projects.

Several other tools kept re-appearing in presenters’ demonstrations. [Fabric](http://www.fabfile.org/) is a remote webapp deployment tool similar to Ruby’s [Capistrano](http://www.capify.org/). Python’s package index, formerly named “[The Cheeseshop](https://www.youtube.com/watch?v=B3KBuQHHKx0)”, has been renamed [PyPI](https://pypi.org/), the Python Package Index. Though easy_install is the standard tool to install PyPI packages, [pip](https://pypi.org/project/pip/) is gaining momentum as its successor. [VirtualEnv](https://pypi.python.org/pypi/virtualenv) is a tool to create isolated Python environments, discrete from the system environment. Since the conference I’ve been exploring how these tools may be leveraged for our own development, and may be integrated into our [DevCamps](http://www.devcamps.org/) multiple-environments system.

### Pinax

The [Eldarion](https://eldarion.com/) folks gave three talks on [Pinax](http://pinaxproject.com/), and the project came up a lot in conversations. If anything could be said to have “buzz” at the conference, this is it. Pinax is a suite of re-usable Django applications, encompassing functionality often-desired, but not common enough to be included in django.contrib. It may be compared to [Drupal](https://www.drupal.org/) and [Plone](https://plone.org/). Its popularity also spurred discussions on what should or should not be included in the Django core, and how all Django developers should make their apps re-usable (some of James Bennett’s favorite topics).

### Community

Among others, I was fortunate to spend time with [Kevin Fricovsky](https://twitter.com/montylounge) and the others who launched the new community site [DjangoDose](https://web.archive.org/web/20090919170130/http://djangodose.com/) during the conference. DjangoDose is a spiritual successor to the now-defunct [This Week in Django](http://www.thisweekindjango.com/) podcast, and was visible on many laptops in the conference room, aggregating [#djangocon tweets](https://www.hashtags.org/analytics/djangocon/).

That’s all I have time to relate now. There was plenty more there and I look forward to following up with people & projects.
