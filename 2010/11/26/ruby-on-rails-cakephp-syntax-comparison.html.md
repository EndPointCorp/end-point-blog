---
author: Steph Skardal
gh_issue_number: 384
tags: php, ecommerce, ruby, rails
title: 'Ruby on Rails versus CakePHP: A Syntax Comparison Guide'
---

My time is typically split between [Interchange](http://www.icdevgroup.com/i/dev) and [Spree](https://spreecommerce.org/) development, but in a recent project for [JackThreads](https://www.jackthreads.com/), I jumped back into CakePHP code. CakePHP is one of the more popular PHP MVC frameworks and is inspired by Rails. I decided to put together a quick syntax comparison guide between CakePHP and Rails since I occasionally have to look up how to do some Rails-y thing in CakePHP.

<table cellpadding="5" cellspacing="0" class="phprails" width="100%"><tbody><tr class="alt">   <th align="center" valign="middle"><h3>Basic</h3></th>   <td align="center" style="width: 43%;" valign="middle">Ruby on Rails</td>   <td align="center" style="width: 43%;" valign="middle">CakePHP</td> </tr>
<tr>   <td align="center" valign="top">MVC Code Inclusion</td>   <td valign="top"> Rails is typically installed as a gem and source code lives in the user’s gem library. In theory, a modified version of the Rails source code can be “frozen” to your application, but I would guess this is pretty rare.   </td>   <td valign="top"> CakePHP is typically installed in the application directory in a “cake/” directory. The “app/” directory contains application specific code. From my experience, this organization has allowed me to easily debug CakePHP objects, but didn’t do much more for me.   </td> </tr>
<tr>   <td align="center" valign="middle">Application Directory Structure</td>   <td valign="top"> <pre class="brush:plain gutter: false">app/
  controllers/ models/ views/ helpers/
lib/
config/
public
  javascripts/ images/ stylesheets/
vendors/
  plugins/ extensions/
</pre></td>   <td valign="top"> <pre class="brush:plain gutter:false">controllers/
models/
views/
  layouts/ elements/ ...
config/
webroot/
tmp/
plugins/
vendors/
</pre></td> </tr>
<tr class="notes">   <td align="center">Notes:</td>   <td colspan="2">     In Rails, layouts live in app/views/layouts/. In CakePHP, layouts live in views/layouts/ and helpers lie in views/helpers/.   </td> </tr>
<tr>   <td valign="middle">Creating an Application</td>   <td valign="top"> <pre class="brush:plain gutter:false">rails new my_app # Rails 3 after gem installation
rails my_app # Rails <3
</pre>
</td>
  <td valign="top">Download the compressed source code and create an application with the recommended directory structure.   </td>
</tr>
<tr class="alt">
  <th valign="top"><h3>Models</h3></th>
  <td align="center" valign="middle">Ruby on Rails</td>
  <td align="center" valign="middle">CakePHP</td>
</tr>
<tr>
  <td align="center" style="padding-top: 30px;" valign="top">Validation</td>
  <td valign="top"> <pre class="brush:ruby gutter:false">class Zone < ActiveRecord::Base
  validates_presence_of :name
  validates_uniqueness_of :name
end
</pre>
</td>
  <td valign="top"> <pre class="brush:php gutter:false">class User extends AppModel {
  var $name = 'User';
  var $validate = array(
    'email' => array(
      'email-create' => array(
        'rule' => 'email',
        'message' => 'Invalid e-mail.',
        'required' => true,
        'on' => 'create'
      )
    )
  );
}
</pre></td>
</tr>
<tr>
  <td align="center" style="padding-top: 30px;" valign="top">Relationships</td>
  <td valign="top"> <pre class="brush:ruby gutter:false">class Order < ActiveRecord::Base
  belongs_to :user
  has_many :line_items
end
</pre>
</td>
  <td valign="top"> <pre class="brush:php gutter:false">class Invite extends AppModel {
  var $name = 'Invite';
  var $belongsTo = 'User';
  var $hasMany = 'Campaigns';
}
</pre></td>
</tr>
<tr>
  <td align="center" style="padding-top: 30px;" valign="top">Special Relationships</td>
  <td valign="top"> <pre class="brush:ruby gutter:false">class Address < ActiveRecord::Base
  has_many :billing_checkouts,
    :foreign_key => "bill_address_id",
    :class_name => "Checkout"
end
</pre></td>
  <td valign="top"> <pre class="brush:php gutter:false">class Foo extends AppModel {
  var $name = 'Foo';
  var $hasMany = array(
    'SpecialEntity' => array(
      'className' => 'SpecialEntity',
      'foreignKey' => 'entity_id',
      'conditions' =>
  array('Special.entity_class' => 'Foo'),
      'dependent' => true
    ),
  );
}
</pre></td>
</tr>
<tr class="alt">
  <th valign="top"><h3>Controllers</h3></th>
  <td align="center" valign="middle">Ruby on Rails</td>
  <td align="center" valign="middle">CakePHP</td>
</tr>
<tr>
  <td align="center" valign="middle">Basic Syntax</td>
  <td valign="top"> <pre class="brush:ruby gutter:false">class FoosController < ActionController::Base
  helper :taxons
  actions :show, :index

  include Spree::Search

  layout 'special'
end
</pre>
</td>
  <td valign="top"> <pre class="brush:php gutter:false">class FooController extends AppController {
  var $name = 'Foo';
  var $helpers = array('Server', 'Cart');
  var $uses = array('SpecialEntity','User');
  var $components = array('Thing1', 'Thing2');
  var $layout = 'standard';
}
</pre></td>
</tr><tr class="notes">
  <td align="center">Notes:</td>
  <td colspan="2"> CakePHP and Rails use similar helper and layout declarations. In CakePHP, the $uses array initiates required models to be used in the controller, while in Rails all application models are available without an explicit include. In CakePHP, the $components array initiates required classes to be used in the controller, while in Rails you will use “include ClassName” to include a module.   </td>
</tr>
<tr>
  <td align="center" style="padding-top: 30px" valign="top">Filters</td>
  <td valign="top"> <pre class="brush:ruby gutter:false">class FoosController < ActionController::Base
  before_filter :load_data, :only => :show
end
</pre></td>
  <td valign="top"> <pre class="brush:php gutter:false">class FooController extends AppController {
  var $name = 'Foo';

  function beforeFilter() {
    parent::beforeFilter();
    //do stuff
  }
}
</pre></td>
</tr>
<tr>
  <td align="center" style="padding-top:30px;" valign="top">Setting View Variables</td>
  <td valign="top"> <pre class="brush:ruby gutter:false">class FoosController < ActionController::Base
  def index
    @special_title = 'This is the Special Title!'
  end
end
</pre>
</td>
  <td valign="top"> <pre class="brush:php gutter:false">class FooController extends AppController {
  var $name = 'Foo';

  function index() {
    $this->set('title',
      'This is the Special Title!');
  }
}
</pre></td>
</tr>
<tr class="alt">
  <th valign="middle"><h3>Views</h3></th>
  <td align="center" valign="middle">Ruby on Rails</td>
  <td align="center" valign="middle">CakePHP</td>
</tr>
<tr>
  <td align="center" valign="middle">Variable Display</td>
  <td valign="top"> <pre class="brush:plain gutter:false"><%= @special_title %>
</pre></td>
  <td valign="top"> <pre class="brush:plain gutter:false"><?= $special_title ?>
</pre></td>
</tr>
<tr>
  <td align="center" valign="middle">Looping</td>
  <td valign="top"> <pre class="brush:plain gutter:false"><% @foos.each do |foo| -%>
<%= foo.name %>
<% end -%>
</pre></td>
  <td valign="top"> <pre class="brush:plain gutter:false"><?php foreach($items as $item): ?>
<?= $item['name']; ?>
<?php endforeach; ?>
</pre></td>
</tr>
<tr>
  <td align="center" valign="middle">Partial Views or Elements</td>
  <td valign="top"> <pre class="brush:plain gutter:false"><%= render :partial => 'shared/view_name',
  :locals => { :b => "abc" } %>
</pre></td>
  <td valign="top"> <pre class="brush:php gutter:false"><?php echo $this->element('account_menu',
  array('page_type' => 'contact')); ?>
</pre></td>
</tr>
<tr class="notes">
  <td align="center">Notes:</td>
  <td colspan="2">     In Rails, partial views typically can live anywhere in the app/views directory. A shared view will typically be seen in the app/views/shared/ directory and a model specific partial view will be seen in the app/views/model_name/ directory. In CakePHP, partial views are referred to as elements and live in the views/elements directory.   </td>
</tr>
<tr>
  <td align="center" valign="middle">CSS and JS</td>
  <td valign="top"> <pre class="brush:plain gutter:false"><%= javascript_include_tag
  'my_javascript',
  'my_javascript2' %>
<%= stylesheet_link_tag
  'my_style' %>
</pre></td>
  <td valign="top"> <pre class="brush:php gutter:false"><?php
  $html->css(array('my_style.css'),
    null, array(), false);
  $javascript->link(array('my_javascript.js'),
    false);
?>
</pre></td>
</tr>
<tr class="alt">
  <th valign="middle"><h3>Routing</h3></th>
  <td align="center" valign="middle">Ruby on Rails</td>
  <td align="center" valign="middle">CakePHP</td>
</tr>
<tr>
  <td align="center" valign="middle">Basic</td>
  <td valign="top"> <pre class="brush:ruby gutter:false"># Rails 3
match '/cart',
  :to => 'orders#edit',
  :via => :get,
  :as => :cart
# Rails <3
map.login '/login',
  :controller => 'user_sessions',
  :action => 'new'
</pre></td>
<td> <pre class="brush:php gutter:false">Router::connect('/refer',
  array('controller' => 'invites',
        'action' => 'refer'));
Router::connect('/sales/:sale_id',
  array('controller' => 'sale',
        'action' => 'show'),
  array('sale_id' => '[0-9]+'));
</pre></td>
</tr>
<tr>
  <td align="center" valign="middle">Nested or Namespace Routing</td>
  <td valign="top"> <pre class="brush:ruby gutter:false"># Rails 3
namespace :admin do
  resources :foos do
    collection do
      get :revenue
      get :profit
    end
  end
end

# Rails <3
map.namespace :admin do |admin|
  admin.resources :foos, :collection => {
    :revenue            => :get,
    :profit             => :get,
  }
end
</pre></td>
<td valign="top">-</td>
</tr>
<tr class="alt">
  <th valign="middle"><h3>Logging</h3></th>
  <td align="center" valign="middle">Ruby on Rails</td>
  <td align="center" valign="middle">CakePHP</td>
</tr>
<tr>
  <td align="center" valign="middle">Where to?</td>
  <td valign="top">tmp/log/production.log or tmp/log/debug.log   </td>
  <td valign="top">tmp/logs/debug.log or tmp/logs/error.log</td>
</tr>
<tr>
  <td align="center" valign="middle">Logging Syntax</td>
  <td valign="top"> <pre class="brush:ruby gutter:false">Rails.logger.warn "steph!" # Rails 3
logger.warn "steph!" # Rails <3
</pre>
or
<pre class="brush:ruby gutter:false">RAILS_DEFAULT_LOGGER.warn "steph!"
</pre></td>
  <td valign="top"><pre class="brush:php gutter:false">$this->log('steph!', LOG_DEBUG);</pre></td>
</tr>
</tbody></table>

If you are looking for guidance on choosing one of these technologies, below are common arguments. In End Point’s case, we choose whatever technology makes the most sense for the client. We implemented a nifty solution for JackThreads to avoid a complete rewrite, described [here](/blog/2009/12/03/iterative-migration-of-legacy) in detail. We also work with existing open source ecommerce platforms such as [Interchange](http://www.icdevgroup.com/i/dev) and [Spree](https://www.spreecommerce.org/) and try to choose the best fit for each client.

<table cellpadding="5" cellspacing="0" class="phprails" width="100%"><tbody><tr class="alt">   <th valign="middle" width="10%"><h3>Pick Me!</h3></th>   <td align="center" valign="middle" width="45%">Ruby on Rails</td>   <td align="center" valign="middle" width="45%">CakePHP</td> </tr>
<tr>   <td></td>   <td valign="top">     <ul><li>Ruby is prettier than PHP.</li>
<li>Rails Object Oriented Programming implementation is more elegant than in CakePHP.</li>
<li>Rails routing is far superior to CakePHP routing.</li>
<li>Deployment and writing migrations are simpler with built in or peripheral tools.</li>
<li>Documentation of Rails is better than CakePHP.</li>
</ul></td>   <td valign="top">     <ul><li>CakePHP has better performance than Rails. <b>UPDATE:</b> This appears to be a rumor. Benchmark data suggests that Rails performs better than CakePHP.</li>
<li>PHP is supported on hosting providers better than Rails.</li>
<li>PHP developers are typically less expensive than Ruby/Rails developers.</li>
</ul></td> </tr>
</tbody></table>
