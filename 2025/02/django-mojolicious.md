---
author: "Marco Pessotto"
date: 2025-02-06
title: "Django and Mojolicious: a quick comparison of two popular web frameworks"
github_issue_number: 2089
featured:
  image_url: /blog/2025/02/django-mojolicious/architecture-structure-wood-building-beam-construction-1063818-pxhere.webp
description: A comparison of two mature web frameworks with similar functionality but different languages and implementation.
tags:
- perl
- python
- django
- mojolicious
- catalyst
---

![A view upward toward the wooden framing of a house under construction against a blue sky.](/blog/2025/02/django-mojolicious/architecture-structure-wood-building-beam-construction-1063818-pxhere.webp)

<!-- Photo https://pxhere.com/en/photo/1063818 CC0 Public Domain -->

Recently I've been working on a project with a [Vue](https://vuejs.org/) front-end and two back-ends, one in Python using the [Django](https://www.djangoproject.com/) framework and one in Perl using the [Mojolicious](https://www.mojolicious.org/) framework. So, it's a good time to spend some words to share the experience and do a quick comparison.

[Previously](/blog/2022/04/perl-web-frameworks/) I wrote a post about Perl web frameworks, and now I'm expanding the subject into another language.

Django was chosen for this project because it's been around for almost 20 years now and provides the needed maturity and stability to be long-running and low-budget. In this regard, it has proved a good choice so far. Recently it saw a major version upgrade without any problems to speak of. It could be argued that I should have used the [Django REST Framework](https://github.com/encode/django-rest-framework) instead of plain Django. However, at the time the decision was made, adding a framework on top of another seemed a bit excessive. I don't have many regrets about this, though.

Mojolicious is an old acquaintance. It used to have fast-paced development but seems very mature now, and it's even been [ported](https://mojojs.org/) to JavaScript.

Both frameworks have just a few dependencies (which is fairly normal in the Python world, but not in the Perl one) and excellent documentation. They both follow the model-view-controller pattern. Let's examine the components.

### Views

Both frameworks come with a built-in template system (which can be swapped out with something else), but in this project we can skip the topic altogether as both frameworks are used only as back-end for transmitting JSON, without any HTML rendering involved.

However, let's see how the rendering looks for the API we're writing.

```perl
use Mojo::Base 'Mojolicious::Controller', -signatures;
sub check ($self) {
    $self->render(json => { status => 'OK' });
}
```

```python
from django.http import JsonResponse
def status(request):
    return JsonResponse({ "status":  "OK" })
```

Nothing complicated here, just provide the right call.

### Models

#### Django

Usually a model in context of web development means a database and here we are going to keep this assumption.

