---
author: Szymon Lipiński
gh_issue_number: 557
tags: django, python
title: Downloading CSV file from Django admin
---

Django has a very nice admin panel. The admin panel is highly extensible and there can be performed really cool enhancements. One of such things is a custom action.

For the purpose of this this article I’ve created a simple Django project with a simple application containing only one model. The file models.py looks like this:

```python
from django.db import models
from django.contrib import admin

class Stat(models.Model):
    code = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    count = models.IntegerField()

class StatAdmin(admin.ModelAdmin):
    list_display = ('code', 'country', 'ip', 'url', 'count')

admin.site.register(Stat, StatAdmin)
```

I’ve also added a couple of rows in the database table for this model. The admin site for this model looks like this:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2012/02/22/dowloading-csv-file-with-from-django/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2012/02/22/dowloading-csv-file-with-from-django/image-0.png" width="600"/></a></div>

Now I want to be able to select some rows and download a CSV file right from the Django admin panel. The file should contain only the information about selected rows.

This can be done really easy with the admin actions mechanism. Over the table with rows there is the actions menu. There is one default action, it is "Delete selected stats". To use the action you need to select the rows, select the action from the combo box and press the OK button.

I will add another action there, which will be named "*Download CSV file for selected stats*".

### Add the action.

First of all I will add the custom action. For this I will enhance the StatAdmin class with the field actions, and add the method, called when someone wants to run this action (all changes from the previous version are highlighted):

```python
class StatAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ('code', 'country', 'ip', 'url', 'count')
    def download_csv(self, request, queryset):
        None
    download_csv.short_description = "Download CSV file for selected stats."
```

In the admin panel for the stats model you can notice that there is the new action. The above code doesn’t do anything useful, so let’s generate the CSV file.

The whole idea is to generate the CSV file, don’t use any disk, do it in memory only and return to the user without any redirection to other page (the file should download automatically after pushing the OK button).

Do it in small steps:

### Generate the CSV

For this I will use the CSV module from Python’s standard library and the function now looks like this:

```python
def download_csv(self, request, queryset):
    import csv
    f = open('some.csv', 'wb')
    writer = csv.writer(f)
    writer.writerow(["code", "country", "ip", "url", "count"])
    for s in queryset:
        writer.writerow([s.code, s.country, s.ip, s.url, s.count])

```

After selecting two rows and running the action, it created a file some.csv in the main project directory with the following content.

```nohighlight
code,country,ip,url,count
B,BB,BBB,BBBB,22
C,CC,CCC,CCCC,33
```
That’s OK, generating the CSV file works, however it shouldn’t be stored on the disk.

Return the file directly into the browser.

I want to send the file to the client right after clicking on the OK button. This is fairly easy, the whole magic is to use proper HTTP headers. I will modify the method to look like this:

```python
def download_csv(self, request, queryset):
    import csv
    from django.http import HttpResponse

    f = open('some.csv', 'wb')
    writer = csv.writer(f)
    writer.writerow(["code", "country", "ip", "url", "count"])

    for s in queryset:
        writer.writerow([s.code, s.country, s.ip, s.url, s.count])

    f.close()

    f = open('some.csv', 'r')
    response = HttpResponse(f, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=stat-info.csv'
    return response
```

So the main changes are: - closed the file and reopen it for reading - added headers for proper content type and file name.

The result is that when someone clicks on the OK button, the browser automatically starts downloading the stat-info.csv file.

**Don’t use disk.**

The only thing left: create the file in memory only. For this I will use StringIO module. It is a nice module implementing exactly the same interface as the file, so I can use it instead the file. StringIO operates only on memory without any disk operations.

```python
def download_csv(self, request, queryset):
    import csv
    from django.http import HttpResponse
    import StringIO

    f = StringIO.StringIO()
    writer = csv.writer(f)
    writer.writerow(["code", "country", "ip", "url", "count"])

    for s in queryset:
        writer.writerow([s.code, s.country, s.ip, s.url, s.count])

    f.seek(0)
    response = HttpResponse(f, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=stat-info.csv'
    return response
```

As you can see the changes are: - added import StringIO - changed opening file to creating new StringIO object - there is no reopening the file, only seek to set the marker at the beginning of the file

Everything is finished now. There is a new action in the admin panel which generates a new CSV file with information about chosen rows and it doesn’t do any browser redirection.
