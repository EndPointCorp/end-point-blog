---
author: Sean Schofield
title: Acts As Xapian — It Just Works
github_issue_number: 50
tags:
- rails
- search
date: 2008-08-26
---

I just recently started listening to the podcast done by the guys at [RailsEnvy](https://web.archive.org/web/20080906094739/http://railsenvy.com/). It’s an excellent resource for keeping up on what’s new in the Rails world and it’s how I found out about the new [acts_as_xapian](https://github.com/frabcus/acts_as_xapian/wikis) search plugin for Rails. The podcast mentioned this [blog post](https://web.archive.org/web/20080902205324/http://locomotivation.com/2008/07/15/mulling-over-our-ruby-on-rails-full-text-search-options) which contains a very thorough rundown of all the different full-text search options currently available for rails. The timing of this article couldn’t have been better since I was in the market for a new solution.

I was approaching a deadline on a client project here at End Point and I was having lots of trouble with my existing search solution which was [acts_as_ferret](https://github.com/jkraemer/acts_as_ferret/). Setting up ferret was relatively easy and I was very impressed with the [Lucene syntax](https://web.archive.org/web/20080913093502/http://lucene.apache.org/java/docs/queryparsersyntax.html) that it supported. It seemed like a perfect a solution at first but then came “the troubles.”

Ferret is extremely fragile. The slightest problem and your server will just crash. What was causing the crash? Unfortunately the server logs won’t give you much help there. You will receive some cryptic message coming from the C++ library if you’re lucky. Note that I skipped the suggested Drb server setup since this was a development box.

After a while I would notice something wrong in my model code that might have caused an error while updating the search index. Unfortunately this was impossible to verify since I could not predictably reproduce the error. So in the end, I think there may have been issues with my model fields but ferret was of no help in tracking these problems down. The final straw came when the client started testing and almost immediately crashed the server after doing a search.

Enter acts_as_xapian. Jim Mulholland’s excellent [tutorial](https://web.archive.org/web/20080826095829/http://locomotivation.com/2008/07/23/simple-ruby-on-rails-full-text-search-using-xapian) was pretty much all I needed to get it up and running on my Mac. Documentation for acts_as_xapian is a bit thin. It consists primarily of the afore mentioned tutorial and a very detailed [README](https://github.com/frabcus/acts_as_xapian/tree/master/README.txt). The mailing list is starting to become more active, however, and you are likely to get a response there to any thoughtful questions you might have.

One major difference with xapian (vs. ferret) is that it does not rebuild your index automatically with each model update. When you modify an ActiveRecord instance it will update the acts_as_xapian_jobs table with the id and model type of your record so that the index can be updated later. The index is then updated via a rake command that you can easily schedule via cron. You can also rebuild the entire index using a different rake command but that shouldn’t really be necessary.

I was a bit concerned about the lack of a continuously updated index but I came to realize that it has some significant advantages. The biggest advantage is that it’s much faster to update your model records since you are not waiting for the re-indexing to complete on the same thread. It also means you can skip the step of setting up a separate Drb server for ferret in your production environment.

With xapian you can index “related fields” in other models by constructing a pseudo-attribute in your model that returns the value of the associated model as a text string. Ferret allows you to do this as well, but unlike ferret, xapian gives excellent feedback about any mistakes you might have made while constructing them. If you have a nil exception somewhere in one of these related fields, xapian will complain and tell you exactly what line it’s bombing out.

I was also able to setup paging for my search results with [paginating_find](https://web.archive.org/web/20080915144208/http://cardboardrocket.com/pages/paginating_find) which I prefer to [will_paginate](https://github.com/mislav/will_paginate/wikis) (just a personal preference—​nothing wrong with will_paginate). There is also a cool feature that will suggest other possible terms (“Did you mean?”) if your search returns no results. So far the only disappointment has been the lack of an obvious way to do searches on specific fields.

If you are in the market for a new full-text search solution for Rails, you should really give xapian a try.