Django comes with a comprehensive [object-relational mapping](https://docs.djangoproject.com/en/5.1/topics/db/queries/) (ORM) system and it feels like the natural thing to use. I don't think it makes much sense to use another ORM, or even to use raw SQL queries (though it is [possible](https://docs.djangoproject.com/en/5.1/topics/db/sql/)).

You usually start a Django project by defining the model. The Django ORM gives you the tools to manage the migrations, providing abstraction from the SQL. You need to define the field types and the relationships (joins and foreign keys) using the appropriate class methods.

For example:

```python
from django.db import models
class User(AbstractUser):
    email = models.EmailField(null=False, blank=False)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="site_users")
    libraries = models.ManyToManyField(Library, related_name="affiliated_users")
    expiration = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
```

These calls provide not only the SQL type to use, but also the validation. For example, the `blank` parameter is a validation option specifying whether Django will accept an empty value. It is different from the `null` option, which directly correlates to SQL. You can see we're quite far from working with SQL, at least two layers of abstraction away.

In the example above, we're also defining a foreign key between a site and a user (many-to-one), so each user belongs to one site. We also define a many-to-many relationship with the libraries record. I like how these relationships are defined, it's very concise.

Thanks to these definitions, you get a whole [admin console](https://docs.djangoproject.com/en/5.1/ref/contrib/admin/) almost for free, which your admin users are sure to like. However, I'm not sure this is a silver bullet for solving all problems. With large tables and relationships the admin pages load slowly and they could become unusable very quickly. Of course, you can tune that by filtering out what you need and what you don't, but that means things are not as simple as "an admin dashboard for free" — at the very least, there's some configuring to do.

As for the query syntax, you usually need to call `Class.objects.filter()`. As you would expect from an ORM, you can chain the calls and finally get objects out of that, representing a database row, which, in turn, you can update or delete.

The syntax for the `filter()` call is based on the double underscore separator, so you can query over the relationships like this:

```python
for agent in (Agent.objects.filter(canonical_agent_id__isnull=False)
              .prefetch_related('canonical_agent')
              .order_by('canonical_agent__name', 'name')
              .all()):
    agent.name = "Dummy"
    agent.save()
```

In this case, provided that we defined the foreign keys and the attributes in the model, we can search/​order across the relationship. The `__isnull` suffix, as you can imagine, results in a `WHERE canonical_agent_id IS NOT NULL` query, while in the `order_by` call we sort over the joined table using the `name` column. Looks nice and readable, with a touch of magic.

Of course things are never so simple, so you can build complex queries with the `Q` class combined with bytewise operators (`&`, `|`).

Here's an example of a simple case-insensitive search for a name containing multiple words:

```python
from django.db.models import Q

def api_list(request)
    term = request.GET.get('search')
    if term
        words = [ w for w in re.split(r'\W+', term) if w ]
        if words:
            query = Q(name__icontains=words.pop())
            while words:
                query = query & Q(name__icontains=words.pop())
            # logger.debug(query)
            agents = Agent.objects.filter(query).all()
```

To sum up, the ORM is providing everything you need to stay away from the SQL. In fact, it seems like Django doesn't like you doing raw SQL queries.

#### Mojolicious and Perl

In the Perl world things are a bit different.

The Mojolicious [tutorial](https://docs.mojolicious.org/Mojolicious/Guides/Tutorial) doesn't even mention the database. You can use any ORM or no ORM at all, if you prefer so. However, Mojolicious makes the DB handle available everywhere in the application.

You could use [DBIx::Connector](https://metacpan.org/pod/DBIx::Connector), [DBIx::Class](https://metacpan.org/pod/DBIx::Class), [Mojo::Pg](https://docs.mojolicious.org/Mojo/Pg) (which was developed with Mojolicious), or whatever you prefer.

For example, to use Mojo::Pg in the main application class:

```perl
package MyApp;
use Mojo::Base 'Mojolicious', -signatures;
use Mojo::Pg;
use Data::Dumper::Concise;

sub startup ($self) {
    my $config = $self->plugin('NotYAMLConfig');
    $self->log->info("Starting up with " . Dumper($config));
    $self->helper(pg => sub {
                      state $pg = Mojo::Pg->new($config->{dbi_connection_string});
                  });
```

In the routes you can call `$self->pg` to get the database object.

The three approaches I've mentioned here are different.

`DBIx::Connector` is basically a way to get you a safe DBI handle across forks and DB connection failures.

`Mojo::Pg` gives you the ability to do abstract queries but also gives some convenient methods to get the results. I wouldn't call it a ORM; from a query you usually gets hashes, not objects, you don't need to define the database layout, and it won't produce migrations for you, though there is some [migration support](https://docs.mojolicious.org/Mojo/Pg/Migrations).

Here's an example of standard and abstract queries:

```perl
sub list_texts ($self) {
    if (my $sid = $self->param('sid')) {
        my $sql = 'SELECT * FROM texts WHERE sid = ? ORDER BY sorting_index';
        @all = $self->pg->db->query($sql, $sid)->hashes->each;
    }
    $self->render(json => { texts => \@all });
```

The query above can be rewritten with an abstract query, using the same module.

```perl
@all = $self->pg->db->select(texts => undef,
                             { sid => $sid },
                             { order_by => 'sorting_index' })->hashes->each;
```

If it's a simple, static query, it's basically a matter of taste; do you prefer to see the SQL or not? The second version is usually nicer if you want to build a different query depending on the parameters, so you add or remove keys to the hashes which maps to query and finally execute it.

Now, speaking of taste, for complex queries with a lot of joins I honestly prefer to see the SQL query instead of wondering if the abstract one is producing the correct SQL. This is true regardless of the framework. I have the impression that it is faster, safer, and cleaner to have the explicit SQL in the code rather than leaving future developers (including future me) to wonder if the magic is happening or not.

Finally, nothing stops you from using `DBIx::Class`, which is the best ORM for Perl, even if it's not exactly light on dependencies.

It's very versatile, it can build queries of arbitrary complexity, and you usually get objects out of the queries you make. It doesn't come with an admin dashboard, it doesn't enforce the data types and it doesn't ship any validation by default (of course, you can implement that manually). The query syntax is very close to the `Mojo::Pg` one (which is basically [SQL::Abstract](https://metacpan.org/pod/SQL::Abstract)).

The gain here is that, like in Django's ORM, you can attach your methods to the classes representing the rows, so the data definitions live with the code operating on them.

However, the fact that it builds an object for each result means you're paying a performance penalty which sometimes can be very high. I think this is a problem common to all ORMs, regardless of the language and framework you're using.

The difference with Django is that once you have chosen it as your framework, you are basically already sold to the ORM. With Mojolicious and other Perl frameworks (Catalyst, Dancer), you can still make the decision and, at least in theory, change it down the road.

My recommendation would be to keep the model, both code and business logic, decoupled from the web-specific code. This is not really doable with Django, but is fully doable with the Perl frameworks. Just put the DB configuration in a dedicated file and the business code in appropriate classes. Then you should be able to, for example, run a script without loading the web and the whole framework configuration. In this ideal scenario, the web framework just provides the glue between the user and your model.

### Controllers

Routes are defined similarly between Django and Mojolicious. Usually you put the code in a class and then point to it, attaching a name to it so you can reference it elsewhere. The language is different, the style is different, but they essentially do the same thing.

Django:

```python
from django.urls import path
from . import views
urlpatterns = [
    path("api/agents/<int:agent_id>", views.api_agent_view, name="api_agent_view"),
]
```

The function `views.api_agent_view` will receive the request with the `agent_id` as a parameter.

Mojolicious:

```perl
sub startup ($self) {
    # ....
    my $r = $self->routes;
    $r->get('/list/:sid')->to('API#list_texts')->name('api_list_texts');
}
```

The `->to` method is routing the request to the `Myapp::Controller::API::list_texts`, which will receive the request with the `sid` as parameter.

This is pretty much the core business of every web framework: routing a request to a given function.

Mojolicious has also the ability to [chain the routes](https://docs.mojolicious.org/Mojolicious/Guides/Routing#Under) (pretty much taken from Catalyst). The typical use is authorization:

```perl
sub startup ($self) {
    ...
    my $r = $self->routes;
    my $api = $r->under('/api/v1', sub ($c) {
        if ($c->req->headers->header('X-API-Key') eq 'testkey') {
            return 1;
        }
        $c->render(text => 'Authentication required!', status => 401);
        return undef;
    }
    $api->get('/check')->to('API#check')->name('api_check');
```

So the request to `/api/v1/check` will first go in the first block and the chain will abort if the API key is not set in the header. Otherwise it will proceed to run the `API` module's `check` function.

### Conclusion

I'm Perl guy and so I'm a bit biased toward Mojolicious, but I also have a pragmatic approach to programming. Python is widely used — they teach it in schools — while Perl is seen as old-school, if not dead (like all the mature technologies). So, Python could potentially attract more developers to your project, and this is important to consider.

Learning a new language like Python is not a big leap; it and Perl are quite similar despite the different syntax. I'd throw Ruby in the same basket.

Of course both languages provide high quality modules you can use, and these two frameworks are an excellent example.
