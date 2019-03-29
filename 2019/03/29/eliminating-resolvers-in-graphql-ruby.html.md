---
author: "Patrick Lewis"
title: "Eliminating Resolvers in GraphQL Ruby"
tags: ruby, graphql
gh_issue_number: 1512
---

<img src="/blog/2019/03/29/eliminating-resolvers-in-graphql-ruby/banner.png" alt="GraphQL Ruby code" />

In this follow-up to my post from last month about [Converting GraphQL Ruby Resolvers to the Class-based API](/blog/2019/02/28/converting-graphql-ruby-resolvers-to-the-class-based-api) I’m going to show how I took the advice of the GraphQL gem’s [documentation on Resolvers](https://graphql-ruby.org/fields/resolvers.html) and started replacing the GraphQL-specific Resolver classes with plain old Ruby classes to facilitate easier testing and code reuse.

The current documentation for the `GraphQL::Schema::Resolver` class essentially recommends that it not be used, except for cases with specific requirements as detailed in the documentation.

> Do you really need a Resolver? Putting logic in a Resolver has some downsides:

> Since it’s coupled to GraphQL, it’s harder to test than a plain ol’ Ruby object in your app
> Since the base class comes from GraphQL-Ruby, it’s subject to upstream changes which may require updates in your code

> Here are a few alternatives to consider:

> * Put display logic (sorting, filtering, etc.) into a plain ol’ Ruby class in your app, and test that class

> * Hook up that object with a method

I found that I was indeed having trouble testing my Resolvers that inherited from `GraphQL::Schema::Resolver` due to the GraphQL-specific overhead and context that they contained. Fortunately, it turned out to be a pretty simple process to convert a Resolver class to a plain Ruby class and test it with RSpec.

This was my starting point:

```ruby
# app/graphql/resolvers/instructor_names.rb
module Resolvers
  # Return collections of instructor names based on query arguments
  class InstructorNames < Resolvers::Base
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

I started the conversion process by rewriting my `Resolvers::InstructorNames` class to be a plain Ruby object:

```ruby
# app/graphql/resolvers/instructor_names.rb
module Resolvers
  class InstructorNames
    def self.run(semester:, past_years:)
      term_year_range = determine_term_year_range(semester, past_years)

      CourseInstructor
        .where(term_year: term_year_range)
        .group(:first_name, :last_name)
        .pluck(:first_name, :last_name)
        .map { |name| name.join(' ') }
    end

    def self.determine_term_year_range(semester, past_years)
      term_year_max = semester[:term_year]
      term_year_min = term_year_max - past_years

      term_year_min..term_year_max
    end
  end
end
```

The removal of all GraphQL-specific code made this an easy class to test with RSpec:

```ruby
# spec/graphql/resolvers/instructor_names_spec.rb
require 'rails_helper'

module Resolvers
  RSpec.describe InstructorNames do
    let!(:instructors_2018) { create_pair(:course_instructor, term_year: semester_2018[:term_year]) }
    let!(:instructors_2019) { create_pair(:course_instructor, term_year: semester_2019[:term_year]) }
    let(:outcome) { described_class.run(inputs) }
    let(:semester_2018) { { term_year: 2018 } }
    let(:semester_2019) { { term_year: 2019 } }

    context 'with a single year' do
      let(:inputs) { { semester: semester_2019, past_years: 0 } }

      it 'returns the expected list of instructor names' do
        expect(outcome).to match_array(instructors_2019.map(&:full_name))
      end
    end

    context 'with multiple years' do
      let(:inputs) { { semester: semester_2019, past_years: 1 } }
      let(:instructors) { instructors_2018 + instructors_2019 }

      it 'returns the expected list of instructor names' do
        expect(outcome).to match_array(instructors.map(&:full_name))
      end
    end
  end
end
```

Finally, I updated my query type to hook up the GraphQL field with the return value of the new plain `InstructorNames` class:

Old `QueryType`:

```ruby
# app/graphql/types/query_type.rb
class Types::QueryType < Types::BaseObject
  description 'Queries'

  field :instructor_names,
      description: 'Returns a collection of instructor names for a given range of years',
      resolver: Resolvers::InstructorNames
end
```

New `QueryType`:

```ruby
# app/graphql/types/query_type.rb
module Types
  class Query < Types::BaseObject
    description 'Queries'

    field :instructor_names, [String], null: false, description: 'Returns a collection of instructor names for a given range of years' do
      argument :semester, Types::Inputs::Semester, required: true
      argument :past_years, Integer, 'Include instructors for this number of past years', required: false
    end

    def instructor_names(semester:, past_years: 0)
      Resolvers::InstructorNames.run(semester: semester, past_years: past_years)
    end
end
```

Note that the `instructor_names` method matches the `instructor_names` field definition, and is responsible for providing the value returned by that field. The argument and field type definitions have been moved out of the Resolver (because it no longer contains anything specific to GraphQL) and into the field definition.

I considered moving my updated “Resolver” logic out of the `app/graphql/` hierarchy entirely, and that might have made more sense if I anticipated wanting to reuse that code elsewhere in my application. But since this particular Rails application is running in API mode and really only exists to serve the GraphQL API, I decided to leave it in place and maintain the naming convention while removing the actual GraphQL inheritance. For a larger application it might make sense to move these files into a directory under `lib/`.
