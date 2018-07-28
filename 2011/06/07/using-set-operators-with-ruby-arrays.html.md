---
author: Mike Farmer
gh_issue_number: 466
tags: ruby, rails
title: Using Set Operators with Ruby Arrays
---

The Array class in Ruby has many methods that are extremely useful. I frequently find myself going to the [RDoc](https://ruby-doc.org/core-2.5.1/Array.html) just to review the different methods and keeping myself up-to-speed on what options are available for manipulating my data using the native methods. Often, I find that there is already a method that exists that can simplify a big chunk of code that I wrote that was confusing and complex.

In a recent project, I needed a way to handle a complex user interface problem that was caused by a many-to-many (has-and-belongs-to-many) database model. The solution that I came up with was an amazingly simple implementation for a problem that could have involved writing some very convoluted and complex algorithms that would have muddied my code and required me to write extensive tests. As it turns out, I had just read up on Array set operators (Ruby methods) and the solution became easier and monumentally more eloquent.

#### Introducing the Union, Difference, and Intersection

Since Arrays essentially act as a set[1], they can be manipulated using the set operations union, difference, and intersection. If you go do the Array rdoc, however, you’ll notice no methods with these names. So here is a brief look at how they work:

#### Union

A union is essentially used to combine the unique values of two sets, or in this case, arrays. To perform a union on two arrays you use the pipe as an operator. For example:

```ruby
[1, 2, 1, 2, 3] | [1, 2, 3, 4] #=> [1, 2, 3, 4]
```

#### Difference

Sometimes you just want to know what is different between two arrays. You can do this by using the difference method as an operator like so:

```ruby
[1, 2, 3] - [3, 4, 5] #=> [1, 2]
```

Now, that may not have been exactly what you were expecting. Difference works by taking the elements on the left and comparing them to the elements on the right. Whatever is different in the left is what’s returned. So the opposite of the above example looks like this:

```ruby
[3, 4, 5] - [1, 2, 3] #=> [4, 5]
```

This subtle difference will be the key in the example I’m going to show later on that will elegantly solve a UI problem I mentioned earlier.

#### Intersection

The intersection of two sets are the elements that are common in both, and like the other set operators, it removes duplicates. To perform an intersection you use the ampersand method as an operator.

```ruby
[1, 1, 3, 5] & [1, 2, 3]   #=> [ 1, 3 ]
```

#### A Practical Use Case

Let’s face it, building nice interfaces using HTML forms can be a challenge, especially when tying them to multiple models in Rails. Even Ryan Bates, creator of the amazing Railscasts website, took [2 episodes](http://railscasts.com/episodes/196-nested-model-form-part-1) to show how to handle some complex nested tables. Although the example I’m showing here isn’t nearly that complex, it does show how set operators can help out with some complex form handling.

#### Simple Bookshelf

For my example here, I’m going to construct a simple bookshelf application. The entire finished application can be found on [under my github account](https://github.com/mikefarmer/Simple-Bookshelf). The idea is that we have a database table full of books. A user can create as many bookshelves as they want and place books on them. The database model for this will require a has-and-belongs-to-many association.

The ERD looks like this:

<a href="/blog/2011/06/07/using-set-operators-with-ruby-arrays/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5615532536416837522" src="/blog/2011/06/07/using-set-operators-with-ruby-arrays/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 48px;"/></a>

To set this up in Rails, I’ll create a basic many to many association with the following code:

<script src="https://gist.github.com/1006755.js?file=book.rb"></script>

<script src="https://gist.github.com/1006755.js?file=bookshelf.rb"></script>

<script src="https://gist.github.com/1006755.js?file=chosen_book.rb"></script>

#### Approaching the UI

Now, in approaching how we are going to tackle assigning books to bookshelves, I want to display the list of books with checkboxes next to them under the bookshelf. When I check a book, I want that book to be added to my shelf. Likewise,when I uncheck the book, I want it removed.

<a href="/blog/2011/06/07/using-set-operators-with-ruby-arrays/image-1-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5615229221417118866" src="/blog/2011/06/07/using-set-operators-with-ruby-arrays/image-1.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 314px; height: 400px;"/></a>

#### The Implementation

The actual implementation here is grossly over simplified, but it illustrates what the concept well. I used [nifty generators](https://github.com/ryanb/nifty-generators) to setup some basic scaffolding for the books and bookshelves controllers. All the interesting code here will be done in the bookshelves controller and views. Let’s look at the view first:

<script src="https://gist.github.com/1006755.js?file=_form.html.erb"></script>

What we have here is a basic form for changing the name of my bookshelf. The interesting part here is where the books are displayed. In the controller I set @books to Book.all so that I can show all of the books with a checkbox next to them. There are a couple of things to notice that will be important later on. First, I’m using the check_box_tag helper will place the input tag outside the @bookshelf scope. Next for the checkbox name, I use "books[]". This will make it so that when the form is submitted, I will get a hash called books as one
of my params to work with. The keys in the hash will be the id of the book. The values will all be “1”. Next, I set the checkbox as checked if that book is already included in the @bookshelves assigned books.

Next, we’ll look at the update action in the bookshelves controller.

<script src="https://gist.github.com/1006755.js?file=bookshelves_controller.rb"></script>

Everything here is pretty standard except the call to the private method called sync_selected_books. This is the real meat and potatoes of what I want to illustrate here so I’ll break it down in detail. First, if no books were checked, we wont have a params[:books] value. It will just be nil. So in that case, we are going to remove any associated books with a delete_all method. Next, if we do have any checked books, then I want to create an array that only has those selected books in them and assign it to checked_books. Then I’ll get another array that has the currently selected books in them and assign it to current_books.

Using the set operators I described above, I’ll be able to determine which books to remove and which books to add using difference. Now I can use some database friendly methods to make the changes.

What makes this nice is how simple it is to understand and to test. The code explains exactly what I want it to do. The beauty of this method is that when I put it together, it worked the first time. The other nice thing about this is how it plays well with the database. We only touch the rows that need to be touched and don’t have to worry about the items that are the same.

#### Wrapping up

Using set operators to manipulate your arrays opens up a lot of possibilities that I hadn’t considered before. It’s worth your time to practice some of these operators and then use them in your projects where you need to manipulate the elements in multiple arrays.

Once again, the entire rails application I used for this illustration is located out on my github account at [https://github.com/mikefarmer/Simple-Bookshelf](https://github.com/mikefarmer/Simple-Bookshelf)

#### Footnotes

1. Ruby does have a Set class, but for my purposes here, I’m going to stick to thinking of arrays as sets as that’s generally what we use in our Ruby applications.
