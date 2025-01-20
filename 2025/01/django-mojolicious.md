---
author: "Marco Pessotto"
date: 2025-01-20
title: "Django and Mojolicious: a quick comparison of two popular web frameworks"
tags:
 - perl
 - python
 - web
 - mojolicious
 - catalyst
 - mvc
 - django
 - orm
 - dbic
---

![Building Frames](/blog/2025/01/architecture-structure-wood-building-beam-construction-1063818-pxhere.webp)

<!-- Photo https://pxhere.com/en/photo/1063818 CC0 Public Domain -->



### Django and Mojolicious

Recently I've been working on a project with a
[Vue](https://vuejs.org/) front-end and two back-ends, one in Python
using the [Django](https://www.djangoproject.com/) framework and one
in Perl using the [Mojolicious](https://www.mojolicious.org/)
framework, so it's probably a good time to spend some words to share
the experience and do a quick comparison.

[Previously](/blog/2022/04/perl-web-frameworks/) I wrote a post about
Perl web frameworks, now I'm expanding the subject crossing into
another language.

Django was chosen because it's been around for almost 20 years now and
provides the needed maturity and stability for a project which aims to
be long-running and low-budget. On this regard, so far it proved a
good choice. Recently it saw a major version upgrade without any
problem at all. It could be argued that I should have used the [Django
REST Framework](https://github.com/encode/django-rest-framework)
instead of plain Django. However, at the time the decision was made,
it seemed that adding a framework on the top of another was a bit
excessive. I don't have many regrets about this though.

Mojolicious is an old acquaintance, it used to have a fast-paced
development but seems very mature now, and it's even ported to
[JavaScript](https://mojojs.org/).

Both frameworks have just a few dependencies (which could be something
normal in the Python world, but it's not in the Perl one) and
excellent documentation.

They both follow the Model-Controller-View pattern, so let's examine
the components.

### Views

Both frameworks come with a built-in template system (which can be
swapped out with something else), but in this case we can skip the
topic altogether as both are used only as back-end talking JSON,
without any HTML rendering involved. 

https://docs.djangoproject.com/en/5.1/topics/templates/
https://docs.mojolicious.org/Mojo/Template

However, given that we're writing API, let's see how the rendering looks.

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

Nothing complicate here, just provide the right call.

### Models

#### Django

Usually a model in the web development context means a database and
here we are going to keep this assumption.

Django comes with a comprehensive [Object-relational mapping
system](https://docs.djangoproject.com/en/5.1/topics/db/queries/) and
it feels like the natural thing to use. I don't think it makes much
sense to use another ORM with it or even using raw SQL query (even if
it's [possible](https://docs.djangoproject.com/en/5.1/topics/db/sql/)).

So usually you start a Django project defining the model. The Django
ORM gives you the tools to manage the migrations abstracting away from
the SQL. You need to define the field types and the relationships
(joins and foreign keys) using the appropriate class methods.

E.g.

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

These calls provide not only the SQL type to use, but also the
validation, so we're, so to speak, quite far from the SQL, at least
two abstraction layers away. For example the `blank` parameter is a
validation thing.

In the example above, we're also defining a foreign key to a site
(many-to-one), so each user needs to belong to one, and a many-to-many
relationship with the libraries record. I like how these relationships
are defined, it's very concise.

Thanks to this, you get, almost for free, a whole [admin
console](https://docs.djangoproject.com/en/5.1/ref/contrib/admin/),
which for sure your admin user are going to like. However, I'm not
sure this is a silver bullet solving all problems. With large tables
and relationships the admin pages load slowly and they could become
unusable very quickly. Of course you can tune that, filter out what
you need and what you don't. I'm just saying that things are not as
simple as "an admin dashboard for free". There's at very least some
configuration to do.

As for the query syntax, you usually need to call
`Class.objects.filter()`. As you would expect from an ORM you can
chain the calls and finally get objects out of that, representing a
database row, which in turn you can update or delete.

The syntax for the `filter()` call is based on the double underscore
separator, so you can query over the relationships with things like this:

```python
for agent in (Agent.objects.filter(canonical_agent_id__isnull=False)
              .prefetch_related('canonical_agent')
              .order_by('canonical_agent__name', 'name')
              .all()):
    agent.name = "Dummy"
    agent.save()
```

In this case, provided that we defined the foreign keys and the
attributes in the model, we can search/order across the relationship.
The `__isnull` suffix, as you can imagine, results in a
`WHERE canonical_agent_id IS NOT NULL` query, while in the `order_by` call
we are sorting over the joined table using the `name` column. Looks
nice and readable, with a touch of magic.

Of course things are never so simple, so you can build complex query
with the `Q` class combining them with bytewise operators (`&`, `|`).

Example of a simple case-insensitive search for a name containing
multiple words:

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

To sum up, the ORM is providing everything you need to stay away from
the SQL. Actually, it seems like Django doesn't like you doing raw SQL
queries.

#### Mojolicious and Perl

In the Perl world things are a bit different.

The Mojolicious
[tutorial](https://docs.mojolicious.org/Mojolicious/Guides/Tutorial)
doesn't even mention the database. You can use any ORM or no ORM at
all, if you prefer so. However, Mojo gives you the way to make the DB
handle available everywhere in the application.

You could use, e.g.
[DBIx::Connector](https://metacpan.org/pod/DBIx::Connector),
[DBIx::Class](https://metacpan.org/pod/DBIx::Class) or
[Mojo::Pg](https://docs.mojolicious.org/Mojo/Pg) (which was developed
with Mojolicious) or whatever you prefer.

So for example, in the main application class:

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

And in the routes you can call `$self->pg` and get the database object.

The three approaches I'm mentioning here are different.

The `DBIx::Connector` is basically a way to get you a safe DBI handle
across forks and DB connection failures.

`Mojo::Pg` gives you the ability to do abstract queries but also some
convenience methods to get the results. I wouldn't call it a ORM. From
a query you usually gets hashes, not objects, you don't need to define
the database layout, it won't produce migrations for you, even if there's
some [migration support](https://docs.mojolicious.org/Mojo/Pg/Migrations).

Example:

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

If it's a simple, static query, it's basically a matter of taste if
you want to see the SQL or not. The second version is usually nicer if
you want to build a different query depending on the parameters, so
you add or remove keys to the hashes which maps to query and finally
execute it.

Now, speaking about tastes, for complex queries with a lot of joins I
honestly prefer to see the SQL query instead of wondering if the
abstract one is producing the correct SQL. This is true regardless of
the framework. I have sometimes the impression that is faster, safer
and cleaner to have the explicit SQL in the code rather than having
future developers (including future me) wondering if the magic is
happening or not.

Finally, nothing stops you from using `DBIx::Class`, which is the best
ORM for Perl, even if it's not exactly light on dependencies.

It's very versatile, it can build query of arbitrary complexity, you
usually get objects out of the queries you make. It doesn't come with
and admin dashboard, it doesn't enforce the data types and it doesn't
ship any validation by default (of course you can build on that). The
query syntax is very close to the `Mojo::Pg` one (which is basically
[SQL::Abstract](https://metacpan.org/pod/SQL::Abstract)).

The gain here is that, like in Django ORM, you can attach your methods
to the classes representing the rows, so the data definitions live
with the code operating on it.

However, the fact that it builds object for each result, it means
you're paying a performance penalty which sometimes can be very high,
and I think this is the common problem of the ORMs, regardless of the
language and framework you're using.

The difference is that with Django, once you have chosen it as your
framework, you are basically already sold to the ORM. With Mojolicious
and in general with the other Perl frameworks (Catalyst, Dancer), you
still have the decision to make and you can change it, at least in
theory, down the road.

Actually, my recommendation would be to keep the model, both code and
business logic, decoupled from the web-specific code. This is not
really doable with Django, but is fully doable with the Perl
frameworks. Just put the DB configuration in a dedicated file, the
business code in appropriated classes, and you should be able to, just
to make an example, run a script without loading the web and the whole
framework configuration. In this ideal scenario, the web framework
just provides the glue between the user and your model.

### Controllers

The way the routes are defined are pretty much similar. Usually you
put the code in a class and then point to it, attaching a name to it
so you can reference it elsewhere.

Language is different, style is different, but pretty much the same thing:

Django:

```python
from django.urls import path
from . import views
urlpatterns = [
    path("api/agents/<int:agent_id>", views.api_agent_view, name="api_agent_view"),
]
```

The function `views.api_agent_view` will receive the request with the agent_id
as parameter.


Mojolicious:

```perl
sub startup ($self) {
    # ....
    my $r = $self->routes;
    $r->get('/list/:sid')->to('API#list_texts')->name('api_list_texts');
}
```

The `->to` method is routing the request to the
`Myapp::Controller::API::list_texts` will receive the request with the
`sid` as parameter.

This is pretty much the core business of every web framework: routing
a request to a given function.

Mojolicious has also the ability to [chain the
routes](https://docs.mojolicious.org/Mojolicious/Guides/Routing#Under)
(pretty much taken from Catalyst). Typical usage is authorization:

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

So the request to `/api/v1/check` will first go in the first block and
the chain will abort if the API key is not set in the header,
otherwise it will proceed to the dispatch to the `API` module, `check`
function.

### Conclusion

I'm after all a Perl guy and I'm a bit biased, but I also have a
pragmatical approach to programming. Python is widely used, they teach
it in schools, while Perl is seen as old-school, if not dead (like all
the mature technologies), so Python could, potentially, attract more
developers to your project and this is an important thing to consider.

Learning a new language like Python is not a big leap, they are quite
similar despite the different syntax. I'd throw Ruby in the same
basket.

Of course both languages provide high quality modules you can use, and
these two frameworks are an excellent example.
