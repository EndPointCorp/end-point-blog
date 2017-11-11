---
author: Piotr Hankiewicz
gh_issue_number: 1239
tags: html, php
title: Scrape web content with PHP (no API? no problem)
---

### Introduction

There is a lot of data flowing everywhere. Not structured, not useful pieces of data moving here and there. Getting this data and structuring, processing can make it really expensive. There are companies making billions of dollars just (huh?) for scraping web content and showing in a nice form.

Another reason for doing such things can be for example, lack of an API from a source website. In this case, it's the only way to get data that you need to process.

Today I will show you how to get web data using PHP and that it can be as easy as pie.

### Just do it

There are multiple scraping scripts ready to use. I can recommend one of them: PHP Simple HTML DOM Parser. It's extremely easy to start with and initial cost is almost nothing, it's open sourced also.

First, download a library from an official site: [http://sourceforge.net/project/showfiles.php?group_id=218559](http://sourceforge.net/project/showfiles.php?group_id=218559). You can use a composer version too, it's here: [https://github.com/sunra/php-simple-html-dom-parser](https://github.com/sunra/php-simple-html-dom-parser).

Let's say that you have downloaded this file already. It's just a one PHP file called simple_html_dom.php. Create a new PHP file called scraper.php and include mentioned library like this:

```php
<?php

require('simple_html_dom.php');
```

In our example, we will scrape top 10 trending YouTube videos and create a nice array of links and names out of it. We will use this link: [https://www.youtube.com/feed/trending?gl=GB](https://www.youtube.com/feed/trending?gl=GB).

We need to grab this page first. Using PHP it's just a one additional line in our script:

```php
<?php

require('simple_html_dom.php');

// Create DOM from URL or file
$html = file_get_html('https://www.youtube.com/feed/trending?gl=GB');
```

A PHP object was just created with the YouTube page structure.

Look at the YouTube page structure to find a repeating structure for a list of videos. It's best to use Chrome developer tools and its HTML browser. At the time of writing this post (it can change in the future of course) it's:

```html
<ul class="expanded-shelf-content-list has-multiple-items">
 <li class="expanded-shelf-content-item-wrapper">...</li>
 <li class="expanded-shelf-content-item-wrapper">...</li>
 <li class="expanded-shelf-content-item-wrapper">...</li>
 ...
</ul>
```

Thanks Google! This time it will be easy. Sometimes a structure of the page lacks of classes and ids and it's more difficult to select exactly what we need.

Now, for each item of **expanded-shelf-content-item-wrapper** we need to find its title and url. Using developer tools again, it's easy to achieve:

```html
<a
 class="yt-uix-sessionlink yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 spf-link "
 dir="ltr"
 aria-describedby="description-id-284683"
 title="KeemStar Swatted My Friend."
 href="/watch?v=oChvoP8zEBw">
 KeemStar Swatted My Friend
</a>
```

Jackpot! We have both things that we need in the same HTML tag. Now, let's grab this data:

```php
<?php

require('simple_html_dom.php');

// Create DOM from URL or file
$html = file_get_html('https://www.youtube.com/feed/trending');

// creating an array of elements
$videos = [];

// Find top ten videos
$i = 1;
foreach ($html->find('li.expanded-shelf-content-item-wrapper') as $video) {
        if ($i > 10) {
                break;
        }

        // Find item link element
        $videoDetails = $video->find('a.yt-uix-tile-link', 0);

        // get title attribute
        $videoTitle = $videoDetails->title;

        // get href attribute
        $videoUrl = 'https://youtube.com' . $videoDetails->href;

        // push to a list of videos
        $videos[] = [
                'title' => $videoTitle,
                'url' => $videoUrl
        ];

        $i++;
}

var_dump($videos);
```

Look, it's simple as using CSS. What we just did? First, we extracted all videos and started looping through them here:

```php
foreach ($html->find('li.expanded-shelf-content-item-wrapper') as $video) {
```

Then, just extracted a title and url per each video item here:

```php
// Find item link element
$videoDetails = $video->find('a.yt-uix-tile-link', 0);

// get title attribute
$videoTitle = $videoDetails->title;
```

At the end, we just push an array object with scraped data to the array and dump it. The result looks like this:

```php
array(10) {
  [0]=>
  array(2) {
    ["title"]=>
    string(90) "Enzo Amore & Big Cass help John Cena even the odds against The Club: Raw, July 4, 2016"
    ["url"]=>
    string(39) "https://youtube.com/watch?v=940-maoRY3c"
  }
  [1]=>
  array(2) {
    ["title"]=>
    string(77) "Loose Women Reveal Sex Toys Confessions In Hilarious Discussion | Loose Women"
    ["url"]=>
    string(39) "https://youtube.com/watch?v=Xxzy_bZwNcI"
  }
  [2]=>
  array(2) {
    ["title"]=>
    string(51) "Tinie Tempah - Mamacita ft. Wizkid (Official Video)"
    ["url"]=>
    string(39) "https://youtube.com/watch?v=J4GQxzUdZNo"
  }
  [3]=>
  array(2) {
    ["title"]=>
    string(54) "Michael Gove's Shows you What's Under his Kilt"
    ["url"]=>
    string(39) "https://youtube.com/watch?v=GIpVBLDky30"
  }
  [4]=>
  array(2) {
    ["title"]=>
    string(25) "Deception, Lies, and CSGO"
    ["url"]=>
    string(39) "https://youtube.com/watch?v=_8fU2QG-lV0"
  }
  [5]=>
  array(2) {
    ["title"]=>
    string(68) "Last Week Tonight with John Oliver: Independence Day (Web Exclusive)"
    ["url"]=>
    string(39) "https://youtube.com/watch?v=IQwMCQFgQgo"
  }
  [6]=>
  array(2) {
    ["title"]=>
    string(21) "Last Week I Ate A Pug"
    ["url"]=>
    string(39) "https://youtube.com/watch?v=TTk5uQL2oO8"
  }
  [7]=>
  array(2) {
    ["title"]=>
    string(59) "PEP GUARDIOLA VS NOEL GALLAGHER | Exclusive First Interview"
    ["url"]=>
    string(39) "https://youtube.com/watch?v=ZWE8qkmhGmc"
  }
  [8]=>
  array(2) {
    ["title"]=>
    string(78) "Skins, lies and videotape - Enough of these dishonest hacks. [strong language]"
    ["url"]=>
    string(39) "https://youtube.com/watch?v=8z_VY8KZpMU"
  }
  [9]=>
  array(2) {
    ["title"]=>
    string(62) "We Are America ft. John Cena | Love Has No Labels | Ad Council"
    ["url"]=>
    string(39) "https://youtube.com/watch?v=0MdK8hBkR3s"
  }
}
```

Isn't it easy?

### The end

I have some advice if you want to make this kind of script be processing the same page all the time:

- set the user agent header to simulate a real web browser request,
- make calls with a random delay to avoid blacklisting from a web server,
- use PHP 7,
- try to optimize the script as much as possible.

You can use this script for production code but, to be honest, it's not the most optimal approach. If you are not satisfied, code it by yourself :-).

Nice documentation is located here: [http://simplehtmldom.sourceforge.net/](http://simplehtmldom.sourceforge.net/)


