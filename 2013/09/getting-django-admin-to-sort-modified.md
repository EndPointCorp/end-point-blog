---
author: Phin Jensen
title: Getting the Django Admin to sort modified columns
github_issue_number: 860
tags:
- django
- python
date: 2013-09-28
---

A lot of what I’ve worked on at End Point is Ovis, a program to keep track of information about our servers. This information includes current operating system, data center, which client owns or uses it, etc. Ovis is built entirely on the Django Admin, with the most important information displayed on the Servers list page.

A very important part of it is tracking server updates.

Knowing when and by who a server was last updated is nice to see, but to put it to good use, we needed to have a column that would show when it was last updated and who last updated it. We also wanted this column to have links to the relevant pages.

Django has a handy way of using functions to create a column based on data that is not part of the model being listed. The documentation for that is [here.](https://docs.djangoproject.com/en/2.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display) This is the code we are using:

```python
def latest_update(self):
    try:
        object = self.update_set.latest()
        if object:
            return "<a href="%s">%s</a> by <a href="%s">%s</a>" % (
                '/admin/ovisapp/update/%s' % object.id,
                object.when_updated.date(),
                '/admin/auth/user/%s' % object.updated_by.id,
                "%s %s." % (object.updated_by.first_name, object.updated_by.last_name[0])
            )
    except:
        return ""
```

It ends up looking like this:

<a href="/blog/2013/09/getting-django-admin-to-sort-modified/image-0.png" imageanchor="1"><img border="0" src="/blog/2013/09/getting-django-admin-to-sort-modified/image-0.png"/></a>

While this is very useful, it has one very big problem. You are unable to sort your list of objects by this new column. This is because with other columns, it sorts with an easy ORDER BY in the database. But when you are grabbing data from another table, adding links and extra space, words, etc., Django doesn’t know what to sort by.

The main part of the sorting is creating a custom Manager to your model, and [annotating](https://docs.djangoproject.com/en/2.0/ref/models/querysets/#annotate) the QuerySet with [aggregate functions](https://docs.djangoproject.com/en/2.0/ref/models/querysets/#aggregation-functions). Like this, which gets the newest update object for each server object:

```python
class ServerManager(Manager):
    def get_query_set(self):
        qs = super(ServerManager, self).get_query_set().annotate(Max('update__when_updated'))
        return qs
```

Set it as your model’s manager by adding this line to the model definition:

```python
objects = ServerManager()
```

Now, to get the column to sort by the aggregate function, set the *admin_order_field* method attribute to point to your new annotated aggregate function, like this:

```python
def latest_update(self):
...
latest_update.admin_order_field = 'update__when_updated__max'
```

And it will sort by the date!

<a href="/blog/2013/09/getting-django-admin-to-sort-modified/image-1.png" imageanchor="1"><img border="0" src="/blog/2013/09/getting-django-admin-to-sort-modified/image-1.png"/></a>


