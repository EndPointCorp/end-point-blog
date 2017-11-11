---
author: Steph Skardal
gh_issue_number: 544
tags: ecommerce, ruby, rails
title: Importing Data with RailsAdmin
---

**Update #1: Read an update to this functionality [here](http://blog.endpoint.com/2012/02/railsadmin-import-part-2.html).**

**Update #2: This article was written in January of 2012, and the code related to the RailsAdmin actions no longer applies to the current release. Please make sure to read the [RailsAdmin](https://github.com/sferik/rails_admin) documentation regarding current action implementation.**

I've blogged about [RailsAdmin](https://github.com/sferik/rails_admin) a few times lately. I've now used it for several projects, and have included it as a based for the Admin interface my recent released [ Ruby on Rails Ecommerce Engine (Piggybak)](http://www.piggybak.org/). One thing that I found lacking in RailsAdmin is the ability to import data. However, it has come up in the [RailsAdmin Google Group](http://groups.google.com/group/rails_admin) and it may be examined in the future. One problem with developing import functionality is that it's tightly coupled to the data and application logic, so building out generic import functionality may need more thought to allow for elegant extensibility.

For a recent ecommerce project using RailsAdmin and Piggybak, I was required to build out import functionality. The client preferred this method to writing a simple migration to migrate their data from a legacy app to the new app, because this import functionality would be reusable in the future. Here are the steps that I went through to add Import functionality:

### #1: Create Controller

```ruby
class CustomAdminController &lt; RailsAdmin::MainController
  def import
    # TODO
  end
end
```

First, I created a custom admin controller for my application in the app/controllers/ directory that inherits from RailsAdmin::MainController. This RailsAdmin controller has several before filters to set the required RailsAdmin variables, and defines the correct layout.

### #2: Add import route

```ruby
match "/admin/:model_name/import" =&gt; "custom_admin#import" , :as =&gt; "import", :via =&gt; [:get, :post]
mount RailsAdmin::Engine =&gt; '/admin', :as =&gt; 'rails_admin'
```

In my routes file, I introduced a new named route for import to point to the new custom controller. This action will be a get or a post.

### #3: Override Rails Admin View

Next, I copied over the RailsAdmin app/views/rails_admin/_model_links.html.haml view to my application to override RailsAdmin's view. I made the following addition to this file:

```nohighlight
...
- can_import = authorized? :import, abstract_model

...
%li{:class =&gt; (params[:action] == 'import' &amp;&amp; 'active')}= link_to "Import", main_app.import_path(model_name) if can_import
```

With this logic, the Import tab shows only if the user has import access on the model. Note that the named route for the import must be prefixed with "main_app.", because it belongs to the main application and not RailsAdmin.

### #4: CanCan Settings

My application uses [CanCan with RailsAdmin](https://github.com/sferik/rails_admin/wiki/CanCan), so I leveraged CanCan to control which models are importable. The CanCan Ability class (app/models/ability.rb) was updated to contain the following, to allow exclude import on all models, and then allow import on several specific models.

```ruby
if user &amp;&amp; user.is_admin?
  cannot :import, :all
  can :import, [Book, SomeModel1, SomeModel2, SomeModel3]
end
```

I now see an Import tab in the admin:

<img src="/blog/2012/01/19/import-railsadmin/image-0.png" style="border:1px solid #999;"/>

### #5: Create View

Next, I created a view for displaying the import form. Here's a generic example to display the set of fields that can be imported, and the form:

```nohighlight
&lt;h1&gt;Import&lt;/h1&gt;
&lt;h2&gt;Fields&lt;/h2&gt;
&lt;ul&gt;
    &lt;% @abstract_model::IMPORT_FIELDS.each do |attr| -%&gt;
    &lt;li&gt;&lt;%= attr %&gt;&lt;/li&gt;
    &lt;% end -%&gt;
&lt;/ul&gt;

&lt;%= form_tag "/admin/#{@abstract_model.to_param}/import", :multipart =&gt; true do |f| -%&gt;
    &lt;%= file_field_tag :file %&gt;
    &lt;%= submit_tag "Upload", :disable_with =&gt; "Uploading..." %&gt;
&lt;% end -%&gt;
```

This will look something like this:

<img src="/blog/2012/01/19/import-railsadmin/image-1.png" style="border:1px solid #999;"/>

### #6: Import Functionality

Finally, the code for the import looks something like this:

```ruby
def import
  if request.post?
    response = { :errors =&gt; [], :success =&gt; [] }
    file = CSV.new(params[:file].tempfile)

    # Build map of attributes based on first row
    map {}
    file.readline.each_with_index { |key, i| map[key.to_sym] = i }

    file.each do |row|
      # Build hash of attributes
      new_attrs = @abstract_model.model::IMPORT_FIELDS.inject({}) { |hash, a| hash[a] = row[map[a]] if map[a] }

      # Instantiate object
      object = @abstract_model.model.new(new_attrs)

      # Additional special stuff here

      # Save
      if object.save
        response[:success] &lt;&lt; "Created: #{object.title}"
      else
        response[:error] &lt;&lt; "Failed to create: #{object.title}. Errors: #{object.errors.full_messages.join(', ')}."
      end
    end
  end
end
```

Note that a hash of keys and locations is created to map keys to the columns in the imported file. This allows for flexibility in column ordering of imported files. Later, I'd like to to re-examine the CSV documentation to identify if there is a more elegant way to handle this.

### #7: View updates to show errors

Finally, I update my view to show both success and error messages, which looks sorta like this in the view:

<img src="/blog/2012/01/19/import-railsadmin/image-2.png" style="border:1px solid #999;"/>

### Conclusion and Discussion

It was pretty straightforward to get this figured out. The only disadvantage I see to this method is that overriding the rails_admin view requires recopying or manual updates to the view over during upgrades of the gem. For example, if any part of the rails_admin view has changes, those changes must also be applied to the custom view. Everything else should be smooth sailing :)

In reality, my application has several additional complexities, which make it less suitable for generic application:

- Several of the models include attached files via [paperclip](https://github.com/thoughtbot/paperclip). Using open-uri, these files are retrieved and added to the objects.
- Several of the models include relationships to existing models. The import functionality requires lookup of these associated models (e.g. an imported book belongs_to an existing author), and reports and error if the associated objects can not be found.
- Several of the models require creation of a special nested object. This was model specific.
- Because of this model specific behavior, the import method is moved out of the controller into model-specific class methods. For example, CompactDisc.import is different from Book.import which is different from Track.import. Pulling the import into a class method also makes for a skinnier controller here.
