---
author: Ethan Rowe
gh_issue_number: 231
tags: php
title: Iterative Migration of Legacy Applications to CakePHP
---

As Steph noted, we recently embarked on an adventure with a client who had a legacy PHP app.  The app was initially developed in rapid fashion, with changing business goals along the way.  Some effort was made at the outset with this vanilla PHP app to put key business logic in classes, but as often happens over time the cleanliness of those classes degraded.  While much of the business rules and state management (i.e. database manipulation, session wrangling, authentication/access-control, etc.) were kept separate from the "views" (the PHP entry pages), the classes themselves became tightly coupled, overburdened with myriad responsibilities, etc.

This was a far cry from the stereotypical spaghetti PHP app, but nevertheless it needed some reorganization; all but the smallest changes inevitably required touching a wide range of classes and pages, and the code would only grow more brittle unless some serious refactoring took place.

We determined at the outset that getting the application moved into an established MVC framework would be of great benefit, and further determined that [CakePHP](http://cakephp.org) would be a good choice.  (This is the point where anybody reading will inevitably ask in comments "Why CakePHP instead of My Preferred Awesome Framework?"  *Sigh*.)  The client agreed.  The question became: how do we get there from here?

I spent some time investigating and inevitably came across the well-regarded three-part blog series:

1. [Converting Legacy Apps to CakePHP Part I](http://www.littlehart.net/atthekeyboard/2008/11/27/converting-legacy-apps-to-cakephp-part-1/)
1. [Part II](http://www.littlehart.net/atthekeyboard/2008/12/04/converting-legacy-apps-to-cakephp-part-2/)
1. [Part III](http://www.littlehart.net/atthekeyboard/2008/12/30/converting-legacy-apps-to-cakephp-part-3/)

(The author of that series has a book out on the subject, as well.)

For somebody new to MVC application design, especially in the PHP space, the series (and presumably the related book) probably makes for pretty good reading.  They present a decent approach to how the refactoring of legacy code can be accomplished.  However, the series also appears to operate under the assumption that you're in a scrap-and-rebuild situation: the legacy app can essentially go nowhere for a few weeks while it gets gutted into CakePHP.

As noted in a [review of the related book](http://www.pseudocoder.com/archives/2009/04/08/review-refactoring-legacy-applications-using-cakephp/), the rebuild-it-all assumption doesn't apply to many real world situations.  The more money your application makes, the more users it affects, the larger the feature set, the more likely it is that the business cannot afford to have an application sit in a code freeze while an entire rewrite takes place.

We ultimately opted for a different approach: iteratively migrate to CakePHP.  The simplicity of the basic PHP paradigm makes this remarkably easy.

The basic steps:

1. Rearrange the legacy application so it runs "within" CakePHP, with the CakePHP dispatcher handling the request but ultimately invoking the original legacy view
1. Make adjustments to the legacy code such that it gets its database handle(s) from CakePHP rather than internally, it uses CakePHP's session, etc.
1. New development can proceed within CakePHP; legacy logic can be refactored into CakePHP over time as the opportunity presents itself (or the situation demands)

Getting the application to run within CakePHP in this manner does not require that much effort.  Of course, this would depend on your situation, but in the traditional model of presentation-oriented code relying on some business objects and a database, it works out.  For the initial step:

1. Prepare a basic CakePHP application
1. Pull the legacy code into the CakePHP webroot, with the legacy pages moved under a new legacy/ subdirectory
1. Prepare a "legacy" action in the default PageController that maps the requested URI path to a path relative to the legacy/ directory, then invokes the file living at that path
1. Set up a new catch-all route that invokes this legacy action

After these steps, you have CakePHP fronting your legacy app, but otherwise not doing much else.  A snippet of our code that deals with pulling in a legacy app page in this manner:

```php
function includeLegacyPage($path = null) {
	// map the path passed in or from the request to the legacy/ subdirectory
	$cakeRequestPath = $path ? $path : $this->controller->params['url']['url'];
	$path = WWW_ROOT . 'legacy/' . $cakeRequestPath;

	// This just maps input arguments to globals
	$this->prepareGlobals(array('cakeRequestPath' => $cakeRequestPath));

	// Resolve directories to an index.php page as necessary
	if (is_dir($path)) {
		if(substr($path, -1) != '/')
			$path .= '/';
		$path .= 'index.php';
	}

	if (!file_exists($path)) {
		$this->controller->render('error');
	}

	try {
		// buffer PHP output
		ob_start();

		// this "invokes" the legacy page and gathers its content
		include $path;

		// pull in the buffered content
		$this->controller->output = ob_get_contents();

		// stop output buffering
		ob_end_clean();
	} catch (JackExceptionRedirect $e) {
		// We adjusted the legacy app's redirect functions to throw a custom exception
		// class that we catch here, so we can use CakePHP's native redirection
		$this->controller->redirect($e->location, $e->getCode(), false);
	} catch (Exception $e) {
		// All other errors propagate up
		throw $e;
	}

	$this->controller->autoRender = false;
	$this->controller->autoLayout = false;
}
```

Our PageController's "legacy" action uses the above routine to pull in the legacy page.

The second step, of getting CakePHP to control the session, the database handle, etc., involves some minor hacks.  They don't feel elegant.  They go outside the MVC pattern.  But they provide the crucial glue necessary to put CakePHP in charge.

- Make the controller's session available from a global; adjust legacy code to use it instead of direct use of the PHP session.  This means that CakePHP controls the session configuration.
- Make the CakePHP database handle available from a global as well; adjust your legacy database initialization code so it simply uses the global handle from CakePHP.  Now CakePHP controls your database configuration, and CakePHP and the legacy code will use the same handle in a given request.
- And so on and so forth.

For instance:

```php
App::import('ConnectionManager');
$standard_globals = array(
	'cakeDbh'       => ConnectionManager::getDataSource('default')->connection,
	'cakeSession'   => $this->Session
);

$this->prepareGlobals($standard_globals);
```

Up until now, CakePHP's introduction into the mix hasn't added value.  Having reached this point, however, you're ready to start taking advantage of CakePHP.  From here, we refactored our special "legacy" action logic into a new "LegacyPage" component so any controller/action could use the mechanism.  Then we were able to:

- Refactor legacy user authentication logic to use CakePHP's Auth core component
- Refactor various legacy pages to be fronted by CakePHP controller actions, moving the high-level flow control (input validation, user validation, and associated redirects) out of the legacy page and into the controller.  This simplifies the legacy page (making it more strictly limited to presentation) and puts flow control where it belongs.
- For a new feature involving new data structures, developed a new CakePHP component to implement the business operations, new controllers/actions for aspects of the new functionality, and adjusted some legacy code to get data from the new component rather than original direct database calls or legacy class calls


So, what are the advantages of this approach, versus a slash-and-burn rewrite-it-all approach?


- We get to a point in which we're tangibly benefitting from CakePHP with minimal investment of time/money; contrast that with the potential expense of rewriting the entire application before the business sees any benefit
- While we proceeded in this work, the client was actively developing their legacy system; there was no need for a code freeze, and reconciling their changes with our work was fairly trivial; one git rebase took care of it (though I admittedly missed a couple things during the rebase, which we caught and fixed with some spot-checking).
- No repeating of oneself: by making the entire legacy application available within the context of the target framework, we don't need to spend cycles rewriting existing functionality; the do-it-from-scratch approach would, by contrast, require reimplementation of everything
- We can refactor the legacy code in a prioritized, iterative fashion: refactor the most important stuff first, and the less important stuff later.
- We can partially refactor specific pieces of legacy code, such as removing business/data logic from pages such that legacy pages become more like views in the MVC triad; we're not forced to redo an entire legacy subsystem to improve the code organization
- The legacy work that is solid and doesn't need much refactoring stays put, and is usable from the rest of the CakePHP application


We may well get to the point (in late 2010, perhaps) when all legacy code has been refactored into CakePHP's MVC architecture.  Or perhaps not: the business has to balance competing priorities, and it may ultimately be that some aspects of the legacy code just don't get refactored because they aren't especially broken and the business need simply doesn't come up.  That's part of the beauty here: we don't have to make that decision right now; we can let the real-world priorities make that decision for us over time.

It's easy to imagine an engineer finding this less attractive than a redo-it-in-my-favorite-framework-du-jour approach.  It reeks of compromise.  Yet, from a business standpoint the advantages are hard to dispute.  From a technical standpoint, they're hard to dispute as well: faster, shorter cycles of development bring a higher likelihood of success, particularly for small teams (or lone individuals); the management of change is much simpler with iterative design; the iterative approach is arguably less prone to second-system effect than is a rewrite; etc.

This asks more of the engineer than does a ground-up rewrite in Framework X.  So many modern frameworks positively shine with possibility; the engineer lusts for the opportunity to Do It Right, and falls prey to the fallacy that the framework will solve all their problems given that Done Right investment.  But, whatever the features and community offerings may be, modern frameworks ultimately help us organize our code better; better organization of code is amongst the most obvious benefits one gets in moving into a modern framework.

The iterative approach gets us there with far less risk and, in many cases, far more naturally than does the rewrite-it-all approach, but it asks us to have the patience to move in small steps.  It asks that we have the mental room and rigor to envision what the Done Right system might look like, as well as a long chain of interim steps taking us from here to there.  But it delivers value much faster, at lower risk, at lower cost, and crucially, reduces redundant work and gives us the opportunity to change direction as we go.  Consequently, for many -- even most -- business situations the iterative transformation *is* the system Done Right.
