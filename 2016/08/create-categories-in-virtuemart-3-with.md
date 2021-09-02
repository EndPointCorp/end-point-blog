---
author: Piotr Hankiewicz
title: Create categories in Virtuemart 3 with Joomla 2.5 and 3.5 programmatically
github_issue_number: 1249
tags:
- php
- ecommerce
date: 2016-08-18
---

### Introduction

*Code that I’m going to show you is ready to download here: [https://github.com/peter-hank/com_morevirtuemart](https://github.com/peter-hank/com_morevirtuemart)*

[Virtuemart](https://virtuemart.net/) is an open-source e-commerce application written in PHP. It’s pretty popular with a 4% share of the whole e-commerce market ([https://blog.aheadworks.com/2015/05/ecommerce-platforms-popularity-may-2015-two-platforms-take-half/](https://blog.aheadworks.com/2015/05/ecommerce-platforms-popularity-may-2015-two-platforms-take-half/)). Today I will show you how to extend it and use its functionality from an external [Joomla](https://www.joomla.org) (free and open-source content management system) component.

### Creating a component

We are going to create a new component to show the code in a nice and clear form. I’m using a component generator from here: [https://www.component-creator.com](https://www.component-creator.com). We don’t need any tables, models and views for the purpose of this blog post. Plain and simple component is what we need. After creating the component download it and install in a Joomla administration interface.

### Component overview

The component structure looks like this:

```bash
# tree components/com_morevirtuemart
components/com_morevirtuemart
├── controller.php
├── controllers
│   └── index.html
├── helpers
│   ├── index.html
│   └── morevirtuemart.php
├── index.html
├── models
│   ├── fields
│   │   ├── createdby.php
│   │   ├── filemultiple.php
│   │   ├── foreignkey.php
│   │   ├── index.html
│   │   ├── modifiedby.php
│   │   ├── submit.php
│   │   ├── timecreated.php
│   │   └── timeupdated.php
│   ├── forms
│   │   └── index.html
│   └── index.html
├── morevirtuemart.php
├── router.php
└── views
    └── index.html
```

We don’t need to use more than a generic controller in a main directory. Its content is not very exciting for now:

```php
<?php

// No direct access
defined('_JEXEC') or die;

jimport('joomla.application.component.controller');

/**
 * Class MorevirtuemartController
 *
 * @since  1.6
 */
class MorevirtuemartController extends JControllerLegacy
{
 /**
  * Method to display a view.
  *
  * @param   boolean $cachable  If true, the view output will be cached
  * @param   mixed   $urlparams An array of safe url parameters and their variable types, for valid values see {@link JFilterInput::clean()}.
  *
  * @return  JController   This object to support chaining.
  *
  * @since    1.5
  */
 public function display($cachable = false, $urlparams = false)
 {
  $view = JFactory::getApplication()->input->getCmd('view', '');
  JFactory::getApplication()->input->set('view', $view);

  parent::display($cachable, $urlparams);

  return $this;
 }
}
```

We can remove a display function and replace it with a function called **createCategory** so a MorevirtuemartController class will look like this:

```php
class MorevirtuemartController extends JControllerLegacy
{
 public function createCategory ()
 {
  echo 'I\'m alive!';

  die();
 }
}
```

To test that our component is fully working right now try to open Joomla with this url: **index.php?option=com_morevirtuemart&task=createCategory**. Of course you need to prepend it with your domain name to make it work. The result should be just an empty page with our text: “I’m alive!”

Now you know how to call a controller task within a browser.

### Creating a category

To use Virtuemart classes we need to initialize all of its logic and configuration. Look here:

```php
<?php

// No direct access
defined('_JEXEC') or die;

jimport('joomla.application.component.controller');

// loading Virtuemart classes and configuration
if (!class_exists( 'VmConfig' )) require(JPATH_ADMINISTRATOR . DS . 'components' . DS . 'com_virtuemart'.DS.'helpers'.DS.'config.php');
$config= VmConfig::loadConfig();
if (!class_exists( 'VirtueMartModelVendor' )) require(JPATH_VM_ADMINISTRATOR.DS.'models'.DS.'vendor.php');
if(!class_exists('TableMedias')) require(JPATH_VM_ADMINISTRATOR.DS.'tables'.DS.'medias.php');
if(!class_exists('TableCategories')) require(JPATH_VM_ADMINISTRATOR.DS.'tables'.DS.'categories.php');
if (!class_exists( 'VirtueMartModelCategory' )) require(JPATH_VM_ADMINISTRATOR.DS.'models'.DS.'category.php');

/**
 * Class MorevirtuemartController
 *
 * @since  1.6
 */
class MorevirtuemartController extends JControllerLegacy
{
 public function createCategory ()
 {
  echo 'I\'m alive!';
  die();
 }
}
```

What we are doing here is importing needed Virtuemart classes and initializing the configuration of each. We are all set now and ready for an implementation.

The most difficult thing here is how to work with a Virtuemart internal authorization system. Before an every CRUD action there is a check for an authorization access. We need to find a workaround for this, there are multiple way of doing this, I will show you how I did that. Create a new file in **components/com_morevirtuemart/model and call it category.php.** Inside this file put this piece of code:

```php
<?php

// No direct access
defined('_JEXEC') or die;

class VirtueMartModelCategoryLocal extends VirtueMartModelCategory {
 public function __construct() {
  parent::__construct();
 }
}
```

I hope it’s pretty clear what we are doing here: extending a Virtuemart category model. What I’m going to do now is to copy a store function from a VirtueMartModelCategory class and put it in our local class of a category model and remove an authentication check from it (you need to secure it by yourself but using a different method). The result of this action is:

```php
<?php

// No direct access
defined('_JEXEC') or die;

class VirtueMartModelCategoryLocal extends VirtueMartModelCategory {
  public function __construct()
  {
    parent::__construct();
  }

  public function store(&$data)
  {
    $table = $this->getTable('categories');

    if ( !array_key_exists ('category_template' , $data ) ){
      $data['category_template'] = $data['category_layout'] = $data['category_product_layout'] = 0 ;
    }
    if(VmConfig::get('categorytemplate') == $data['category_template'] ){
      $data['category_template'] = 0;
    }

    if(VmConfig::get('categorylayout') == $data['category_layout']){
      $data['category_layout'] = 0;
    }

    if(VmConfig::get('productlayout') == $data['category_product_layout']){
      $data['category_product_layout'] = 0;
    }

    $table->bindChecknStore($data);

    if(!empty($data['virtuemart_category_id'])){
      $xdata['category_child_id'] = (int)$data['virtuemart_category_id'];
      $xdata['category_parent_id'] = empty($data['category_parent_id'])? 0:(int)$data['category_parent_id'];
      $xdata['ordering'] = empty($data['ordering'])? 0: (int)$data['ordering'];

        $table = $this->getTable('category_categories');

      $table->bindChecknStore($xdata);

    }

    $this->clearCategoryRelatedCaches();

    return $data['virtuemart_category_id'] ;
  }
}
```

In addition, I removed call to media creation. If you need to create media along with the categories you need to extend it as well, the same as we did with a category model. We are all set now to create a new category from a component controller, we just need to include an extended model there and call a **store** function. Our controller should look like this now:

```php
<!--?php

// No direct access
defined('_JEXEC') or die;

jimport('joomla.application.component.controller');

// loading Virtuemart classes and configuration
defined('VMPATH_ROOT') or define('VMPATH_ROOT', JPATH_ROOT);
defined('VMPATH_ADMIN') or define('VMPATH_ADMIN', VMPATH_ROOT.DS.'administrator' . DS . 'components' . DS . 'com_virtuemart');
if (!class_exists( 'VmConfig' )) require(JPATH_ROOT.DS.'administrator' . DS . 'components' . DS . 'com_virtuemart' . DS . 'helpers' . DS . 'config.php');
VmConfig::loadConfig();
if (!class_exists( 'VmController' )) require(VMPATH_ADMIN.DS.'helpers' . DS . 'vmcontroller.php');
if (!class_exists( 'VmModel' )) require(VMPATH_ADMIN.DS.'helpers' . DS . 'vmmodel.php');
require(JPATH_ROOT . DS . 'administrator' . DS . 'components' . DS . 'com_virtuemart' . DS . 'models' . DS . 'category.php');
require(JPATH_ROOT . DS . 'administrator' . DS . 'components' . DS . 'com_virtuemart' . DS . 'models' . DS . 'product.php');
require(JPATH_ROOT . DS . 'administrator' . DS . 'components' . DS . 'com_virtuemart' . DS . 'models' . DS . 'media.php');

// loading an exteneded category model
require(__DIR__ . DS . 'models' . DS . 'category.php');

/**
 * Class MorevirtuemartController
 *
 * @since  1.6
 */
class MorevirtuemartController extends JControllerLegacy
{
 public function __construct()
 {
  parent::__construct();

  $this--->categoryModel = new VirtueMartModelCategoryLocal();
 }

 public function createCategory ()
 {
  $catData = [
   'category_name' => 'Brand new Virtuemart category',
  'category_parent_id' => 0,
   'published' => 0
   ];

  $catId = $this->categoryModel->store($catData);

  echo 'Created a new category';

  die();
 }
}
```

Wow! The new category should be there. There are many more available attributes to be set, we’ve used a needed minimum: category name, its parent and status.

### The end

There are a few things I should mention:

- ensure to add an authentication to your code, you can use a Joomla authentication system,
- be aware that Virtuemart code can change in time so be careful with updates,
- I recommend to use a CLI script for this kind of operations.

Thanks for reading.
