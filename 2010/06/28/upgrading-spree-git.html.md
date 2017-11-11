---
author: Steph Skardal
gh_issue_number: 322
tags: ecommerce, rails, spree, git
title: Upgrading Spree with the help of Git
---

Lately, I've upgraded a few Spree projects with the recent Spree releases. Spree is a Ruby on Rails ecommerce platform that End Point previously sponsored and continues to support. In all cases, my Spree project was running from the Spree gem (version 0.10.2) and I was upgrading to Spree 0.11.0. I wanted to go through a brief explanation on how I went about upgrading my projects.

<a href="http://spreecommerce.com/"><img alt="Spree" src="http://spreecommerce.com/images/new_logo.png"/></a>

First, I made sure my application was running and committed all recent changes to have a clean branch. I follow the development principles outlined [here](http://blog.endpoint.com/2010/03/spree-software-development.html) that describe methodology for developing custom functionality on top of the Spree framework core. All of my custom functionality lives in the RAILS_ROOT/vendor/extensions/site/ directory, so that directory probably won't be touched during the upgrade.

```nohighlight
steph@The-Laptop:/var/www/ep/myproject$ git status
# On branch master
nothing to commit (working directory clean)
```

Then, I tried the rake spree:upgrade task with the following results. I haven't upgraded Spree recently, and I vaguely remembered there being an upgrade task.

```nohighlight
steph@The-Laptop:/var/www/ep/myproject$ rake spree:upgrade
(in /var/www/ep/myproject)
[find_by_param error] database not available?
This task has been deprecated.  Run 'spree --update' command using the newest gem instead.
```

OK. The upgrade task has been removed. So, I try spree --update:

```nohighlight
Updating to Spree 0.11.0 ...
Finished.
```

That was easy! I run 'git status' and saw that there were several modified config/ files, and a few new config/ files:

```nohighlight
# On branch master
# Changed but not updated:
#   (use "git add <file>..." to update what will be committed)
#   (use "git checkout -- <file>..." to discard changes in working directory)
#
#       modified:   config/boot.rb
#       modified:   config/environment.rb
#       modified:   config/environments/production.rb
#       modified:   config/environments/staging.rb
#       modified:   config/environments/test.rb
#       modified:   config/initializers/locales.rb
#       modified:   config/initializers/new_rails_defaults.rb
#       modified:   config/initializers/spree.rb
#
# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
#
#       config/boot.rb~
#       config/environment.rb~
#       config/environments/cucumber.rb
#       config/environments/production.rb~
#       config/environments/staging.rb~
#       config/environments/test.rb~
#       config/initializers/cookie_verification_secret.rb
#       config/initializers/locales.rb~
#       config/initializers/new_rails_defaults.rb~
#       config/initializers/spree.rb~
#       config/initializers/touch.rb
#       config/initializers/workarounds_for_ruby19.rb
</file></file></file>
```

Because I had a clean master branch before the upgrade, I can easily examine the code changes for this upgrade from Spree 0.10.2 to Spree 0.11.0:

config/boot.rb

```diff
-      load_rails("2.3.5")  # note: spree requires this specific version of rails (change at your own risk)
+      load_rails("2.3.8")  # note: spree requires this specific version of rails (change at your own risk)
```

config/environment.rb

```diff
-  config.gem 'authlogic', :version => '>=2.1.2'
+  config.gem 'authlogic', :version => '2.1.3'
-  config.gem 'will_paginate', :lib => 'will_paginate', :version => '2.3.11'
+  config.gem 'will_paginate', :lib => 'will_paginate', :version => '2.3.14'
-  config.i18n.default_locale = :'en-US'
+  config.i18n.default_locale = :'en'
```

config/environment/test.rb

```diff
-config.gem 'test-unit', :lib => 'test/unit', :version => '~>2.0.5' if RUBY_VERSION.to_f >= 1.9
+config.gem 'test-unit', :lib => 'test/unit', :version => '~>2.0.9' if RUBY_VERSION.to_f >= 1.9
```

Most of the changes were not surprising, except that the locale changes here are significant because they may require extension locales to be updated. After I reviewed these changes, I installed newer gem dependencies and bootstrapped the data since all my application data was stored in sample data files and restarted the server to test the upgrade. Then, I added the config/ and public/ files in a single git commit. I removed the old temporary configuration files that were left around from the upgrade.

For this particular upgrade, my git log shows changes in the files below. The config/ files were made when I ran the update, and the public/ files were modified when I restarted the server as gem public/ files are copied over during a restart.

```nohighlight
commit 96a68e86064aa29f51c5052631f896845c11c266
Author: Steph Powell <steph@endpoint.com>
Date:   Mon Jun 28 13:44:50 2010 -0600

    Spree upgrade.

diff --git a/config/boot.rb b/config/boot.rb
diff --git a/config/environment.rb b/config/environment.rb
diff --git a/config/environments/cucumber.rb b/config/environments/cucumber.rb
diff --git a/config/environments/production.rb b/config/environments/production.rb
diff --git a/config/environments/staging.rb b/config/environments/staging.rb
diff --git a/config/environments/test.rb b/config/environments/test.rb
diff --git a/config/initializers/cookie_verification_secret.rb b/config/initializers/cookie_verification_secret.rb
diff --git a/config/initializers/locales.rb b/config/initializers/locales.rb
diff --git a/config/initializers/new_rails_defaults.rb b/config/initializers/new_rails_defaults.rb
diff --git a/config/initializers/spree.rb b/config/initializers/spree.rb
diff --git a/config/initializers/touch.rb b/config/initializers/touch.rb
diff --git a/config/initializers/workarounds_for_ruby19.rb b/config/initializers/workarounds_for_ruby19.rb
diff --git a/public/images/admin/bg/spree_50.png b/public/images/admin/bg/spree_50.png
Binary files a/public/images/admin/bg/spree_50.png and b/public/images/admin/bg/spree_50.png differ
diff --git a/public/images/tile-header.png b/public/images/tile-header.png
Binary files /dev/null and b/public/images/tile-header.png differ
diff --git a/public/images/tile-slider.png b/public/images/tile-slider.png
Binary files /dev/null and b/public/images/tile-slider.png differ
diff --git a/public/javascripts/admin/checkouts/edit.js b/public/javascripts/admin/checkouts/edit.js
diff --git a/public/javascripts/taxonomy.js b/public/javascripts/taxonomy.js
diff --git a/public/stylesheets/admin/admin-tables.css b/public/stylesheets/admin/admin-tables.css
diff --git a/public/stylesheets/admin/admin.css b/public/stylesheets/admin/admin.css
diff --git a/public/stylesheets/screen.css b/public/stylesheets/screen.css
```

From my experience, the config/ and public/ files are typically modified with a small release. If your project has custom JavaScript, or overrides the Spree core JavaScript, you may have to review the upgrade changes more carefully. Version control goes a long way in highlighting changes and problem areas. Additionally, having custom code abstracted from the Spree core should allow for easier maintenance of your project.
