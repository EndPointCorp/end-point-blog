---
author: Steph Skardal
gh_issue_number: 549
tags: database, piggybak, rails
title: 'RailsAdmin Import: Part 2'
---

I recently wrote about [importing data in RailsAdmin](/blog/2012/01/19/import-railsadmin). [RailsAdmin](https://github.com/sferik/rails_admin) is a Rails engine that provides a nice admin interface for managing your data, which comes packed with configuration options.

In a recent Ruby on Rails ecommerce project, I’ve been using RailsAdmin, [Piggybak (a Rails ecommerce gem supported by End Point)](https://github.com/piggybak/piggybak), and have been building out custom front-end features such as advanced search and downloadable product support. When this client came to End Point with the project, we offered several options for handling data migration from a legacy system to the new Rails application:

1. Create a standard migration file, which migrates data from the existing legacy database to the new data architecture. The advantage with this method is that it requires virtually no manual interaction for the migration process. The disadvantage with this is that it’s basically a one-off solution and would never be useful again.
2. Have the client manually enter data. This was a reasonable solution for several of the models that required 10 or less entries, but not feasible for the tables containing thousands of entries.
3. Develop import functionality to plug into RailsAdmin which imports from CSV files. The advantage to this method is that it could be reused in the future. The disadvantage with ths method is that data exported from the legacy system would have to be cleaned up and formatted for import.

The client preferred option #3. Using [a quick script for generating custom actions for RailsAdmin](https://github.com/sferik/rails_admin/wiki/Custom-action), I developed a new gem called rails_admin_import to handle import that could be plugged into RailsAdmin. Below are some technical details on the generic import solution.

<img border="0" src="/blog/2012/02/01/railsadmin-import-part-2/image-0.png" width="750"/>

### ActiveSupport::Concern

Using [ActiveSupport::Concern](http://www.fakingfantastic.com/2010/09/20/concerning-yourself-with-active-support-concern/), the rails_admin_import gem extends ActiveRecord::Base to add the following class methods:

- import_fields: Returns an array of fields that will be included in the import, excluding :id, :created_at, and :updated_at, belongs_to fields, and file fields.
- belongs_to_fields: Returns an array of fields with belongs_to relationships to other models.
- many_to_many_fields: Returns an array of fields with has_and_belongs_to_many relationships to other models.
- file_fields: Returns an array of fields that represent data for [Paperclip](https://github.com/thoughtbot/paperclip) attached files.
- run_import: Method for running the actual import, receives request params.

And the following instance methods:

- import_files: sets attached files for object
- import_belongs_to_data: sets belongs_to associated data for object
- import_many_to_many_data: sets many_to_many associated data for object

The general approach here is that the import of files, belongs_to, many_to_many relationships, and standard fields makes up the import process for a single object. The run_import method collects success and failure messages for each object import attempt and those results are presented to the user. A regular [ActiveRecord](http://api.rubyonrails.org/classes/ActiveRecord/Base.html) save method is called on the object, so the existing validation of objects during each save applies.

### Working with Associated Data

One of the tricky parts here is how to handle import of fields representing associations. Given a user model that belongs to a state, country, and has many roles, how would one decide what state, country, or role value to include in the import?

<img border="0" height="167" src="/blog/2012/02/01/railsadmin-import-part-2/image-1.png" width="400"/>

I’ve solved this by including a dropdown to select the attribute used for mapping in the form. Each of the dropdowns contains a list of model attributes that are used for association mapping. A user can then select the associated mappings when they upload a file. In a real-life situation, I may import the state data via abbreviation, country via display name (e.g. “United States”, “Canada”) and role via the role name (e.g. “admin”). My data import file might look like this:

<table cellpadding="0" cellspacing="0" style="border:1px solid #999;" width="100%">
<tbody><tr>
<td>name</td>
<td>email</td>
<td>favorite_color</td>
<td>state</td>
<td>country</td>
<td>role</td>
</tr>
<tr>
<td>Steph Skardal</td>
<td>steph@endpoint.com</td>
<td>blue</td>
<td>CO</td>
<td>United States</td>
<td>admin</td>
</tr>
<tr>
<td>Aleks Skardal</td>
<td>aleksskardal@gmail.com</td>
<td>green</td>
<td></td>
<td>Norway</td>
<td>user</td>
</tr>
<tr>
<td>Roger Skardal</td>
<td>roger@gmail.com</td>
<td>tennis ball yellow</td>
<td>UT</td>
<td>United States</td>
<td>dog</td>
</tr>
<tr>
<td>Milton Skardal</td>
<td>milton@gmail.com</td>
<td>kibble brown</td>
<td>UT</td>
<td>United States</td>
<td>dog</td>
</tr>
</tbody></table>

### Many to Many Relationships

Many to many relationships are handled by allowing multiple columns in the CSV to correspond to the imported data. For example, there may be two columns for role on the user import, where users may be assigned to multiple roles. This may not be suitable for data with a large number of many to many assignments.

### Import of File Fields

In this scenario, I’ve chosen to use open-uri to request existing files from a URL. The CSV must contain the URL for that file to be imported. The import process downloads the file and attaches it to the imported object.

```ruby
self.class.file_fields.each do |key|
  if map[key] && !row[map[key]].nil?
    begin
      row[map[key]] = row[map[key]].gsub(/\s+/, "")
      format = row[map[key]].match(/[a-z0-9]+$/)
      open("#{Rails.root}/tmp/uploads/#{self.permalink}.#{format}", 'wb') { |file| file << open(row[map[key]]).read }
      self.send("#{key}=", File.open("#{Rails.root}/tmp/uploads/#{self.permalink}.#{format}"))
    rescue Exception => e
      self.errors.add(:base, "Import error: #{e.inspect}")
    end
  end
end
```

If the file request fails, an error is added to the object and presented to the user. This method may not be suitable for handling files that do not currently exist on a web server, but it was suitable for migrating a legacy application.

### Configuration: Display

Following RailsAdmin’s example for setting configurations, I’ve added the ability to allow the import display to be set for each model.

```ruby
config.model User do
  label :name
end
```

The above configuration will yield success and error messages with the user.name, e.g.:

<img border="0" height="244" src="/blog/2012/02/01/railsadmin-import-part-2/image-2.png" width="400"/>

### Configuration: Excluded Fields

In addition to allowing a configurable display option, I’ve added the configuration for excluding fields.

```ruby
config.model User do
  excluded_fields do
    [:reset_password_token, :reset_password_sent_at, :remember_created_at,
      :sign_in_count, :current_sign_in_at, :last_sign_in_at, :current_sign_in_ip,
      :last_sign_in_ip]
  end
end
```

The above configuration will exclude the specified fields during the import, and they will not display on the import page.

### Configuration: Additional Fields and Additional Processing

Another piece of functionality that I found necessary for various imports was to hook in additional import functionality. Any model can have an instance method **before_import_save** that accepts the row of CSV data and map of CSV keys to perform additional tasks. For example:

```ruby
def before_import_save(row, map)
  self.created_nested_items(row, map)
end
```

The above method will create nested items during the import process. This simple extensibility allows for additional data to be handled upon import outside the realm of has_and_belongs_to and belongs_to relationships.

Fields for additional nested data can be defined with the extra_fields configuration, and are shown on the import page.

```ruby
config.model User do
  extra_fields do
    [:field1, :field2, :field3, :field4]
  end
end
```

### Hooking into RailsAdmin

As I mentioned above, I used a script to generate this Engine. Using RailsAdmin configurable actions, import must be added as an action:

```ruby
config.actions do
  dashboard
  index
  ...
  import
end
```

And [CanCan](https://github.com/ryanb/cancan) settings must be updated to allow for import if applicable, e.g.:

```ruby
cannot :import, :all
can :import, User
```

### Conclusion

My goal in developing this tool was to produce reusable functionality that could easily be applied to multiple models with different import needs, and to use this tool across Rails applications. I’ve already used this gem in another Rails 3.1 project to quickly import data that would otherwise be difficult to deal with manually. The combination of association mapping and configurability produces a flexibility that encourages reusability.

Feel free to review or check out the code [here](https://github.com/stephskardal/rails_admin_import).
