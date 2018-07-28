---
author: Brian Gadoury
gh_issue_number: 425
tags: javascript, jquery, php, sysadmin
title: 'jQuery and Long-Running Web App Processes: A Case Study'
---



I was recently approached by a client’s system administrator with a small but interesting training/development project. The sys-admin, named Rod, had built a simple intranet web application that used a few PHP pages, running on an Amazon EC2 instance, to accept some user input and kick off multiple long-running server side QA deployment processes. He wanted to use Ajax to start the process as well as incrementally display its output, line-by-line, on the same web page. However, waiting for the entire process to finish to display its output was a poor user experience, and he wasn’t able to get an Ajax call to return any output incrementally over the lifetime of the request.

Rod asked me to help him get his web app working and train him on what I did to get it working. He admitted that this project was a good excuse for him to learn a bit of [jQuery](https://jquery.com/) (a good example of [keeping your tools sharp](/blog/2010/10/12/keep-your-tools-sharp-to-avoid-personal)) even if it wasn’t necessarily the best solution in this case. I have always enjoy training others, so we fired up Skype, got into an IRC channel, and dove right in.

First, I started with the javascript development basics: 

1. Install the [Firebug add-on for Firefox](https://getfirebug.com/)

1. Use Firebug’s Console tab to watch for javascript errors and warnings

1. Use Firebug’s Net tab to monitor what ajax calls your app is making, and what responses they are getting from the server

1. Replace all those hateful debug alert() calls with console.log() calls, especially for ajax work 

A special note about console.log(): Some browsers (including any Firefox that doesn’t have Firebug installed) do not natively supply a console object. To work around this, we defined the following console.log stub at the very top of our single javascript file:

```javascript
if (typeof console === 'undefined') {
    console = { log: function() {} };
}
```

Rod’s javascript was a mix of old-school javascript that he had remembered from years ago, and new-school jQuery he had recently pulled from various tutorials. His basic design was this: When the user clicked the “Deploy” button, it should kick off two separate Ajax requests; “Request A” would initiate a POST request to deploy.php. Deploy.php made a number of system calls to call slow-running external scripts, and logged their output to a temporary logfile on the server. “Request B” would make a GET request to getoutput.php every 2 seconds (which simply displayed the output of said logfile) and display its output in a scrollable div element on the page.

Hearing Rod describe it to me, I wondered if he might be headed down the wrong path with his design. But, he already had put time into getting the server-side code working and did not want to change direction at this point. Discussing it with him further, it became clear that he did not want to re-write the server-side code and that we could in fact make his current design produce working code with teachable concepts along the way.

To start, Rod told me that his “[ajax POST request](https://api.jquery.com/jQuery.ajax/) (Request A) wasn’t firing.” As the Russian proverb says, “Trust, but verify.” So, we opened Firebug’s Net tab, clicked the web app’s Deploy button (actually its only button—​Steve Jobs look out) and saw that the ajax request was in fact firing. However, it was not getting back a successful HTTP 200 status code and as such, was not getting handled by jQuery as Rod expected. Expanding the ajax request in the Net tab let us see exactly what name/value data that was getting POSTed. We spotted a typo in one of his form input names and fixed it. Now Request A was clearly firing, POSTing the correct data to the correct URL, and getting recognized as successful by jQuery. (More on this in a bit.)

Rod’s code was making Request A from within a jQuery event handler defined for his form’s Deploy button. But, he was making Request B via an HTML onClick attribute within that same HTML tag. He was getting all sorts of strange results with that setup based on which request was returning first, if Request B’s function call was correctly returning false to prevent the entire form from getting POSTed to itself, etc. Consolidating logic and control into event handlers that are defined in one place is preferable to peppering a web page with HTML onClick, onChange, etc. javascript calls. So, we refactored his original jQuery event handler and onClick javascript call into the following code snippet: 

```javascript
//global variable for display_output() interval ID
var poll_loop;

$(".deploy_button").click(function() {
    $.ajax({
        beforeSend: function() {
            $('#statusbox').html("Running deployment...");
        },
        type: "POST",
        url: "deploy.php",
        data: build_payload(),
        success: function() {
            console.log('Qa-run OK');
            //previously called via an onClick
            poll_loop = setInterval(function() {
                display_output("#statusbox", 'getoutput.php');
            }, 2000);
        },
        error: function() {
            console.log('Qa-run failed.');
        }
    });
});
```

That $.ajax(...) call is our jQuery code that initiates the Request A ajax call and defines anonymous functions to call based on the HTTP status code of Request A. If Request A returns an HTTP 200 status code from the server, the anonymous function defined for the ‘success:’ key will be executed. If any other HTTP code is returned, the anonymous function defined for the (optional) ‘error:’ key is executed. We refactored the onClick’s call to display_output() into the ‘success:’ function above. Now, it only gets called if Request A is successful, which is the only time we’d want it to execute.

The body of the ‘success:’ anonymous function calls setInterval() to create an asynchronous (in that it does not block other javascript execution) javascript loop that calls display_output() every 2 seconds. The setInterval() function returns an “interval ID” that is essentially a reference to that interval. We save that interval ID to the ‘poll_loop’ variable that we intentionally make global (by declaring it with ‘var’ outside any containing block) so we can cancel the interval later.

Here is the display_output() function that makes Request B and gets called every 2 seconds: 

```javascript
function display_output(elementSelector, sourceUrl) {
    $(elementSelector).load(sourceUrl);
    var html = $(elementSelector).html();
    if (html.search("EODEPLOY") > 0) {
        window.clearInterval(poll_loop);
        alert('Deployment Finished.');
    }
    if (html.search("DEPLOY_ERROR") > 0) {
        window.clearInterval(poll_loop);
        alert('Deployment FAILED.');
    }
}
```

That [.load() method](https://api.jquery.com/load/) is jQuery shorthand for making an ajax GET request and assigning the returned HTML/text into the element object on which it’s called. Because the display_output() function is responsible for terminating the interval that calls it, we need to define our end cases. If either “EODEPLOY” (for a successful deployment) or “DEPLOY_ERROR” (for a partially failed deployment) appear as strings within the resulting HTML, we call clearInterval() to stop the infinite loop, and alert the user accordingly. If neither of our end cases are encountered, display_output() will be executed again in 2 seconds.

As it stands, the poll_loop interval will run indefinitely if the server-side code somehow fails to ever return the two strings we’re looking for. I left that end case as an exercise up to Rod, but suggested he add a global variable that could be used to measure the number of display_output() calls or the elapsed time since the Deploy button was clicked, and end the loop once an upper limit was hit.

Other suggested features that Rod and I discussed but I’ve omitted from this article include: 

1. Client-side input validation using javascript regular expressions

1. Matching server-side input validation because sometimes the call is coming from inside the house

1. Adding a unique identifier that is passed as part of both Request A and Request B to better identify requests and to prevent temp file naming conflicts from multiple concurrent users.

1. Packaging display_output()’s “Deployment FAILED” output and providing a button to easily send the output to Rod’s team 

I’m sure there are a ton of other possible solutions for a project like this. For example, I know that Jon and Sonny developed a more advanced polling solution for another client, [www.locateexpress.com](https://web.archive.org/web/20110902084453/http://www.locateexpress.com/locate.html), using [YUI’s AsyncQueue](https://yuilibrary.com/yui/docs/async-queue/). Without getting to deeply into the server-side design, I’m curious to hear how other people might approach this problem. What do you think?


