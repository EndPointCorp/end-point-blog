---
author: Brian Buchalter
title: 'Performing Bulk Edits in Rails: Part 2'
github_issue_number: 518
tags:
- rails
date: 2011-12-03
---



This is the second article in the series on how to perform a bulk edit in Rails. Let’s recap our user’s story from [Part 1](/blog/2011/11/performing-bulk-edits-in-rails-part-1/). 

- User makes a selection of records and clicks “Bulk Edit” button
- User works with the same form they would use for a regular edit, plus

    - check boxes are added by each attribute to allow the user to indicate this variable should be affected by the bulk edit
    - only attributes which are the same among selected records should be populated in the form

Part 1 addressed the first part of our user story. Now that we have our user’s selection, we need to create an interface to allow them to select attributes affected by the bulk edit. Let’s start with the form we’ll use to POST our input.

```ruby
# app/controllers/bulk_edits_controller.rb

def new
  @foos = Foo.find(params[:stored_file_ids]) #params collected by work done in Part 1
  @foo = Foo.new
end

# app/views/bulk_edit/new.html.erb

<%= form_for @foo, :url => "/bulk_edits" do |f| %>
  <% @foos.each do |foo| %>
    <%= hidden_field_tag "foo_ids[]", foo.id %>
  <% end %>
  <%= render "foos/form", :f => f %>
  <%= f.submit %>
<% end %>
```

Let’s first look at how we formed our form_for tag. Although this is a form for a Foo object, we don’t want to POST to foos_controller#create so we add :url => "/bulk_edits" which will POST to the bulk_edits_controller#create. Additionally, we need to send along the foo_ids we eventually want to bulk update. Finally, we don’t want to re-create the form we already have for Foo. By modifying one master form, we’ll make long term maintenance easier. Now that we’ve got our form posting to the right place, let’s see what modifications will need to make to our standard form to allow the user to highlight attributes they want to modify.

```ruby
# app/views/foos/_form.html.erb

<%= check_box_tag "bulk_edit[]", :bar %>
<%= f.label :bar %>
<%= f.text_field :bar %>
```

<div class="separator" style="text-align: center;"><img border="0" height="52" src="/blog/2011/12/performing-bulk-edits-in-rails-part-2/image-0.png" width="320"/><br/>
Bulk edit check boxes appear in front of field names to let users know which fields will be modified.</div>

We’ve added another [check_box_tag](http://api.rubyonrails.org/classes/ActionView/Helpers/FormTagHelper.html#method-i-check_box_tag) to the form to record which attributes the user will select for bulk updating. However, we only want to display this when we’re doing a bulk edit. Let’s tweak this a bit further.

```ruby
# app/views/foos/_form.html.erb

<%= bulk_edit_tag :bar %>
<%= f.label :bar %>
<%= f.text_field :bar %>

# app/helpers/foos_helper.rb

def bulk_edit_tag(attr)
  check_box_tag("bulk_edit[]", attr) if bulk_edit?
end

def bulk_edit?
  params[:controller] == "bulk_edits"
end
```

With these modifications to the form in place, the user can now specify which fields are eligible for bulk editing. Now we need the logic to determine how to populate the bar attribute based on the user’s selection. This way, the user will see that an attribute is the same across all selected items. Let’s revise our bulk edit controller.

```ruby
# app/controllers/bulk_edit_controller.rb

def new
  @foos = Foo.find(params[:foo_ids])
  matching_attributes = Foo.matching_attributes_from(@foos)
  @foo = Foo.new(matching_attributes)
end

# app/models/foo.rb

def self.matching_attributes_from(foos)

  matching = {}
  attriubtes_to_match = Foo.new.attribute_names  #see <a href="http://api.rubyonrails.org/classes/ActiveRecord/Base.html#method-c-attribute_names">attribute_names</a> for more details

  foos.each do |foo|

    attributes_to_match.each do |attribute|

      value = foo.__send__(attribute)  #see <a href="http://apidock.com/ruby/Object/__send__">send</a>, invokes the method identified by symbol, use underscore version to avoid namespace issues

      if matching[attribute].nil?
        matching[attribute] = value  #assume it's a match

      elsif matching[attribute] != value
        matching[attribute] = "" #on the first mismatch, empty the value, but don't make it nil

      end

    end

  end
end

```

<div class="separator" style="clear: both; text-align: center;"><img border="0" height="57" src="/blog/2011/12/performing-bulk-edits-in-rails-part-2/image-1.png" width="320"/><br/>
Only fields which are the same across all selected records will be populated. Other fields will be left blank by default.</div>

With Foo#matching_attributes_for generating a hash of matching attributes, the form will only populate fields which match across all of the user’s selected items. With our form in place, the last step is to actually perform the bulk edit.

```ruby
# app/controllers/bulk_edits_controller.rb
def create
  if params.has_key? :bulk_edit

    foos = Foo.find(params[:foo_ids])
    foos.each do |foo|

        eligible_params = {}
        params[:bulk_edit].each do |eligible_attr|

            #create hash of eligible_attributes and the user's value
            eligible_params.merge! { eligible_attr => params[:foo][eligible_attr] } 

        end

        #update each record, but only with eligible attributes
        foo.update_attributes(eligible_params)

    end
  end
end
```

We’ve now completed the entire user story. Users are able to use check boxes to identify which attributes should be bulk updated. They also get to see which attributes match across their selection. Things are, of course, always more involved with a real production application. Keep in mind this example does not make good use of mass assignment protection using [attr_accessible](https://apidock.com/rails/ActiveRecord/Base/attr_accessible/class) and forcing an empty whitelist of attributes by using [config.active_record.whitelist_attributes](http://guides.rubyonrails.org/configuring.html#configuring-active-record) = true. This is a best practice that should be implemented anytime you need sever-side validation of your forms.

Additionally, there may be cases where you want to perform bulk edits of more complex attributes, such as nested attributes. Consider appending your additional attributes to the Foo.new.attribute_names array and then tweaking the eligible attributes logic. Also consider implementing a maximum number of records which are able to be bulk edited at a time; wouldn’t want your server to time out. Good luck!


