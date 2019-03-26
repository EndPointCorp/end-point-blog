---
author: "Patrick Lewis"
title: "Converting GraphQL Ruby Resolvers to the Class-​based API"
tags: ruby, graphql
gh_issue_number: 1501
---

<img src="/blog/2019/02/28/converting-graphql-ruby-resolvers-to-the-class-based-api/banner.png" alt="GraphQL Ruby code" />

The [GraphQL gem](https://graphql-ruby.org/) is a great tool for any Rails developer who wants to add a full-​featured GraphQL API to their Rails applications.

I have been using GraphQL to serve an API in one of my Rails applications since late 2017 and have been very happy with the features and performance provided by the gem, but some of the domain-​specific syntax for building out my API schema never felt quite right when compared to the other Ruby code I was writing in my projects. Fortunately, the 1.8.0 release of the GraphQL Ruby gem brought with it a new default class-​based syntax while remaining compatible with existing code that predated the change.

The [Class-based API guide](https://graphql-ruby.org/schema/class_based_api) that accompanied the changes does a good job of describing the upgrade path for developers who need to convert their existing schemas. The old `.define` syntax is eventually going to be removed with version 2.0 of the gem, so I was interested in converting my existing API over to the new style, both to see what benefits the newer syntax provides and to ensure that the API schema remains compatible with future releases of the gem.

The GraphQL gem provides some rake tasks like `graphql:upgrade:schema` and `graphql:upgrade:member` for automatic conversion of the older-​style `.define` files to the newer class-​based syntax. It worked quite well for updating my [type definitions](https://graphql-ruby.org/type_definitions/objects.html), but I also make heavy use of [resolvers](https://graphql-ruby.org/fields/resolvers.html) for containing the logic needed to return values in my GraphQL fields, and there was no way to automatically convert those files.

I found that the process of manually converting my resolvers was pretty straightforward and provided some benefits by cleaning up my `QueryType` file that was starting to look a little unwieldy.

Here is a before and after for comparison:


Old pre-1.8 '.define' syntax for types:

```ruby
# app/graphql/types/query_type.rb
Types::QueryType = GraphQL::ObjectType.define do
  description 'Queries'

  field :instructor_names, types[types.String] do
    description 'Returns a collection of instructor names for a given range of years'

    argument :semester, !Inputs::SemesterInput
    argument :past_years, types.Int, 'Include instructors for this number of past years'

    resolve Resolvers::InstructorNamesResolver.new
  end
end
```

New class-based syntax for types:

```ruby
# app/graphql/types/query_type.rb
class Types::QueryType < Types::BaseObject
  description 'Queries'

  field :instructor_names,
      description: 'Returns a collection of instructor names for a given range of years',
      resolver: Resolvers::InstructorNamesResolver
end
```



Old pre-1.8 '.define' syntax for resolvers:

```ruby
# app/graphql/resolvers/instructor_names_resolver.rb
module Resolvers
  # Return collections of instructor names based on query arguments
  class InstructorNamesResolver
    def call(_obj, args, _ctx)
      semester = args[:semester]
      past_years = args[:past_years] || 0
      term_year_range = determine_term_year_range(semester, past_years)

      CourseInstructor
        .where(term_year: term_year_range)
        .group(:first_name, :last_name)
        .pluck(:first_name, :last_name)
        .map { |name| name.join(' ') }
    end

    private

    def determine_term_year_range(semester, past_years)
      term_year_max = semester[:term_year]
      term_year_min = term_year_max - past_years

      term_year_min..term_year_max
    end
  end
end
```

New class-based syntax for resolvers:

```ruby
# app/graphql/resolvers/instructor_names_resolver.rb
module Resolvers
  # Return collections of instructor names based on query arguments
  class InstructorNamesResolver < Resolvers::Base
    type [String], null: false

    argument :semester, Inputs::SemesterInput, required: true
    argument :past_years, Integer, 'Include instructors for this number of past years', required: false

    def resolve(semester:, past_years: 0)
      term_year_range = determine_term_year_range(semester, past_years)

      CourseInstructor
        .where(term_year: term_year_range)
        .group(:first_name, :last_name)
        .pluck(:first_name, :last_name)
        .map { |name| name.join(' ') }
    end

    private

    def determine_term_year_range(semester, past_years)
      term_year_max = semester[:term_year]
      term_year_min = term_year_max - past_years

      term_year_min..term_year_max
    end
  end
end
```

The main things to note here are:

* The class definitions for `Types::QueryType` and `Resolvers::InstructorNamesResolver`, which now inherit from base GraphQL classes.
* The `type` and `argument` definitions are moved out of the `query_type` file, cleaning it up greatly, especially for larger schemas with many fields.
* The `call` method in `InstructorNamesResolver` is now `resolve`, and accepts arguments using named parameters (or `**args` if you want to retain the previous syntax).

Overall, I’m really happy with the newer GraphQL API syntax and think that its more idiomatic Ruby is easier to work with and feels more familiar than the older style. I look forward to building out my API schema further and attempting things like replacing my use of Resolvers with plain old Ruby objects in order to make it even easier to test the logic they contain.
