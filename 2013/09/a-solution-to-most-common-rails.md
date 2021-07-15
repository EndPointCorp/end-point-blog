---
author: Tim Case
title: A Solution to the Most Common Rails Authentication Problem
github_issue_number: 858
tags:
- ruby
- rails
date: 2013-09-24
---

Q: What’s one of the most common authentication related mistakes?

A: Forgetting to write the code that triggers authentication.

Q: What can we do about it?

A: Make it easier to test authentication.

The most common authentication problem that probably affects every Rails app is forgetting or overlooking the implementation of the authentication.  In Rails, this generally means forgetting to add a controller before filter to verify the user is authenticated for actions that should be protected.  Let me be the first to admit that I’m guilty of doing this myself but I’ve noticed it occurring in all Rails apps that I’ve worked on.

Having seen this problem, committed it myself, and being bothered by it, I’ve come up with a small solution that is my humble attempt to solve the problem by making it easier to track what is being authenticated and what isn’t.  Before I show the solution I want to divulge that the current implementation has some shortcomings which I will explain towards the end of the article, but I feel it’s still a worthwhile solution in the form of the “good outweighs the bad”.

The solution is to provide helpers that make it easy to unit test the authentication of controllers.  I’m sure this has been done before but I’ve not found a standard way to do this so I’m going to propose one.  Here is a code example:

### The solution in a nutshell:

```
require 'test_helper'

class InquiriesControllerTest < ActionController::TestCase

  verify_authentication_declared
  verify_require_authenticate :edit, :update
  verify_do_not_require_authenticate :new, :create

end

class InquiriesNotifiersController < ApplicationController
  before_filter :authenticate, only: [:edit, :update]
  before_filter :do_not_authenticate, only: [:new, :create]

  def new
  end

  def create
  end

  def edit
  end

  def update
  end
end
```
I created a test helper which allows you to add to add three lines of code to verify your authentication:

1. verify_authentication_declared — Does two different things:
    a. Checks that all actions in your controller are explicitly listed in the tested controller’s before_filters.  In my example I have two before_filters that call :authenticate and :do_not_authenticate.
    b. Checks that no actions are listed for both :authenticate, and do not :authenticate.
2. verify_require_authenticate — Allows the developer to specify what actions are intended to be authenticated
3. verify_do_not_authenticate — Allows the developer to specify what actions don’t require authentication, notice that this is different than just not setting the before_filter for :authenticate, what this does is clearly communicate the intent that the action should not be authenticated.

### How to implement:

1. Grab the test helper [in this gist](https://gist.github.com/timcase/6691475) and place it in your test folder alongside ‘test_helper.rb’, name it ‘auth_test_helper.rb’
2. In ‘test_helper.rb’, require the auth_test_helper and extend TestHelper with it:

    ```
    require 'auth_test_helper'
    class ActiveSupport::TestCase
      extend AuthTestHelper
    ```
3. If your solution uses an authentication before_filter with a different name than authenticate then you can either change the name in ‘auth_test_helper.rb’ or you can add an alias in your application controller, and then use the alias in your controllers. For example:

    ```
    class ApplicationController
     def authenticate
       require_login
     end
    end

    def ProductsController < ApplicationController
     before_filter :authenticate, only: [:new]

     def new
     end
    end
    ```

    Important note: the auth tests look for the :only symbol to determine which actions are covered so mod AuthTestHelper if you want to use :except.

    Alternatively, you can use the :authenticate method to actually perform the authentication.  This would be the choice if you roll your own authentication:

    ```
     def authenticate
       redirect_to login_url, alert: "Please login, and you’ll be sent to the page you tried to access." if current_user.nil?
     end
    ```

4. Add a method to ApplicationController for do_not_authenticate, the method doesn’t actually do anything and serves only to make it possible to declare which actions are not authenticated

    ```
    class ApplicationController
      def authenticate
        require_login
      end
       
      def do_not_authenticate
      end
    end

    def ProductsController < ApplicationController
      before_filter :authenticate, only: [:new]
      before_filter :do_not_authenticate, only: [:edit]
      def new
      end

      def edit
      end
    end
    ```

5. In your test for the controller add three lines of verify code:

    ```
      verify_authentication_declared
      verify_require_authenticate :edit, :update
      verify_do_not_require_authenticate :new, :create
      
    ```

    Only :verify_require_authenticate and :verify_do_not_require_authenticate accept parameters and those will be symbols of the methods that they verify.

### Shortcomings of this Approach:

1. It could be argued that this isn’t a solution merely moving the problem out into the tests.  By that I mean, if the developer doesn’t implement the three line verify block then there again can be the problem of forgotten authentication.  My idea to address this was to have :verify_authentication_declared automatically executed for each controller test but as of this writing I couldn’t get it to technically work.
2. The verify methods throw exceptions instead of making failed assertions.  This is wrong from a testing sense, the verify methods for authentication should be asserts like any other test, and throwing an exception should be reserved for when something unusual happens.

Despite the shortcomings listed above, I still think the good outweighs the bad, and if over time these tests prove themselves to be valuable I’m going to fix the shortcomings, for now I’m going to present the idea and let people play with it.

### Source code

[Gist for AuthTestHelper](https://gist.github.com/timcase/6691475)
