---
author: Steph Skardal
title: Using The Security Component and validatePost in CakePHP Gotcha
github_issue_number: 228
tags:
- php
date: 2009-12-02
---

Recently, [Ron](/team/ron-phipps), Ethan, and I worked on a [JackThreads](https://www.jackthreads.com/) project. We are in the process of moving JackThreads’ legacy PHP application to the CakePHP framework in addition to introducing new functionality for this project.

Several of the pages require secure requests:

- the home page (where users log in or create accounts)
- the login page
- the "invite" page (where users create an account)
- the checkout page

We referred to [this article](https://web.archive.org/web/20090515232941/techno-geeks.org/2009/03/using-the-security-component-in-cakephp-for-ssl) that discusses using the security component in CakePHP. Although this article covered the basics, we extended the concepts of the article by creating a CakePHP component with the custom security functionality to force a secure request and includes query string parameters. Below are the contents of the component that was created:

```php
class StephsSecurityComponent extends Object {
    var $components = array('Security');
    function forceSecure($args) {
        $this->Security->blackHoleCallback = 'forceSSL';
        $this->Security->requireSecure($args);
    }
    function forceSSL($controller) {
        $redirect_location = 'https://'.HTTPS_HOST.$controller->here;
        $params = $controller->params['url'];
        unset($params['url']);
        if(count($params) > 0)
        {
            $param_string = '';
            foreach($params as $key => $value)
                $param_string .= '&'.$key.'='.$value;
            $param_string = preg_replace('/^\&/', '?', $param_string);
            $redirect_location .= $param_string;
        }
        $controller->redirect($redirect_location);
    }
}
```

This design required the following definition in the application’s app_controller:

```php
function forceSSL() {
    $this->StephsSecurity->forceSSL($this);
}
```

And any controller that required an action to be secure would call the forceSecure function in the beforeFilter:

```php
function beforeFilter() {
    $this->StephsSecurity->forceSecure('my_action');
}
```

For the most part, the security redirect worked as expected. The before filter in each controller correctly registered the action that required a secure request, and logging statements in the CakePHP core security component verified that the secure component would call the blackHoleCallback if the request was not secure. But then, we came across a bug!

<a href="https://www.flickr.com/photos/deadmike/4070259901/in/pool-ccbugs" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5410713644068329970" src="/blog/2009/12/using-security-component-and/image-0.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 320px; height: 214px;"/></a>

One of the controllers that included this new functionality was not working as expected. The controller had two actions; both actions accepted inputs from forms and **did stuff** with those forms, only one of the actions required the force secure, one of the actions received form inputs from the [CakePHP form helper](https://web.archive.org/web/20091220200812/http://book.cakephp.org/view/182/Form) and the other action received inputs from a legacy PHP page. The action that received inputs from a legacy PHP page didn’t **do stuff** correctly. Below is a simplified version of this controller:

```php
class ThisController extends AppController {
   ...
    var $uses = array('Security', 'StephsSecurity');
    function beforeFilter() {
        $this->StephsSecurity->forceSecure('action_one');
    }
    function action_one() {
        //receives inputs from a cakephp form helper
        //do stuff with $this->params
    }
    function action_two() {
        //receives inputs from a legacy php page
        //do stuff with $this->params -- FAIL
    }
}
```

We added debugging and found that $this->params (or the form parameters) to action_two was empty. We added logging to the beforeFilter to determine if the parameters were deleted during the beforeFilter process. We found that the parameters were present at the conclusion of the beforeFilter. So, at some point in between the beforeFilter and before the action, our form parameters were deleted.

```php
function beforeFilter() {
    $this->log($this->params, LOG_DEBUG);
    //some other unrelated before filtering
    $this->log($this->params, LOG_DEBUG);
    $this->StephsSecurity->forceSecure('action_one');
    $this->log($this->params, LOG_DEBUG);   //parameters looked ok here!
}
```

After more troubleshooting, we determined that if the CakePHP core Security component wasn’t included in the controller, the parameters were not deleted and the action **did it’s stuff**. A review of the CakePHP core Security component revealed that the component performs a validation on posts, which includes a check for a Token input. Because the post to this action originated from a legacy PHP page, it did not include any special hidden form variables included with the use of the CakePHP form helper (much like the Token inputs included via the Rails form helper):

```nohighlight
<input type="hidden" value="POST" name="_method"/>
<input type="hidden" id="Token123123123 value="123123123131231231223" name="data[_Token][key]"/>
```

As a result, the black hole security redirect was called before action_two was reached, then action_two was called with missing parameters. Ethan realized there was a simple fix to this post validation failure. The Security->validatePost variable was set to false inside the controller’s beforeFilter to bypass the _validatePost check in the security component. No more post validation produced expected action_two behavior.

```php
function beforeFilter() {
    $this->Security->validatePost = false;
    $this->StephsSecurity->forceSecure('index');
}
```

Unfortunately, there isn’t a lot of documentation on the [CakePHP Security component](https://web.archive.org/web/20091228191339/http://book.cakephp.org/view/324/The-Security-Component) that would have helped us identify this issue quickly. Configuration of the CakePHP Security component, discussed [here](https://web.archive.org/web/20091220201430/http://book.cakephp.org/view/257/Configuration), fails to mention the validatePost value, but it is included in the [CakePHP API documentation](https://web.archive.org/web/20091103002422/http://api.cakephp.org/file/cake/libs/controller/components/security.php).

Fortunately, it wasn’t too difficult to troubleshoot once we observed the undesired behavior originated from the inclusion of the Security component in the controller. We are now aware of this Security post validation as we continue to transition legacy PHP to CakePHP.  I’m sure we’ll come across situations where data is passed from legacy pages or 3rd party services that do not contain the required Token variables and will require bypassing the _validatePost check.
