---
author: Steph Skardal
title: 'Rails Ecommerce with Spree: Customizing with Hooks Comments'
github_issue_number: 253
tags:
- rails
- spree
date: 2010-01-13
---

Yesterday, I went through some examples using [hook and theme implementation in Spree](/blog/2010/01/rails-ecommerce-spree-hooks-tutorial), an open source Ruby on Rails ecommerce platform. I decided to follow-up with closing thoughts and comments today.

I only spent a few hours working with the new Spree edge code (Version 0.9.5), but I was relatively happy with the Spree theme and hook implementation, as it does a better job decoupling the extension views with Spree core functionality and views. However, I found several issues that are potential areas for improvement with this release or releases to come.

**Theme too clunky?**

One concern I have is that the entire “views” directory from SPREE_ROOT/app was moved into the theme with this theme-hook work (all of the “V” in MVC). Yesterday, I discussed how WordPress had designed a successful theme and plugin interaction and one thing I mentioned was that a WordPress theme was lightweight and comprised of several customer-facing PHP files (index, single post page, archive pages, search result page). Moving **all** of the Spree core views to the theme presents a couple of issues, in my opinion:

- A developer that jumps into theme development is immediately met with more than 50 files in the theme directory to understand and work with. What you may notice from my tutorial yesterday is that I actually changed the look of Spree through an extension rather than creating a new theme—​I believe there is better separation of my custom design and the Spree core if I included the custom styling in the extension rather than creating a new theme and copying over 50+ files to edit. I’m also more comfortable working with CSS to manipulate the appearance rather than editing and maintaining those files. Now, the next time the Spree core and default template are updated, I don’t have to worry about copying and pasting all the theme files into my custom theme and managing modifications. I think over time, Spree should aim to improve separation of theme views and core views and simplify the theme views.
- The new default Spree includes the admin views. Spree developers and users are probably more interested in changing and modifying customer-facing pages than admin pages. I believe that Spree should focus on developing a strong admin interface and assume that only more advanced developers will need to override the admin views. The admin view would contain a set of predefined core hooks to add tabs and reports. Rather than having a theme with all of the rails views, the theme should be a lightweight collection of files that are likely to be edited by users and the Spree core should include files that are less likely to be modified (and in theory, have an awesome admin interface that would only be extended with additional reports or additional fields for object updates and edits).

**Theme-Hook Decoupling?**

<a href="https://4.bp.blogspot.com/_wWmWqyCEKEs/S0jyUPIJddI/AAAAAAAADBQ/Rg_ZsrAs1XM/s1600-h/spree_building_blocks.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5424852180639774162" src="/blog/2010/01/rails-ecommerce-spree-hooks-comments/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 308px; height: 391px;"/></a>

Extension views or text are hooked through the hooks defined in the theme.

Another big concern I have is the tight coupling between Spree themes and hooks. **All** of the hooks are defined in the Spree theme. If someone were to switch from one theme to another, there is the potential for functionality to be lost if consistency between theme hooks isn’t enforced. This issue piggybacks off of the first issue: I think the Spree core should have control of all the admin views and admin hooks. It would be great to see the views simplified or refactored and allow Spree core to control and instantiate many hooks. I think it’s great to provide the flexibility to instantiate hooks in themes, but I think the core code (admin, especially) should be more **opinionated** and contain its own set of views with hooks that would likely be overridden less frequently.

<a href="https://3.bp.blogspot.com/_wWmWqyCEKEs/S0jzyuuqLpI/AAAAAAAADBY/X59I5QW_3Yo/s1600-h/spree_building_blocks_ideal.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5424853804030504594" src="/blog/2010/01/rails-ecommerce-spree-hooks-comments/image-1.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 202px;"/></a>

A more ideal approach to decouple appearance and functionality would require hooks to be defined in the Spree core.

**Conclusion**

In the tutorial, I also didn’t address extended core functionality with models and controllers in the extensions. The logic discussed the article [Rails Ecommerce Product Optioning in Spree](/blog/2009/12/rails-ecommerce-product-optioning-in) and [Rails Approach for Spree Shopping Cart Customization](/blog/2009/10/rails-approach-to-spree-shopping-cart) should work with some view modifications to use existing hooks instead of overriding core views.

<a href="https://2.bp.blogspot.com/_wWmWqyCEKEs/S0j-TThOmsI/AAAAAAAADBg/gUtsc4sUTdk/s1600-h/image3.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5424865358778374850" src="/blog/2010/01/rails-ecommerce-spree-hooks-comments/image-2.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 148px;"/></a>

A screenshot of the tutorial app in yesterday’s article.

Despite the issues mentioned above, I think that the hook and theme work in the upcoming Spree 0.9.5 release is a big step in the right direction to improve the customization building blocks of Spree. It was mentioned in yesterday’s article that the release hasn’t been made official, but several developers have expressed an interest in working with the code. Hopefully the final kinks of theme and hook implementation will be worked out and the new release will be announced soon. Over time, the hook and theme implementation will advance and more examples and documentation will become available.
