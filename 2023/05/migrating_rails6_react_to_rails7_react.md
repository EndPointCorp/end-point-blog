---
author: "Indra Pranesh Palanisamy"
title: "Migrating Rails 6 React to Rails 7 React"
featured:
  image_url: /blog/2023/03/identifying-vulnerabilities-using-horusec/pexels-indra-pranesh-palanisamy-15837790.webp
description: "In this blog post, we will explore the steps, benefits, and challenges involved in migrating from Rails 6 to Rails 7, specifically focusing on migrating a Rails 6 React application to Rails 7 React. This guide aims to provide valuable insights into the world of Ruby on Rails migration."
date: 2023-05-29
tags:
- ruby-on-rails
- react
- migration
---

![A coconut tree stands in the corner of a serene blue sky](/blog/2023/05/migrating_rails6_react_to_rails7_react/pexels-indra-pranesh-palanisamy-17019134.webp)

<!-- Photo by Indra Pranesh Palanisamy, 2022 -->

CasePointer’s disease reporting portal is built on Rails 6 and React and it's time for an upgrade to Rails 7. This blog post will cover the steps, benefits, and challenges of migrating from Rails 6 to Rails 7, providing valuable insights into the world of Ruby on Rails.

With the recent release of Rails 7, there are many new features and improvements to explore.
One of the biggest changes in Rails 7 is the retirement of Webpacker in favor of using the native webpack for bundling JavaScript.

For those who are not familiar, Webpacker is a Rails gem which is a wrapper around the webpack build system that provides a standard webpack configuration and reasonable defaults.


## Steps for Migrating Rails 6 React to Rails 7 React

To migrate a Rails 6 React application to Rails 7 React, follow these steps:

### 1. Update Rails Gem in Gemfile

In your application's Gemfile, update the Rails gem version to Rails 7:

```ruby
# old
gem "rails", "~> 6.1.4"

# new
gem "rails", "~> 7.0.0"
```

### 2. Upgrade Rails Packages
Upgrade the Rails packages using Yarn:

```shell
yarn upgrade @rails/actioncable --latest
yarn upgrade @rails/activestorage --latest
```

### 3. Run the Rails Update Task
Run the following command to initiate the Rails update task:

```shell
bin/rails app:update
```

This task guides you file by file to integrate the new Rails 7 defaults. Refer to the [Rails documentation](https://guides.rubyonrails.org/upgrading_ruby_on_rails.html) for detailed information on this update task.

### 4. Remove Webpacker
Since Webpacker is no longer the default in Rails 7, follow these steps to remove it:

Remove the webpacker gem from your Gemfile:
```ruby
# Remove the webpacker gem
gem 'webpacker', '~> 4.0'
```

Remove the `webpacker.yml` file and any other related files associated with webpacker.

Run `bundle install` to update the Gemfile.lock:

```shell
bundle install
```
### 5. Setting up Webpack

To set up Webpack for your Rails 7 React application, follow these steps:

Install webpack and other necessary libraries:
```shell
yarn install webpack webpack-cli @babel/core
```

Create a webpack.config.js file at the root of your application:
```javascript
// webpack.config.js

const path = require("path");
const webpack = require("webpack");
// Add other necessary plugins and configurations

module.exports = {
  // Webpack configuration options
  output: {
    // Make sure to use the path of the rails asset pipeline
    path: path.join(__dirname, '/app/assets/builds'),
    ...
  }
  module: {
    rules: [
      // Add CSS/SASS/SCSS rule with loaders
      {
        test: /\.(?:sa|sc|c)ss$/i,
        use: [MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader'],
      },
      {
        test: /\.(png|jpe?g|gif|eot|woff2|woff|ttf|svg)$/i,
        use: 'file-loader',
      },
      { 
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      }
    ],
  },
  ...
};
```

Add a .babelrc file for Babel configuration:
```json
// .babelrc

{
  "presets": ["@babel/preset-env", "@babel/preset-react"]
}
```

Update the scripts section in your package.json:
```json
// package.json

{
  "scripts": {
    "build": "webpack",
    "dev": "webpack --watch"
  }
}
```

### 6. Update Rails Asset Tags
In your application views, update the asset tags from stylesheet_pack_tag and javascript_pack_tag to stylesheet_link_tag and javascript_include_tag, respectively:

```erb
<%= stylesheet_link_tag 'application', media: 'all', 'data-turbolinks-track': 'reload' %>
<%= javascript_include_tag 'application', 'data-turbolinks-track': 'reload' %>
```

### 7. Start the dev server

Start the local development server with,

```
// rails
rails server

// react
yarn run dev
```
<br>

Migrating a Rails 6 React application to Rails 7 React involves several steps, including updating the Rails gem, removing Webpacker, setting up  
Webpack, and updating the asset tags. By following these steps, we can take advantage of the new features and improvements in Rails 7 while 
continuing to leverage the power of React.