---
author: Mark Johnson
gh_issue_number: 535
tags: database, interchange, optimization, performance, scalability, search, seo
title: Interchange Search Caching with “Permanent More”
---

Most sites that use Interchange take advantage of Interchange’s “more lists”. These are built-in tools that support an Interchange “search” (either the search/scan action, or result of direct SQL via [query]) to make it very easy to paginate results. Under the hood, the more list is a drill-in to a cached “search object”, so each page brings back a slice from the cache of the original search. There are extensive ways to modify the look and behavior of more lists and, with a bit of effort, they can be configured to meet design requirements.

Where more lists tend to fall short, however, is with respect to SEO. There are two primary SEO deficiencies that get business stakeholders’ attention:

- There is little control over the construction of the URLs for more lists. They leverage the scan actionmap and contain a hash key for the search object and numeric data to identify the slice and page location. They possess no intrinsic value in identifying the content they reference.
- The search cache by default is ephemeral and session-specific. This means all those results beyond page 1 the search engine has cataloged will result in dead links for search users who try to land directly on the more-listed pages.

It is the latter issue that I wish to address because there is—​and has been for some time now—​a simple mechanism called “permanent more” to remedy the default behavior.

You can leverage “permanent more” by adding the boolean **mv_more_permanent**, or the shorthand **pm**, to your search conditions. E.g.:

```nohighlight
Link:

    <a href="[area search="
        co=1
        sf=category
        se=Foo
        op=rm
        more=1
        ml=5
        <b>pm=1</b>
    "]">All Foos</a>

Loop:

    [loop search="
        co=1
        sf=category
        se=Foo
        op=rm
        more=1
        ml=5
        <b>pm=1</b>
    "]
    ...loop body with [more-list]...
    [/loop]

Query:

    [query
        list=1
        more=1
        ml=10
        <b>pm=1</b>
        sql="SELECT * FROM products WHERE category LIKE '%Foo%'"
    ]
    ...same as loop but with 10 matches/page...
    [/query]
```

 If the initial search is defined with the “permanent more” setting, it will produce the following adjustments:

- The hash key used to store and identify the search cache is deterministic based on the search conditions. Many searches for Interchange are category driven. Thus, all end users who wish to browse a category end up clicking identical links, which create duplicate search caches, belonging uniquely to them. With permanent more, they all share the same cache, with the same identifier. As long as the search conditions don’t change, neither does the cache identifier. Even as the cache is refreshed with new executions of the search, the object remains in the same location. Thus, the results a search engine produced this morning reference links still valid now, tomorrow, or next week, provided they reference the same search conditions.
- The cached search object has no session affinity. Any link referencing the cache with the correct hash key has access to the content.

Taken together, “permanent more” removes (for the most part, addressed later) dead links from more lists cataloged by search engines. There are, however, other benefits to “permanent more” beyond those intended as described above:

- As stated in passing, standard Interchange search caching produces duplicate search objects for common search conditions. For a busy site, these caches can have an impact on storage. Typically, maintenance is implemented to clean up cache files for all such files whose age exceeds by some amount the session duration (standard is 48 hours). With permanent more, duplicate caches are eliminated. A cache location is reused by all users with the same search requirements, keeping data-storage requirements for caches to the minimum necessary. As searches change, ophaned caches can still easily be cleaned up as they will immediately start to age with no more access to them necessary for storage.
- For the same reason that “permanent more” resolves search-engine links, it also resolves content management for individual sites using a reverse proxy for caching. Because most (and certainly the easiest) caching keys are based off of URL, the deterministic nature of the hash keys for “permanent more” allows assurance that the cached content in the proxy accurately reflects the search content over time, and that all users will hit the cached resource and not generate new, unique links with varying hash keys.

One shortcoming of “permanent more” to be aware of is the impact of changing data underneath the search. Even if search conditions do not change, the count and order of matching record sets may. So, e.g., enough products may be removed from a given category to cause the last page of a more list to become empty, which would cause any specific link into that page to become dead. More minor, but still a possibility, is the introduction or removal of products so that a particularly searched-for term has been “bumped” to another page within the search cache since the last time the search engine crawled the more lists. For searches backed by particularly volatile data, “permanent more” may not be sufficient to address search-engine or caching demands.

Finally, “permanent more” should be avoided for any search features that may cache data sensitive to an individual user. This is unlikely to happen as, under most circumstances, the configuration of the search itself will change based on the unique characteristics of the user executing the search (e.g., a username included in a query to review order history). However, it is still possible that context-sensitive information could be stored in the search object and, if so, all other users with access to the more lists would have access to that information.
