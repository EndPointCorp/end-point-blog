---
author: Gaurav Soni
title: Active Storage.
tags: ruby, rails
gh_issue_number: 1385
---

### Overview
[Active storage](https://github.com/rails/rails/tree/master/activestorage) is the new feature of rails 5.2, that provides functionality to upload files to the cloud like AWS, Google cloud etc. This gem attaches uploading files to the Active Record object. It uploads the file asynchronously by which app server overhead reduces and also doesn’t requires to add a background job explicitly. Active storage by default uses the active job to upload the files.

### Features of Active Storage

<b> Mirror Service:-</b> This service allows synchronization of the file between multiple cloud storage. For example we have storage.yml in the config folder.

```nohighlight
development:
  service: Mirror
  primary: amazon
  mirrors:
    - azure
    - google
```

Mirror Service first upload files to the amazon s3 after that it pushed to the azure and google cloud. when we remove the file then first it remove from the amazon and after that it removes from the azure and google cloud. This service is very helpful when we are migration from one cloud to another cloud.

<b>Direct Uploads:-</b> Active Storage comes javascipt library 'activestorage.js'. By using this library we can upload files from front-end to cloud storage direct. There are some event that is provided by activestorage library is `direct-upload:start` `direct-upload:initialize` `direct-upload:progress ` etc.

<b>Asynchronous Upload</b>:- Active storage uploads file asynchronously to the cloud. It doesn’t require to add any background job to upload files asynchronously. It uses active job to upload files on the cloud.

### Installation

<b> Rails < 5.2 </b>

Add the following to your Gemfile

```nohighlight
gem 'activestorage', github: 'rails/activestorage'
```

In Rails 5.2 active store comes by default.

```nohighlight
rails activestorage:install
```

This generate two tables `active_storage_blobs` and `active_storage_attachments`.

and then run

```nohighlight
rails db:migrate
```

Suppose we have model User and we need to upload the profile picture of that user.

```ruby
  class User < ApplicationRecord
    has_one_attached :profile_picture
  end
```

This `has_one_attached` method maps one to one relationship between the Active Record object and uploaded the file.


let's create a form for the user

```ruby
  <%= form_with model: @user, local: true do |form| %>
    <%= form.label :email %>
    <%= form.text_field :email %>
   
    <%= form.label :password %>
    <%= form.password_field :password %>
    <%= form.password_field :password_confirmation %>
 
    <%= form.file_field :profile_picture %>
 
    <%= form.submit %>
  <% end %>
```  

Create action in users controller is something like

```ruby
  def create
    @user = User.create(user_params)
  end

  private

  def user_params
    params.require(:user).permit(:email, :password, :profile_picture)
  end
```

### AWS configuration

Add following lines to your environment.rb(development/production etc) file

```ruby
config.active_storage.service = :amazon
```

Create storage.yml file in rails's config folder.

```nohighlight
  amazon:
    service: S3
    access_key_id: ENV['access_key_id']
    secret_access_key: ENV['secret_access_key']
```

### Disadvantages

1) It is currently in the beta version.

2) For now it supports only to amazon, google, azure.

You can also see the [Active Storage](http://edgeguides.rubyonrails.org/active_storage_overview.html) doc for more details.
