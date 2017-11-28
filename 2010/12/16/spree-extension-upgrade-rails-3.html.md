---
author: Steph Skardal
gh_issue_number: 387
tags: ecommerce, rails, spree
title: Dissecting a Rails 3 Spree Extension Upgrade
---

A while back, I wrote about the release of Spree 0.30.* [here](/blog/2010/10/25/spree-on-rails-3-part-one) and [here](/blog/2010/10/25/spree-on-rails-3-part-two). I didn't describe extension development in depth because I hadn't developed any Rails 3 extensions of substance for End Point's clients. Last month, I worked on an advanced reporting extension for a client running on Spree 0.10.2. I spent some time upgrading this extension to be compatible with Rails 3 because I expect the client to move in the direction of Rails 3 and because I wanted the extension to be available to the community since Spree's reporting is fairly lightweight.

Just a quick rundown on what the extension does: It provides incremental reports such as revenue, units sold, profit (calculated by sales minus cost) in daily, weekly, monthly, quarterly, and yearly increments. It reports Geodata to show revenue, units sold, and profit by [US] states and countries. There are also two special reports that show top products and customers. The extension allows administrators to limit results by order date, "store" (for [Spree's multi-site architecture](/blog/2010/05/24/spree-multi-store-architecture)), product, and taxon. Finally, the extension provides the ability to export data in PDF or CSV format using the Ruport gem. One thing to note is that this extensions does not include new models – this is significant only because Rails 3 introduced significant changes to ActiveRecord, which are not described in this article.

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td valign="top">
<a href="/blog/2010/12/16/spree-extension-upgrade-rails-3/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5551351830109836498" src="/blog/2010/12/16/spree-extension-upgrade-rails-3/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 200px; height: 158px;"/></a>
</td>
<td valign="top">
<a href="/blog/2010/12/16/spree-extension-upgrade-rails-3/image-1-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5551351835672839570" src="/blog/2010/12/16/spree-extension-upgrade-rails-3/image-1.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 200px; height: 112px;"/></a>
</td>
</tr><tr>
<td valign="top">
<a href="/blog/2010/12/16/spree-extension-upgrade-rails-3/image-2-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5551351833995652594" src="/blog/2010/12/16/spree-extension-upgrade-rails-3/image-2.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 200px; height: 99px;"/></a>
</td><td valign="top">
<a href="/blog/2010/12/16/spree-extension-upgrade-rails-3/image-3-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5551351834485444850" src="/blog/2010/12/16/spree-extension-upgrade-rails-3/image-3.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 200px; height: 110px;"/></a>
</td>
</tr><tr>
<td valign="top">
<a href="/blog/2010/12/16/spree-extension-upgrade-rails-3/image-4-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5551351844023719202" src="/blog/2010/12/16/spree-extension-upgrade-rails-3/image-4.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 200px; height: 77px;"/></a>
</td><td align="center">
Screenshots of the Spree Advanced Reporting extension.
</td></tr></tbody></table>

To deconstruct the upgrade, I examined a git diff of the master and rails3 branch. I've divided the topics into Rails 3 and Spree specific categories.

## Rails 3 Specific

### SafeBuffers

In my report extension, I utilize Ruport's to_html method, which returns a ruport table object to an HTML table. With the upgrade to Rails 3, ruports to_html was spitting out escaped HTML with the addition of default XSS protection. The change is described [here](http://yehudakatz.com/2010/02/01/safebuffers-and-rails-3-0/). and required the addition of a new helper method (raw) to yield unescaped HTML:

```diff
diff --git a/app/views/admin/reports/top_base.html.erb b/app/views/admin/reports/top_base.html.erb
index 6cc6b70..92f2118 100644
--- a/app/views/admin/reports/top_base.html.erb
+++ b/app/views/admin/reports/top_base.html.erb
@@ -1,4 +1,4 @@
-<%= @report.ruportdata.to_html %>
+<%= raw @report.ruportdata.to_html %>
```

### Common Deprecation Messages

While troubleshooting the upgrade, I came across the following warning:

```nohighlight
DEPRECATION WARNING: Using #request_uri is deprecated. Use fullpath instead. (called from ...)
```

I made several changes to address the deprecation warnings, did a full round of testing, and moved on.

```diff
diff --git a/app/views/admin/reports/_advanced_report_criteria.html.erb b/app/views/admin/reports/_advanced_report_criteria.html.erb
index ba69a2e..6d9c3f9 100644
--- a/app/views/admin/reports/_advanced_report_criteria.html.erb
+++ b/app/views/admin/reports/_advanced_report_criteria.html.erb
@@ -1,11 +1,11 @@
 <% @reports.each do |key, value| %>
-  <option <%= request.request_uri == "/admin/reports/#{key}" ? 'selected="selected" ' : '' %>
  value="<%= send("#{key}_admin_reports_url".to_sym) %>">
+  <option <%= request.fullpath == "/admin/reports/#{key}" ? 'selected="selected" ' : '' %>
  value="<%= send("admin_reports_#{key}_url".to_sym) %>">
     <%= t(value[:name].downcase.gsub(" ","_")) %>

```

### Integrating Gems

An exciting change in Rails 3 is the advancement of Rails::Engines to allow easier inclusion of mini-applications inside the main application. In an ecommerce platform, it makes sense to break up the system components into Rails Engines. Extensions become gems in Spree and gems can be released through rubygems.org. A gemspec is required in order for my extension to be treated as a gem by my main application, shown below. Componentizing elements of a larger platform into gems may become popular with the advancement of Rails::Engines / Railties.

```diff
diff --git a/advanced_reporting.gemspec b/advanced_reporting.gemspec
new file mode 100644
index 0000000..71f00a8
--- /dev/null
+++ b/advanced_reporting.gemspec
@@ -0,0 +1,22 @@
+Gem::Specification.new do |s|
+  s.platform    = Gem::Platform::RUBY
+  s.name        = 'advanced_reporting'
+  s.version     = '2.0.0'
+  s.summary     = 'Advanced Reporting for Spree'
+  s.homepage    = 'http://www.endpoint.com'
+  s.author = "Steph Skardal"
+  s.email = "steph@endpoint.com"
+  s.required_ruby_version = '>= 1.8.7'
+
+  s.files        = Dir['CHANGELOG', 'README.md', 'LICENSE', 'lib/**/*', 'app/**/*']
+  s.require_path = 'lib'
+  s.requirements << 'none'
+
+  s.has_rdoc = true
+
+  s.add_dependency('spree_core', '>= 0.30.1')
+  s.add_dependency('ruport')
+  s.add_dependency('ruport-util') #, :lib => 'ruport/util')
+end
```

### Routing Updates

With the release of Rails 3, there was a major rewrite of the router and integration of rack-mount. The [Rails 3 release notes on Action Dispatch](http://edgeguides.rubyonrails.org/3_0_release_notes.html#action-dispatch) provide a good starting point of resources. In the case of my extension, I rewrote the contents of config/routes.rb:

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td>
<b>Before</b>
<pre class="brush:ruby">
map.namespace :admin do |admin|
  admin.resources :reports, :collection => {
    :sales_total => :get,
    :revenue   => :get,
    :units   => :get,
    :profit   => :get,
    :count   => :get,
    :top_products  => :get,
    :top_customers  => :get,
    :geo_revenue  => :get,
    :geo_units  => :get,
    :geo_profit  => :get,
  }
  map.admin "/admin",
    :controller => 'admin/advanced_report_overview',
    :action => 'index'
end
</pre>
</td></tr><tr><td>
<b>After</b>
<pre class="brush:ruby">
Rails.application.routes.draw do
  #namespace :admin do
  #  resources :reports, :only => [:index, :show] do
  #    collection do
  #      get :sales_total
  #    end
  #  end
  #end
  match '/admin/reports/revenue' => 'admin/reports#revenue', :via => [:get, :post]
  match '/admin/reports/count' => 'admin/reports#count', :via => [:get, :post]
  match '/admin/reports/units' => 'admin/reports#units', :via => [:get, :post]
  match '/admin/reports/profit' => 'admin/reports#profit', :via => [:get, :post]
  match '/admin/reports/top_customers' => 'admin/reports#top_customers', :via => [:get, :post]
  match '/admin/reports/top_products' => 'admin/reports#top_products', :via => [:get, :post]
  match '/admin/reports/geo_revenue' => 'admin/reports#geo_revenue', :via => [:get, :post]
  match '/admin/reports/geo_units' => 'admin/reports#geo_units', :via => [:get, :post]
  match '/admin/reports/geo_profit' => 'admin/reports#geo_profit', :via => [:get, :post]
  match "/admin" => "admin/advanced_report_overview#index", :as => :admin
end
</pre>
</td></tr></tbody></table>

## Spree Specific

### Transition extension to Engine

The biggest transition to Rails 3 based Spree requires extensions to transition to Rails Engines. In Spree 0.11.*, the extension class inherits from Spree::Extension and the path of activation for extensions in Spree 0.11.* starts in initializer.rb where the ExtensionLoader is called to load and activate all extensions. In Spree 0.30.*, extensions inherit from Rails:Engine which is a subclass of Rails::Railtie. Making an extension a Rails::Engine allows it to hook into all parts of the Rails initialization process and interact with the application object. A Rails engine allows you run a mini application inside the main application, which is at the core of what a Spree extension is – a self-contained Rails application that is included in the main ecommerce application to introduce new features or override core behavior.

See the diffs between versions here:

<table width="100%">
<tbody><tr>
<td>
<b>Before</b>
<pre class="brush:diff">
diff --git a/advanced_reporting_extension.rb b/advanced_reporting_extension.rb
deleted file mode 100644
index f75d967..0000000
--- a/advanced_reporting_extension.rb
+++ /dev/null
@@ -1,46 +0,0 @@
-# Uncomment this if you reference any of your controllers in activate
-# require_dependency 'application'
-
-class AdvancedReportingExtension < Spree::Extension
-  version "1.0"
-  description "Advanced Reporting"
-  url "http://www.endpoint.com/"
-
-  def self.require_gems(config)
-    config.gem "ruport"
-    config.gem "ruport-util", :lib => 'ruport/util'
-  end
-
-  def activate
-    Admin::ReportsController.send(:include, AdvancedReporting::ReportsController)
-    Admin::ReportsController::AVAILABLE_REPORTS.merge(AdvancedReporting::ReportsController::ADVANCED_REPORTS)
-
-    Ruport::Formatter::HTML.class_eval do
-      # Override some Ruport functionality
-    end
-  end
-end
</pre>
</td></tr><tr><td>
<b>After</b>
<pre class="brush:diff">
diff --git a/lib/advanced_reporting.rb b/lib/advanced_reporting.rb
new file mode 100644
index 0000000..4e6fee6
--- /dev/null
+++ b/lib/advanced_reporting.rb
@@ -0,0 +1,50 @@
+require 'spree_core'
+require 'advanced_reporting_hooks'
+require "ruport"
+require "ruport/util"
+
+module AdvancedReporting
+  class Engine < Rails::Engine
+    config.autoload_paths += %W(#{config.root}/lib)
+
+    def self.activate
+      #Dir.glob(File.join(File.dirname(__FILE__), "../app/**/*_decorator*.rb")) do |c|
+      #  Rails.env.production? ? require(c) : load(c)
+      #end
+
+      Admin::ReportsController.send(:include, Admin::ReportsControllerDecorator)
+      Admin::ReportsController::AVAILABLE_REPORTS.merge(Admin::ReportsControllerDecorator::ADVANCED_REPORTS)
+
+      Ruport::Formatter::HTML.class_eval do
+        # Override some Ruport functionality
+      end
+    end
+
+    config.to_prepare &method(:activate).to_proc
+  end
+end
</pre>
</td></tr></tbody></table>

### Required Rake Tasks

Rails Engines in Rails 3.1 will allow migrations and public assets to be accessed from engine subdirectories, but a work-around is required to access migrations and assets in the main application directory in the meantime. There are a few options for accessing Engine migrations and assets; Spree recommends a couple rake tasks to copy assets to the application root, shown here:

```diff
diff --git a/lib/tasks/install.rake b/lib/tasks/install.rake
new file mode 100644
index 0000000..c878a04
--- /dev/null
+++ b/lib/tasks/install.rake
@@ -0,0 +1,26 @@
+namespace :advanced_reporting do
+  desc "Copies all migrations and assets (NOTE: This will be obsolete with Rails 3.1)"
+  task :install do
+    Rake::Task['advanced_reporting:install:migrations'].invoke
+    Rake::Task['advanced_reporting:install:assets'].invoke
+  end
+
+  namespace :install do
+    desc "Copies all migrations (NOTE: This will be obsolete with Rails 3.1)"
+    task :migrations do
+      source = File.join(File.dirname(__FILE__), '..', '..', 'db')
+      destination = File.join(Rails.root, 'db')
+      puts "INFO: Mirroring assets from #{source} to #{destination}"
+      Spree::FileUtilz.mirror_files(source, destination)
+    end
+
+    desc "Copies all assets (NOTE: This will be obsolete with Rails 3.1)"
+    task :assets do
+      source = File.join(File.dirname(__FILE__), '..', '..', 'public')
+      destination = File.join(Rails.root, 'public')
+      puts "INFO: Mirroring assets from #{source} to #{destination}"
+      Spree::FileUtilz.mirror_files(source, destination)
+    end
+  end
+end
```

### Relocation of hooks file

A minor change with the extension upgrade is a relocation of the hooks file. Spree hooks allow you to interact with core Spree views, described more in depth [here](/blog/2010/01/12/rails-ecommerce-spree-hooks-tutorial) and [here](/blog/2010/01/13/rails-ecommerce-spree-hooks-comments).

```diff
diff --git a/advanced_reporting_hooks.rb b/advanced_reporting_hooks.rb
deleted file mode 100644
index fcb5ab5..0000000
--- a/advanced_reporting_hooks.rb
+++ /dev/null
@@ -1,43 +0,0 @@
-class AdvancedReportingHooks < Spree::ThemeSupport::HookListener
-  # custom hooks go here
-end

diff --git a/lib/advanced_reporting_hooks.rb b/lib/advanced_reporting_hooks.rb
new file mode 100644
index 0000000..cca155e
--- /dev/null
+++ b/lib/advanced_reporting_hooks.rb
@@ -0,0 +1,3 @@
+class AdvancedReportingHooks < Spree::ThemeSupport::HookListener
+  # custom hooks go here
+end
```

### Adoption of "Decorator" naming convention

A common behavior in Spree extensions is to override or extend core controllers and models. With the upgrade, Spree adopts the "decorator" naming convention:

```ruby
Dir.glob(File.join(File.dirname(__FILE__), "../app/**/*_decorator*.rb")) do |c|
  Rails.env.production? ? require(c) : load(c)
end
```

I prefer to extend the controllers and models with module includes, but the decorator convention also works nicely.

### Gem Dependency Updates

With the transition to Rails 3, I found that there were changes related to dependency upgrades. Spree 0.11.* uses searchlogic 2.3.5, and Spree 0.30.1 uses searchlogic 3.0.0.*. Searchlogic is the gem that performs the search for orders in my report to pull orders between a certain time frame or tied to a specific store. I didn't go digging around in the searchlogic upgrade changes, but I referenced Spree's core implementation of searchlogic to determine the required updates:



```diff
diff --git a/lib/advanced_report.rb b/lib/advanced_report.rb
@@ -13,11 +15,26 @@ class AdvancedReport
     self.params = params
     self.data = {}
     self.ruportdata = {}
+
+    params[:search] ||= {}
+    if params[:search][:created_at_greater_than].blank?
+      params[:search][:created_at_greater_than] =
+        Order.first(:order => :completed_at).completed_at.to_date.beginning_of_day
+    else
+      params[:search][:created_at_greater_than] =
+        Time.zone.parse(params[:search][:created_at_greater_than]).beginning_of_day rescue ""
+    end
+    if params[:search][:created_at_less_than].blank?
+      params[:search][:created_at_less_than] =
+        Order.last(:order => :completed_at).completed_at.to_date.end_of_day
+    else
+      params[:search][:created_at_less_than] =
+        Time.zone.parse(params[:search][:created_at_less_than]).end_of_day rescue ""
+    end
+
+    params[:search][:completed_at_not_null] ||= "1"
+    if params[:search].delete(:completed_at_not_null) == "1"
+      params[:search][:completed_at_not_null] = true
+    end
     search = Order.searchlogic(params[:search])
-    search.checkout_complete = true
     search.state_does_not_equal('canceled')
-
-    self.orders = search.find(:all)
+    self.orders = search.do_search

     self.product_in_taxon = true
     if params[:advanced_reporting]
```

### Rakefile diffs

Finally, there are substantial changes to the Rakefile, which are related to rake tasks and testing framework. These didn't impact my development directly. Perhaps when I get into more significant testing on another extension, I'll dig deeper into the code changes here.

```diff
diff --git a/Rakefile b/Rakefile
index f279cc8..f9e6a0e 100644
# lots of stuff
```

For those interested in learning more about the upgrade process, I recommend the reviewing the [Rails 3 Release Notes](http://edgeguides.rubyonrails.org/3_0_release_notes.html) in addition to reading up on Rails Engines as they are an important part of Spree's core and extension architecture. The advanced reporting extension described in this article is available [here](https://github.com/stephskardal/spree-advanced-reporting).
