---
author: Steph Skardal
title: 'Ruby on Rails: Russian Translation and Pluralization'
github_issue_number: 1404
tags:
- rails
- ruby
- localization
date: 2018-04-12
---

<img src="/blog/2018/04/rails-russian-localization/localization.jpg" alt="Coding" />
<small>[Photo by Matthew Henry of Burst](https://burst.shopify.com/photos/woman-codes)</small>

### Russian is Hard

Translation to Russian is tricky, and what’s even more tricky is coding logic to handle localization and pluralization of Russian (especially when you can’t read it). Here, I’ll explain some of the complexities and approaches I used for localization of a Ruby on Rails application.

### Pluralization

In general, Rails claims to have good localization and pluralization support, but I found that the support for handling more complex translations required customization. The first thing to note is that pluralization in Russian is not quite as simple as it is in English.

##### English

In English, we are familiar with pluralization of regular nouns to be appending an ‘s’ to the end of the noun (except for those nouns ending in ‘y’ and ‘o’). Pluralization is irregular in some cases, e.g. “octopus” becomes “octopi”, and Rails can handle some of these special cases for English but may not necessarily understand rules for other languages. See:

```ruby
pry(main)> pluralize 1, 'user'
=> "1 user"
pry(main)> pluralize 2, 'user'
=> "2 users"
pry(main)> pluralize 1, 'octopus'
=> "1 octopus"
pry(main)> pluralize 2, 'octopus'
=> "2 octopi"
```

Wikipedia has a thorough explanation of English plurals [here](https://en.wikipedia.org/wiki/English_plurals) for anyone interested.

##### Russian

Russian pluralization is more complex. In the most simplified terms (from my understanding), the mapping can boil down to:

* where count is zero, word has one ending
* where count is one, word has another ending
* where count is 2–4, 22–24, 32–34, word has yet another ending
* where count is 5–20, 25–30, 35–40, …: word has yet another ending

To accomplish this translation and pluralization in Rails, I implemented the following mapping found [here](https://stackoverflow.com/questions/6166064/i18n-pluralization):

```ruby
{:ru =>  
  { :i18n =>  
    { :plural =>  
      { :keys => [:zero, :one, :few, :other],
        :rule => lambda { |n| 
          if n == 0
            :zero
          elsif
            ( ( n % 10 ) == 1 ) && ( ( n % 100 != 11 ) ) 
            # 1, 21, 31, 41, 51, 61...
            :one
          elsif
            ( [2, 3, 4].include?(n % 10) \
            && ![12, 13, 14].include?(n % 100) )
            # 2-4, 22-24, 32-34...
            :few
          elsif ( (n % 10) == 0 || \
            ![5, 6, 7, 8, 9].include?(n % 10) || \
            ![11, 12, 13, 14].include?(n % 100) )
            # 0, 5-20, 25-30, 35-40...
            :other
          end
        }
      }   
    }   
  }   
}
```

And here is what our locales looks like for translating the noun ‘user’:

```
user:
  zero: пользователей
  one: пользователь
  few: пользователя
  other: пользователей
```

The above mapping helps us solve the initial problem with pluralized translations, but wait, there’s more complexity ahead!

### Contextual Changes (e.g. Nominative vs. Genitive)

In addition to complexities with pluralization, I had to heavily rely on our [client](http://www.musicarussica.com/) to further differentiate [noun declension](https://en.wikipedia.org/wiki/Declension). I’m not a linguist nor an English teacher, but my best explanation here is that there is a difference in noun endings if it is nominative vs. genitive. For example ‘Users’ vs. ‘List of Users’ uses the same pluralization of ‘user’ in English, but in Russian and many other languages, the context influences the word ending here.

What does this mean for us? It means that simply calling `t('user', count: 1)` or `t('user', count: 5)` may not provide the correct localization and pluralization because the text in front of or behind the translation influences its declension. Therefore, we can’t just have the zero, one, few, and other mapping as shown in the above code example.

### Enter Ruby on Rails, Rails gems (admin & breadcrumbs)

In our Ruby on Rails application, we use [RailsAdmin](https://github.com/sferik/rails_admin), a gem to add admin functionality to our application. RailsAdmin, and other gems that we use, use generic formulas of translations based on the pluralization code.

Examples of locales strings are:

* `"List of %{model_label_plural}"`
* `"%{model_label_plural}"`
* `"New %{model_label}"`
* `"Edit this %{model_label}"`
* `"%{model_label}"`

These formulas work fine for English, but they are too simplified for the contextual changes that I previously described.

Because RailsAdmin is a gem, that means I can override specific elements of it to accommodate Russian, and here’s a short list of how we accomplished this:

* Retrieved a [rails_admin.ru.yml](https://gist.github.com/sergey-alekseev/ba3c1d549e28a6721dee) as a starting point.
* In some cases, removed model_label or model_label_plural entirely from some translations to make more generic messages, e.g. instead of “User successfully saved”, we use some equivalent of “Successful.”
* Added code to override RailsAdmin helper methods used in various parts of RailsAdmin navigation and text rendering.
* Copy views from RailsAdmin source and override entirely to use custom translation mapping in the form of discrete strings.

### Hindsight is 20/20

When I started working on localization here, I was trying to work within the constraints of the gem and the formulas it used, but I ultimately had to resort to custom overrides of various helper methods and views. While this is not the method I prefer to work with a gem (making the upgrade path more complicated), I felt that this was the best way to handle localization & pluralization, *and* allow our client to override these discrete strings in a custom_admin locale file. Unfortunately, I could not find existing support for Rails 5.0 and our gems to handle the localization that I needed, so I would likely approach it similarly in the future.

[Musica Russica](http://www.musicarussica.com/) is one of our Ruby on Rails ecommerce clients. The founder, Dr. Vladimir Morosan, was extremely helpful in completing the translation (and corresponding explanation to a software engineer) of a new Ruby on Rails 5.0 site.
