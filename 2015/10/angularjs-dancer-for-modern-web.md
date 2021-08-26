---
author: Josh Lavin
title: AngularJS & Dancer for Modern Web Development
github_issue_number: 1169
tags:
- angular
- dancer
- javascript
- perl
date: 2015-10-30
---

At the [Perl Dancer Conference 2015](http://perl.dance), I gave a talk on *[AngularJS & Dancer for Modern Web Development](https://www.perl.dance/talks/11-angularjs-%26-dancer-for-modern-web-development)*. This is a write-up of the talk in blog post form.

### Legacy Apps

It’s a fact of life as a software developer that a lot of us have to work with legacy software. There are many older platforms out there, still being actively used today, and still supporting valid businesses. Thus, legacy apps are unavoidable for many developers. Eventually, older apps are migrated to new platforms. Or they die a slow death. Or else the last developer maintaining the app dies.

### Oh, to migrate

It would be wonderful if I could migrate every legacy app I work on to something like [Perl Dancer](http://perldancer.org/). This isn’t always practical, but a developer can dream, right?

Of course, every circumstance is different. At the very least, it is helpful to consider ways that old apps can be migrated. Using new technologies can speed development, give you new features, and breathe new life into a project, often attracting new developers.

As I considered how to prepare my app for migration, here are a few things I came up with:

- Break out of the Legacy App Paradigm
    - Consider that there are better ways to do things than the way they’ve always been done
- Use Modern Perl
    - Use [object-oriented Perl](http://www.modernperlbooks.com/books/modern_perl_2014/07-object-oriented-perl.html)
    - Use [tests](https://metacpan.org/pod/Test::Stream)
    - Use [CPAN](https://metacpan.org/) modules and don’t reinvent the wheel
- Organize business logic
    - Try to avoid placing logic in front-end code

### You are in a legacy codebase

I explored how to start using testing, but I soon realized that this requires methods or subroutines. This was the sad realization that up till now, my life as a Perl programmer had been spent doing scripting. My code wasn’t testable, and looked like a relic with business logic strewn about.

### Change

I set out to change my ways. I started exploring [object-oriented Perl](http://perldoc.perl.org/perlootut.html) using [Moo](https://metacpan.org/pod/Moo), since Dancer2 uses Moo. I started trying to write unit tests, and started to use classes and methods in my code.

Essentially, I began breaking down problems into smaller problems. This, after all, is how the best methods are written: short and simple, that do [just one thing](https://en.wikipedia.org/wiki/Single_responsibility_principle). I found that writing code this way was fun.

### Crash

I quickly realized that I wasn’t able to run tests in my Legacy App, as it couldn’t be called from the command line (at least not out of the box, and not without weird hacks). Thus, if my modules depended on Legacy App code, I wouldn’t be able to call them from tests, because I couldn’t run these tests from the shell.

This led me to a further refinement: *abstract away all Legacy App-specific code from my modules*. Or, at least all the modules I could (I would still need a few modules to rely on the Legacy App, or else I wouldn’t be using it it all). This was a good idea, it turned out, as it follows the principle of [Separation of Concerns](https://en.wikipedia.org/wiki/Separation_of_concerns), and the idea of *Web App + App*, which was mentioned frequently at the conference.

*Now* I was able to run tests on my modules!

### Move already

This whole process of “getting ready to migrate” soon began to look like [yak shaving](http://catb.org/jargon/html/Y/yak-shaving.html). I realized that I should have moved to Dancer earlier, instead of trying to do weird hacks to get the Legacy App doing things as Dancer would do them.

However, it was a start, a step in the right direction. Lesson for me, tip for you.

*And*, the result was that my back-end code was all the more ready for working with Dancer. I would just need to change a few things, and presto! (More on this below.)

### Front-End

With the back-end looking tidier, I now turned to focus on the front-end. There was a lot of business logic in my front-end code that needed to be cleaned up.

Here is an example of my Legacy App front-end code:

```html
@_TOP_@
<h1>[scratch page_title]</h1>
[perl]
   my $has_course;
   for (grep {$_->{mv_ib} eq 'course'} @$Items) {
      $has_course++;
   }
   return $has_course ? '<p>You have a course!</p>' : '';
[/perl]
<button>Buy [if cgi items]more[else]now[/else][/if]</button>
@_BOTTOM_@
```

As you can see, the Legacy App allowed the embedding of all sorts of code into the HTML page. I had Legacy App tags (in the brackets), plus something called “embedded perl”, plus regular HTML. Add all this together and you get *Tag Soup*.

This kind of structure won’t look nice if you attempt to view it on your own machine in a web browser, absent from the Legacy App interpreting it. But let’s face it, this code doesn’t look nice anywhere.

### Separation of Concerns

I thought about how to apply the principle of *Separation of Concerns* to my front-end code. One thing I landed on, which isn’t a new idea by any means, is the use of “HTML + placeholders”, whereby I would use some placeholders in my HTML, to be later replaced and filled in with data. Here is my first attempt at that:

```html
@_TOP_@
[my-tag-attr-list
    page_title="[scratch page_title]"
    has_course="[perl] ... [/perl]"
    buy_phrase="Buy [if cgi items]more[else]now[/else][/if]"
]

    <h1>{PAGE_TITLE}</h1>
    {HAS_COURSE?}<p>You have a course!</p>{/HAS_COURSE?}
    <button>{BUY_PHRASE}</button>

[/my-tag-attr-list]
@_BOTTOM_@
```

What I have here uses the Legacy App’s built-in placeholder system. It attempts to set up all the code in the initial “my-tag-attr-list”, then the HTML uses placeholders (in braces) which get replaced upon the page being rendered. (The question-mark in the one placeholder is a conditional.)

This worked OK. However, the logic was *still* baked into the HTML page. I wondered how I could be more ready for Dancer? (Again, I should have just gone ahead and migrated.) I considered using [Template::Toolkit](http://p3rl.org/Template::Toolkit), since it is used in Dancer, but it would be hard to add to my Legacy App.

### Enter AngularJS (or your favorite JavaScript framework)

[AngularJS](http://angularjs.org/) is a JavaScript framework for front-end code. It displays data on your page, which it receives from your back-end via [JSON](http://json.org/) feeds. This effectively allows you to separate your front-end from your back-end. It’s almost as if your front-end is consuming an API. (Novel idea!)

After implementing AngularJS, my Legacy App page looked like this (not showing JavaScript):

```html
@_TOP_@
<h1 ng-bind="page.title"></h1>
<p ng-if="items.course">You have a course!</p>
<button ng-show="items">Buy more</button>
<button ng-hide="items">Buy now</button>
@_BOTTOM_@
```

Now all my Legacy App is doing for the front-end is basically “includes” to get the header/footer (the TOP and BOTTOM tags). The rest is HTML code with ng- attributes. These are what AngularJS uses to “do” things.

This is much cleaner than before. I am still using the Legacy App back-end, but all it has to do is “routing” to call the right module and deliver JSON (and do authentication).

Here’s a quick example of how the JavaScript might look:

```html
<html ng-app="MyApp">
...
<script src="angular.min.js"></script>
<script>
  angular.module / factory / controller
  $scope.items = ...;
</script>
</html>
```

This is very simplified, but via its modules/factories/controllers, the AngularJS code handles how the JSON feeds are displayed in the page. It pulls in the JSON and can massage it for use by the ng- attributes, etc.

I don’t have to use AngularJS to do this—​I could use a Template::Toolkit template delivered by Dancer, or any number of other templating systems. However, I like this method, because it doesn’t require a Perl developer to use. Rather, any competent JavaScript developer can take this and run with it.

### Migration

Now the migration of my entire app to Dancer is much easier. I gave it a whirl with a handful of routes and modules, to test the waters. It went great.

For my modules that were the “App” (not the “Web App” and dependent on the Legacy App), very few changes were necessary. Here is an example of my original module:

```perl
package MyApp::Feedback;
use MyApp;
my $app = MyApp->new( ... );
sub list {
    my $self = shift;
    my $code = shift
        or return $app->die('Need code');
    my $rows = $app->dbh($feedback_table)->...;
    return $rows;
}
```

You’ll see that I am using a class called MyApp. I did this to get a custom die and a database handle. This isn’t really the proper way to do this (I’m learning), but it worked at the time.

Now, after converting that module for use with Dancer:

```perl
package MyApp::Feedback;
use Moo;
with MyApp::HasDatabase;
sub list {
    my $self = shift;
    my $code = shift
        or die 'Need code';
    my $rows = $self->dbh->...;
    return $rows;
}
```

My custom die has been replaced with a Perl die. Also, I am now using a [Moo::Role](https://metacpan.org/pod/Moo::Role) for my database handle. And that’s all I changed!

#### Before

The biggest improvements were in things that I “stole” from Dancer. (Naturally, Dancer would do things better than I.) This is my Legacy App’s route for displaying and accepting feedback entries. It does not show any authentication checks. It handles feeding back an array of entries for an item (“list”), a single entry (GET), and saving an entry (POST):

```perl
sub _route_feedback {
    my $self = shift;
    my (undef, $sub_action, $code) = split '/', $self->route;
    $code ||= $sub_action;
    $self->_set_status('400 Bad Request');   # start with 400
    my $feedback = MyApp::Feedback->new;
    for ($sub_action) {
        when ("list") {
            my $feedbacks = $feedback->list($code);
            $self->_set_tmp( to_json($feedbacks) );
            $self->_set_path('special/json');
            $self->_set_content_type('application/json; charset=UTF-8');
            $self->_set_status('200 OK') if $feedbacks;
        }
        default {
            for ($self->method) {
                when ('GET') {
                    my $row = $feedback->get($code)
                        or return $self->_route_error;
                    $self->_set_tmp( to_json($row) );
                    $self->_set_path('special/json');
                    $self->_set_content_type('application/json; charset=UTF-8');
                    $self->_set_status('200 OK') if $row;
                }
                when ('POST') {
                    my $params = $self->body_parameters
                        or return $self->_route_error;
                    $params = from_json($params);
                    my $result = $feedback->save($params);
                    $self->_set_status('200 OK') if $result;
                    $self->_set_path('special/json');
                    $self->_set_content_type('application/json; charset=UTF-8');
                }
            }
        }
    }
}
```

#### After

Here are those same routes in Dancer:

```perl
prefix '/feedback' => sub {
    my $feedback = MyApp::Feedback->new;
    get '/list/:id' => sub {
        return $feedback->list( param 'id' );
    };
    get '/:code' => sub {
        return $feedback->get( param 'code' );
    };
    post '' => sub {
        return $feedback->save( scalar params );
    };
};
```

Dancer gives me a lot for free. It is a *lot* simpler. There’s still no authentication shown here, but everything else is done. (And I can use an [authentication plugin](http://p3rl.org/Dancer2::Plugin::Auth::Extensible) to make even that easy.)

### TMTOWTDI

For the front-end, we have options on how to use Dancer. We could have Dancer deliver the HTML files that contain AngularJS. Or, we could have the web server deliver them, as there is nothing special about them that says Dancer must deliver them. In fact, this is especially easy if our AngularJS code is a [Single Page App](https://en.wikipedia.org/wiki/Single-page_application), which is a single static HTML file with AngularJS “routes”. If we did this, and needed to handle authentication, we could look at using [JSON Web Tokens](http://jwt.io/).

### Now starring Dancer

In hindsight, I probably should have moved to Dancer right away. The Legacy App was a pain to work with, as I built my own Routing module for it, and I also built my own Auth checking module. Dancer makes all this simpler.

In the process, though, I learned something...

### Dancer is better?

*I learned you can use tools improperly*. You can do Dancer “wrong”. You can write tag soup in anything, even the best modern tools.

You can stuff all your business logic into Template::Toolkit tags. You can stuff logic into Dancer routes. You can do AngularJS “wrong” (I probably do).

### Dancer is better:

Dancer is better when (thanks to [Matt S Trout](https://twitter.com/shadowcat_mst) for these):

- **Routes contain code specific to the Web.**
- **Routes call non-Dancer modules** (where business logic lives; again, *Web App + App*).
- **The route returns the data in the appropriate format.**

These make it easy to test. You are effectively talking to your back-end code as if it’s an API. *Because it is.*

The point is: start improving somewhere. Maybe you cannot write tests in everything, but you can try to write smart code.

### Lessons learned

- Separate concerns
- Keep it testable
- Just start somewhere

The end. Or maybe the beginning...
