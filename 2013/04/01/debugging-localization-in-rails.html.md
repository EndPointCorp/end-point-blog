---
author: Mike Farmer
gh_issue_number: 773
tags: rails
title: Debugging Localization in Rails
---



Rails offers a very extensive library for handling localization using [the rails-i18n gem](https://github.com/svenfuchs/rails-i18n). If you've done any localization using Rails, you know that it can be difficult to keep track of every string on your web application that needs translation. During a recent project, I was looking for an easy way to visually see translation issues while browsing through the UI in our application.

### Missing Translations

I've known for some time that when I was missing a translation for a given text that it would appear in the HTML with a special <span> tag with the class .translation_missing. So in my global CSS I added the following:

```css
.translation_missing { background-color: red; color: white !important; }
```

Now when I viewed any page where I had forgotten to add a translation to my en.yml file I could see the text marked in bright red. This served as a great reminder that I needed to add the translation.

I'm an avid watcher of my rails log while I develop. I almost always have a terminal window right next to my browser that is tailing out the log so I can catch any weirdnesses that may crop up. One thing that I thought would be nice is if the log showed any translation issues on the page it was loading. After some research, I found that the [I18n gem](http://rubygems.org/gems/i18n) used by Rails doesn't give you any obvious hooks for translation errors. There is, however, a section in the [Rails I18n Guide](http://guides.rubyonrails.org/i18n.html#using-different-exception-handlers) for adding custom exception handlers for translation issues and this is where I started with something like this in an initializer:

```ruby
module I18n
  def self.just_raise_that_exception(*args)
    Rails.logger.debug args.join("\n")
    raise args.first
  end
end

I18n.exception_handler = :just_raise_that_exception
```

This got things started for me. After some small modifications to the logger line, I had the output that I wanted and to make things really stick out, I added some color using the [term-ansicolor gem](http://flori.github.com/term-ansicolor/) and came up with this:

```ruby
def self.just_raise_that_exception(*args)
  require 'term/ansicolor'
  include Term::ANSIColor
  Rails.logger.debug red("--- I18n Missing Translation: #{args.inspect} ---")
  raise args.first
end
```

### I18n Fallbacks

After using this solution for a while I ran into another issue. When I would change the locale in my app to something like es (Spanish) and look for translation issues, I was noticing some text that wasn't being translated but it wasn't being marked as red by my CSS. When I looked at the text further I noticed that it wasn't even being surrounded by the <span class="translation_missing> tag. As it turned out, I did have a translation for that text in English, but not in the language that was set to my current locale. The reason for this is what I18n refers to as Fallbacks. Fallbacks tell the I18n what alternate, or default, locale to "fall back" to if a translation isn't available for the current locale. By default, the fallback locale is en. Since I had a translation for that text in my en.yml there was no indicator that I had "fallen back" even though it was obvious that there was a translation issue.

Coming up with a way to be notified of fallbacks wasn't nearly as simple as my initial solution. After a lot of googling and reading in StackOverflow, I found that perhaps the best solution was to [override the translate method](https://github.com/svenfuchs/i18n/blob/master/lib/i18n/backend/fallbacks.rb#L37) in the I18n gem. This sounds really scary, but it actually wasn't too bad. Back in my initializer, I removed the solution that I had originally come up with and added the following:

```ruby
module I18n::Backend
  module Fallbacks

    # To liven things up a bit
    require 'term/ansicolor'
    include Term::ANSIColor

    def translate(locale, key, options = {})
      # First things first, if there is an option sent, decorate it and send it back.
      return fallback_message(locale, key, super) if options[:fallback]

      default = extract_non_symbol_default!(options) if options[:default]

      options[:fallback] = true
      I18n.fallbacks[locale].each do |fallback|
        catch(:exception) do
          # Get the original translation
          translation = super(fallback, key, options)

          # return the translation if we didn't need to fall back
          return translation if fallback == locale

          # return the decorated fallback message if we did actually fall back.
          result = fallback_message(locale, key, translation)
          return result unless result.nil?
        end
      end
      options.delete(:fallback)

      return super(locale, nil, options.merge(:default => default)) if default

      # If we get here, then no translation was found.
      Rails.logger.debug red("--- I18n Missing Translation: #{locale}::#{key} ---")
      throw(:exception, I18n::MissingTranslation.new(locale, key, options))
    end

    # Added this method to log the fallback and decorate the text with a <span> tag.
    def fallback_message(locale, key, fallback_text)
      return nil if fallback_text.nil?
      keys = key.to_s.split(".")
      return fallback_text if keys.first == 'platform_ui'

      Rails.logger.debug yellow("--- I18n Fallback: #{locale}::#{key} ---")
      %(<span class="translation_fallback" title="translation missing: #{locale}, #{key}">#{fallback_text}</span>).html_safe
    end

  end
end
```

With this initializer in place, I added the following CSS to my global stylesheet:

```css
.translation_fallback { background-color: green; color: white !important; }
```

Now all missing translation errors and fallbacks were noticeable while browsing the UI and all translation issues were logged to my development log. Now obviously, I don't want these things showing up in production so I wrapped the whole thing in a if Rails.env.development? conditional. I could also think of times, like while working on implementing design, that I don't really care about translation issues as well, so I added a flag for turning it off in development as well.

You can see my entire solution on [a gist over at github.](https://gist.github.com/mikefarmer/5286140#file-debug_localization-rb) It was suggested by a fellow colleague that I should turn this into a gem, but I didn't see the need if all you had to do is copy and paste this initializer. If a gem is something you'd like to see this in, please let me know and I'll consider packaging it up.


