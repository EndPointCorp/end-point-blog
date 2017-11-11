---
author: Jeff Boes
gh_issue_number: 770
tags: seo
title: Google Sitemap rapid deployment
---



I was going to call this "Quick and Dirty Sitemaps", but "Rapid Deployment" sounds more buzz-word-worthy. This is how to get a Google sitemap up and running quickly, using the Google sitemap generator and the Web Developer Firefox plug-in.

I had occasion to set up a sitemap using the [Google sitemap generator](https://sitemap-generators.googlecode.com/svn/trunk/docs/en/sitemap-generator.html) for a site recently. Here's what I did:

 Download the generator using the excellent documentation found at the previous link. Unpack it into a convenient location and copy the example_config.xml file to something else, e.g., www.mysite.com_config.xml. Edit the new configuration file and:

1. Modify the "base_url" setting to your site;
1. Change the "store_into" setting to a file in your site's document root;
1. Add a pointer to a file that will contain your list-of-links, e.g.,
```xml
<urllist path="site_urls.txt">
</urllist>
```

I would locate this in the same path as your new configuration file.

 Now, if you don't already have [Web Developer](http://chrispederick.com/work/web-developer/firefox/), give yourself a demerit and go install it.

 ... 

 Okay, you'll thank me for that. Now pick a few pages from your site: good choices, depending on your site's design, are the home page, the sitemap (if you have one), and any of the top-level "nav links" you may have set up.

 Visit each of those pages in turn. Use Web Developer to assemble the links from the pages, clicking:

1. Tools menu
1. Web Developer extension
1. Information
1. View link information

Copy and paste each informational list-of-links and append it to a text file. You can clean it up a bit when you are done, removing any links you don't want in the sitemap, or you can let the sitemap generator tell you which ones to remove while testing.

You can sort and de-duplicate the file with something like this:

```bash
$ sort site_urls.txt | uniq > site_urls.out
```

Inspect the site_urls.out file and when you're happy with it, rename it to "site_urls.txt".

 You're ready to run the sitemap generator:

```bash
$ python sitemap_gen.py --config=www.mysite.com_config.xml --testing
```

Check the output for warnings, adjust the configuration and/or the site_urls.txt file, and eventually you can run this without the --testing flag. Now you just need to add it to a crontab where it will be run appropriately, and you're done!


