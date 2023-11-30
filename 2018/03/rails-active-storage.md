---
author: Gaurav Soni
title: Rails Active Storage
github_issue_number: 1390
tags:
- ruby
- rails
date: 2018-03-12
---

### Overview

[Active Storage](https://github.com/rails/rails/tree/master/activestorage) is a new feature of Ruby on Rails 5.2 that provides functionality to upload files to the cloud, currently Amazon Web Services, Google Cloud, Microsoft Azure.

This gem attaches pointers to uploaded files to the Active Record object. It uploads the file asynchronously which reduces app server overhead, and it also doesn’t require adding a background job explicitly. Active Storage by default uses Active Job to upload the files.

### Features of Active Storage

<b>Mirror Service:</b> This allows synchronization of the file between multiple cloud storage services. For example we have this `config/storage.yml`:

```yaml
development:
  service: Mirror
  primary: amazon
  mirrors:
    - azure
    - google
```

The Mirror service first uploads files to Amazon S3. After that it pushes to Azure and Google Cloud. When we remove the file then first it removes it from Amazon S3 and after that it removes it from Azure and Google Cloud. This service is very helpful when we are migrating from one cloud to another.

<b>Direct Uploads:</b> Active Storage comes with a JavaScript library `activestorage.js`. By using this library we can upload files from the front-end browser to cloud storage directly. Some events that are provided by the activestorage.js library are `direct-upload:start`, `direct-upload:initialize`, and `direct-upload:progress`.

<b>Asynchronous Upload</b>: Active Storage uploads files asynchronously to the cloud. It doesn’t require adding any background job to upload files asynchronously. It uses Active Job to upload files to the cloud.

### Installation

In Rails versions before 5.2, add the following to your Gemfile:

```ruby
gem 'activestorage', github: 'rails/activestorage'
```

In Rails 5.2 active store comes by default.

To install into your application:

```bash
rails activestorage:install
```

This generates two tables `active_storage_blobs` and `active_storage_attachments`.

Then run:

```bash
rails db:migrate
```

Suppose we have model User and we need to upload the profile picture of that user.

```ruby
class User < ApplicationRecord
  has_one_attached :profile_picture
end
```

This `has_one_attached` method maps one to one relationship between the Active Record object and the uploaded file.

Let’s create a form for the user:

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

The create action in the users controller is something like:

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

Add this line to the relevant environment.rb (development/production) file:

```ruby
config.active_storage.service = :amazon
```

Create the `config/storage.yml` file:

```yaml
amazon:
  service: S3
  access_key_id: ENV['access_key_id']
  secret_access_key: ENV['secret_access_key']
```

### Disadvantages

1. Active Storage is currently in beta testing.

2. At the moment it supports only Amazon, Google, and Azure clouds.

You can also see the [Active Storage](http://edgeguides.rubyonrails.org/active_storage_overview.html) overview at Rails Guides for more details.

### Conclusion

For now, Active Storage’s features are very limited as compared with CarrierWave and Paperclip, but it will likely become a popular replacement for CarrierWave or Paperclip in future. Active Storage has the advantage that it doesn’t require any explicit job call when uploading an image asynchronously.

Active Storage supports mini_magick and imagemagick for image transformations, but to perform image resizing or versioning I still recommend CarrierWave because of its rich set of features.
