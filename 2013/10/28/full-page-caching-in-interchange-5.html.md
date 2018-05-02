---
author: Mark Johnson
gh_issue_number: 867
tags: interchange, nginx, performance, perl, scalability
title: Full Page Caching in Interchange 5
---

I recently attended the [eCommerce Innovation Conference 2013](http://www.ecommerce-innovation.com/) with fellow End Pointer [Richard Templet](/team/richard_templet) and presented on the work End Point has done to develop full-page caching in Interchange 5. The work is in final review currently for inclusion into core Interchange and should provide a roadmap for cache management in Nitesi/Interchange 6.

### Parameters of a Caching Solution

In order to identify the full scope of what one means when one says an application uses caching, there are (at least) 3 aspects to define:

- Where in the application stack is the cache being applied.
- How long until the cache is expired.
- What level of user state must it support.

The issue of cache duration is not addressed here as any such formulation will be specific to business requirements and tolerance of stale data. I will state, however, that even very brief cache durations can have an enormous impact on performance, particularly for sites that have a relatively small number of resources that absorb the bulk of the traffic. Cache durations of several minutes to several hours can drop the traffic that makes it to Interchange to a small fraction of the overall requests.

### Caching and the Application Stack

Let's examine an ideal target architecture for a simple implementation of an Interchange store, or stores. Note that we could also introduce load balancing layers to substantially boost capacity through horizontal scaling at multiple points in this stack, and if we did so we'd need to add those to our list to identify the impact of selecting a target cache point.

- Browser
- Reverse proxy (e.g., Varnish, Pound, nginx)
- Web server (e.g., Apache httpd, nginx)
- Interchange, with session storage

    - Database (e.g., MySQL)
    - Other applications (e.g., email server)
    - Web services (e.g., payment gateway)

The higher up the stack we can cache, the more scalable our solution becomes. Interchange comes with [timed-build] which can be used to great effect to cache database results in particular, but also potentially other applications that could produce bottlenecks in performance. Moreover, because Interchange assembles the document, this is the last point in the stack that we can (directly, if at all) partially cache a resource. However, having all requests reach Interchange is, itself, a scalability issue that would have to be resolved with either horizontal scaling or pushing our cache farther up the stack.

It's also possible to produce a static build of assets in the web server's doc space, keeping requests from reaching Interchange at all. And while responses from a web server will have considerably less overhead and better response times than Interchange, both building and maintaining a static repository of Interchange assets is going to take some effort and, ultimately, will require horizontal scaling to relieve overload.

Our target point for the cache described herein is at the reverse proxy. We want to control our cache using standard cache headers and an nginx configuration that uses the full URL for its cache keys. The reverse proxy is chosen because:

- Very fast and efficient at delivering documents.
- Low maintenance as we are able to have proxy engine keep its data storage fresh according to document headers.
- Assets can now be massively scaled through 3rd-party CDNs requiring no infrastructure investment and maintenance that horizontal scaling solutions lower in the stack would.
- Full URL cache keys and cache headers allow us extend our cache all the way to the browser, for those user agents that respect the cache headers.

### Core Interchange Support for Full-Page Caching

To provide general support for full-page caching in Interchange, we found it necessary to introduce some core features into Interchange 5. These features are in final review internally and will be committed to core soon.

#### SuppressCachedCookies

New boolean catalog configuration parameter that, when true, instructs Interchange not to write any cookies in a cacheable response. Cookies are inherently specific to the individual client being served and nginx will refuse to cache a resource containing Set-Cookie headers.

#### $::Instance->{Volatile}

Value indicates to critical core code what the request's cache potential is. Three values:

- **undef** - unknown, could be cached, but hasn't been explicitly identified
- **true** - cannot be cached. Indicates the requested resource is user-dependent and may produce different results for the same URL for different users.
- **false** (other than undef) - explicitly treat as a "can be cached" resource. This setting can be used to reverse override other cache overrides.

The ternary nature of Volatile allows a developer to explicitly control the caching behavior of any given resource if circumstances require an adjustment to the default behavior.

#### [if-not-volatile]

New container tag whose body will only interpolate if the value of $::Instance->{Volatile} at the time of interpolation is false. Tag is particularly useful for placing settings for cache headers on shared resources (includes files, components, etc.) where the final document may or may not be cacheable.

#### OutputCookieHook

Catalog configuration parameter that takes the name of a catalog or global sub to execute just prior to Interchange writing its Set-Cookie headers. Setting was inspired by the need to maintain portions of the session on the client via cookies to allow some more stubborn session-dependent resources to be cacheable.

### Obstacles to Full-Page Caching in Interchange

Standard coding practices in a typical Interchange catalog interfere with full-page caching in a number of ways, primarily:

- Liberal coupling of resources with user sessions
- Searches common to all site users (e.g., category lists) generate saved search objects that force session coupling
- Heavy reliance on non-RESTful URLs, primarily those generated by the process actionmap

In most circumstances, these practices can be altered to produce fully cacheable resources, and particularly if the most heavily used components of the site are addressed first, such as the home page and category lists.

### Catalog Changes to Mitigate Caching Obstacles

Precisely what changes are required depends on the specific coding practices used for the resources in question. However, there are a number of typical usage patterns that will to some degree affect almost all Interchange catalogs.

#### Use RESTful URLs

Avoid unnecessary dependence on the process actionmap, which is often used liberally precisely because it gives lots of hooks into cool and useful features. Avoid any other use of common URLs that produce varying resources based on session dependence.

Take advantage of writing custom actionmaps, which allow the developer extreme flexibility in URL construction. Because actionmaps make it easy and straightforward to produce unique URLs, they are ideal both for creating cacheable resources and fine-tuning SEO.

#### Permanent More for Category Lists

By default, search objects which Interchange uses for more lists, are restricted to access from the generating user's session. This is a safeguard as often search results include personal data for access only to the requestor. However, for features such as category lists, this creates a difficult burden for the developer who wishes to cache the popular resources and whose results are identical across all users.

We can overcome this difficulty by making the search definitions for category lists, or other canned searches, include the [permanent more](/blog/2012/01/02/interchange-search-caching-with) indicator. Permanent more causes all identical searches to share a common search object accessible by the same URLs, and freeing the usual coupling with the session of the search originator.

#### Address Common Session Variables

There are certain session variables that are often found in page code and can cause a number of difficulties when trying to make a resource cacheable. Start by tracking through the use of each of the following and come up with a strategy to remove the dependencies so that the interpolated code is free of them:

- [value]
- [data session ___]
- [set]/[seti]
- Any [if] conditionals that use those respective bases (e.g., [if value], [if session], and [if scratch])

#### Cacheable Redirects

Any code that issues a redirect must do so consistently with respect to its URL. Any redirect will cache the http code and, if issued conditionally, will force all users accessing the cached resource to also redirect. This practice is seen often in Interchange catalogs, particularly when monitoring pages that are restricted to logged-in users. In summary, it's OK to cache redirects, but just make sure that a given URL is either always, or never, redirected.

#### Profile and "Click" Code

It is common practice to define profile and click code in scratch variables. This is particularly true for click code defined with the [button] tag, which while convenient causes the click action to be defined under the hood in scratch space. In order for these event-driven features to work, the resource must compile that code and seed it in the session in anticipation of the user's next actions. If those resources are cached, those important features are never added to the session as the result of a page load and, so, none of the actions will work.

All use of [button] or [set] to produce click or profile code should be moved into the profile files (typically found in etc/profile.*). There they are added to the Interchange global configuration at compile time and are thus available to all users without regard to the state of their sessions. This is good practice generally since it is often easy (particularly with [button]) to have multiple actions map to the same scratch key. When that happens, a user going through the browser back button can get invalid results on actions taken because the click or profile definitions have changed with respect to the anticipated such actions on the current page.

#### Set SuppressCachedCookies to Yes

As described earlier, this will tell the Interchange core not to write any cookies if the resource is to be cached.

#### Define Cache-Control Headers

At any point in the development of the response body, Interchange can be issued a pragma that tells it to treat the response as cacheable. This will interact with the core features described above to ensure that there is no impact on the user session as a result of this request, and put the correct headers in the output stream (as well as keep the cookie headers out).

Invocation looks something like [tag pragma cache_control]max-age=NNN[/tag], where NNN is the number of seconds the cache should persist.

### Impact on Session Management

Any resource considered cacheable should *a priori* have neither impact nor dependence on a session. This must be true if we consider that, once cached, a user will interact with the page--and expect correct behavior--without ever touching Interchange. This introduces some new conditions associated with the session:

- The initial user request against a cacheable resource will *not* generate a session. Why is this so? Apart from the already-noted discrepancy of accessing the resource for a cached vs. live hit, generating a session would necessitate producing the session cookie. Returning that cookie would invalidate the resource as cacheable. Further, one of the significant advantages of a reverse-proxy caching strategy is to provide protection in a DoS attack, and the user agents in such an attack are very unlikely to maintain a session. Thus, if we were failing to produce a cache on initial hits to allow setting a session, **all** those DoS hits would reach Interchange, and on top of that be churning out session entries on the server.
- Session writing is suppressed on any response with a cacheable resource. Interchange must treat the response without any permanence because all accesses of the resource from the cache will *never* reach Interchange. If the request that produced the cache also wrote that user's session, it would produce a deviation in behavior between the cached v. live requests.

### Overrides on a Cacheable Response

Any action resulting in a POST is considered to imply the necessity of the user initiating the request reaching the session (or the database, or some other permanent storage controlled by the Interchange app). Thus POSTs by default force the Volatile setting to true. However, note this can be overridden by the developer if necessary (e.g., if a DoS hits the home page with a POST rather than the expected GET).

Similarly, any requests passing through either the "process" or "order" actionmap are assumed to require access to the session. "process" will most often be issued as a POST as well, although using "order" with a GET is common.

### User State on Cacheable Resources

A big mistake a developer may make when considering full-page caching is to assume an all-or-nothing approach. Trying to compartmentalize an entire catalog into fully cacheable resources would be a daunting task, requiring essentially the construction of a fully client-side application and session management. This is neither realistic nor desirable.

A catalog can gain considerable benefit simply from evaluating those resources which do not require session entanglement at all and starting with them. Without considering users that are logged in or have items in their cart, under most circumstances the home and category list pages should be free from entanglement. With a bit of URL management, the resources can skip the cache when a user is logged in or has items in the cart.

#### "Read Only" User State

If caching is desirable on resources that cannot be decoupled from session influence, we can expose the necessary parts of the session to the client in the form of cookies and can refactor our document to contain client-side code to manage the session use. Typical examples of this would be personalization for logged in users, or the display of a small cart on all pages. The session data stored in the cookie is controlled exclusively by Interchange and is read-only on the client. Each time the session is accessed and updated, the cookie is re-written to the client.

Management of such a process is relatively easy with modern Javascript frameworks such as jQuery. As a typical example, one might need to replace the following session-dependent code

```
  [if session logged_in]
    Hi, [value fname]!
  [/if]
```

with client-side management:

```
  <span id="fname_display"></span>
```
and in the ready() event elsewhere with our session cookie data stored in valuesData:

```
  if (valuesData.fname) {
    $('#fname_display').replaceWith('Hi, ' + valuesData.fname + '!');
  }
```

The OutputCookieHook was developed as a convenient mechanism for constructing the proposed valuesData cookie above, allowing for a subroutine to build the cookie just prior to the core code that constructs the document headers but after any standard actions that would alter the session and would need to be captured in the cookie data.

#### "Read Write" User State

If state needs are more complex on a particularly popular resource, it may be necessary to allow our state cookie to also be updated from the client. With the tools described here, the developer can either amend the existing cookie, or construct a new one, that captures data input by the client through subsequent requests to cached resources. Once the user issues the next non-cached request, an Autoload subroutine could be constructed to identify that changes have occurred and then sync those changes back to the user's session. While implementing read-write user state may be challenging, it is possible and has been done at End Point for clients where that need exists.

---

Hopefully this provides a good idea of how to get started when approaching full-page caching, which is possible in most web app frameworks, and soon will be much easier in Interchange 5 with the new core tools introduced here.
