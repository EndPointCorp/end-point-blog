---
author: Brian Gadoury
gh_issue_number: 531
tags: ecommerce, open-source, ruby, rails, spree
title: Rails Request-Based Routing Constraints in Spree
---



I recently adopted an unreleased ecommerce project running Spree 0.60.0 on Rails 3.0.9. The site used a Rails routing constraint and wildcard DNS to dynamically route subdomains to the “dispatch” action of the organizations_controller. If a request’s subdomain component matched that regular expression, it was routed to the dispatch method. Here's the original route:

```ruby
match '/' =&gt; 'organizations#dispatch', :constraints =&gt; { :subdomain =&gt; /.+/ }
```

The business requirement driving this feature was that a User could register an Organization by submitting a form on the site. Once that Organization was marked "approved" by an admin, that Organization would become accessible at their own subdomain - *no server configuration required*.

For marketing reasons, we decided to switch from subdomains to top-level subdirectories. This meant RESTful routes (e.g. domain.com/organizations/143) wouldn’t cut it. In order to handle this, I created a routing constraint class called OrgConstraint. This routing constraint class works in tandem with a tweaked version of that original route.

```ruby
match '*org_url' =&gt; 'organizations#show', :constraints =&gt; OrgConstraint.new
```

The :constraints param takes an *instance* of a class (not a class name) that responds to a matches? predicate method that returns true or false. If matches? returns true, the request will be routed to that controller#action. Else, that route is treated like any other non-matching route. Here’s the entire OrgConstraint class:

```ruby
class OrgConstraint
  def matches?(request)
    Organization.valid_url? request.path_parameters[:org_url]
  end
end
```

Note how Rails automatically passes the [request object](http://guides.rubyonrails.org/action_controller_overview.html#the-request-object) to the matches? method. Also note how the relative url of the request is available via the :org_url symbol - the same identifier we used in the route definition. The Organization.valid_url? class method encapsulates the logic of examining a simple cached (via Rails.cache) hash consisting of organization urls as keys and true as their value.

The final step in this process is, of course, the organizations_controller’s show method. It now needs to look for that same :org_url param that the route definition creates, in the standard params hash we all know and love:

```ruby
def show
  @organization = Organization.find(params[:id]) if params[:id]  
  # from routing constraint
  @organization ||= Organization.find_by_url(params[:org_url]) if params[:org_url]  
  ...
end
```

I should point out that Rails instantiates exactly one instance of your routing constraint class when it first loads your routes. This means you’ll want to ensure your class’s design will respond appropriately to changes in any underlying data. This is one of the reasons the Organization class caches the {$org_url => true} hash rather than using instance variables within the OrgConstraint class.

 


