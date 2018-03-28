---
author: Kamil Ciemniewski
gh_issue_number: 1215
tags: machine-learning, optimization, probability-theory, ruby
title: Learning from data basics — the Naive Bayes model
---



Have you ever wondered what is the machinery behind some of the algorithms for doing seemingly very intelligent tasks? How is it possible that the computer program can recognize faces in photos, turn an image into a text or even classify some emails as legitimate or as spam?

Today, I’d like to present one of the simplest models for performing classification tasks. The model enables extremely fast execution, making it very practical in many use cases. The example I’ll choose will enable us to extend the discussion about the most optimal approach to another blog post.

### The problem

Imagine that you’re working on an e-commerce store for your client. One of the requirements is to present the currently logged in user with a “promotion box” somewhere on the page. The goal is to maximize our chances of having the user put the product from the box into the basket. There’s one promotional box and a couple of different categories of products to choose the actual product from.

### Thinking about the solution — using probability theory

One of the obvious directions we may want to turn towards is to use probability theory. If we could collect the data about the user’s previous choices and his or her characteristics, we can use probability to select the product category best suited for the current user. We would then choose a product from this category that currently has an active promotion.

### Quick theory refresher for programmers

As we’ll be exploring the probability approaches using Ruby code, I’d like to very quickly walk you through some of the basic concepts we will be using from now on.

#### Random variables

The simplest probability scenario many of us are already accustomed with is the coin toss results distribution. Here we’re throwing the coin, noting whether we get heads or tails. In this experiment, we call “got heads” and “got tails” probability events. We can also shift the terminology a bit by calling them: two values of the “toss result” **random variable**.

So in this case we’d have a random variable — let’s call it **T** (for “toss”) that can take values of: “heads” or “tails”. We then define the probability distribution P(T) as a function from the random variable value to a real number between 0 and 1 inclusively on both sides. In real world the probability values after e. g 10000 tosses might look like the following:

```nohighlight
+-------+---------------------+
| toss  | value               |
+-------+---------------------+
| heads | 0.49929999999999947 |
| tails |   0.500699999999998 |
+-------+---------------------+
```

These values are nearing 0.5 more and more with the greater number of tosses.

#### Factors and probability distributions

We’ve shown a simple probability distribution. To ease the comprehension of the Ruby code we’ll be working with, let me introduce the notion of the **factor**. We called the “table” from the last example a probability distribution. The table represented a function from a random variable’s value to a real number between [0, 1]. The **factor** is a generalization of that notion. It’s a function from the same domain, but returning any real number. We’ll explore the usability of this notion in some of our next articles.

The probability distribution is a factor that adds two constraints:

- its values are always in the range [0, 1] inclusively
- the sum of all it’s values is exactly 1

### Simple Ruby modeling of random variables and factors

We need to have some ways of computing probability distributions. Let’s define some simple tools we’ll be using in this blog series:

```ruby
# Let's define a simple version of the random variable
# - one that will hold discrete values
class RandomVariable
  attr_accessor :values, :name

  def initialize(name, values)
    @name = name
    @values = values
  end
end

# The following class really represents here a probability
# distribution. We'll adjust it in the next posts to make
# it match the definition of a "factor". We're naming it this
# way right now as every probability distribution is a factor
# too.
class Factor
  attr_accessor :_table, :_count, :variables

  def initialize(variables)
    @_table = {}
    @_count = 0.0
    @variables = variables
    initialize_table
  end

  # We're choosing to represent the factor / distribution
  # here as a table with value combinations in one column
  # and probability values in another. Technically, we're using
  # Ruby's Hash. The following method builds the the initial hash
  # with all the possible keys and values assigned to 0:
  def initialize_table
    variables_values = @variables.map do |var|
      var.values.map do |val|
        { var.name.to_sym => val }
      end.flatten
    end # [ [ { name: value } ] ]   
    @_table = variables_values[1..(variables_values.count)].inject(variables_values.first) do |all_array, var_arrays|
      all_array = all_array.map do |ob|
        var_arrays.map do |var_val|
          ob.merge var_val
        end
      end.flatten
      all_array
    end.inject({}) { |m, item| m[item] = 0; m }
  end

  # The following method adjusts the factor by adding information
  # about observed combination of values. This in turn adjusts probability
  # values for all the entries:
  def observe!(observation)
    if !@_table.has_key? observation
      raise ArgumentError, "Doesn't fit the factor - #{@variables} for observation: #{observation}"
    end

    @_count += 1

    @_table.keys.each do |key|
      observed = key == observation
      @_table[key] = (@_table[key] * (@_count == 0 ? 0 : (@_count - 1)) + 
       (observed ? 1 : 0)) / 
         (@_count == 0 ? 1 : @_count)
    end

    self
  end

  # Helper method for getting all the possible combinations
  # of random variable assignments
  def entries
    @_table.each
  end

  # Helper method for testing purposes. Sums the values for the whole
  # distribution - it should return 1 (close to 1 due to how computers
  # handle floating point operations)
  def sum
    @_table.values.inject(:+)
  end

  # Returns a probability of a given combination happening
  # in the experiment
  def value_for(key)
    if @_table[key].nil?
      raise ArgumentError, "Doesn't fit the factor - #{@varables} for: #{key}"
    end
    @_table[key]
  end

  # Helper method for testing purposes. Returns a table object
  # ready to be printed to stdout. It shows the whole distribution
  # as a table with some columns being random variables values and
  # the last one being the probability value
  def table
    rows = @_table.keys.map do |key|
      key.values << @_table[key]
    end
    table = Terminal::Table.new rows: rows, headings: ( @variables.map(&:name) << "value" )
    table.align_column(@variables.count, :right)
    table
  end

  protected

  def entries=(_entries)
    _entries.each do |entry|
      @_table[entry.keys.first] = entry.values.first
    end
  end

  def count
    @_count
  end

  def count=(_count)
    @_count = _count
  end
end
```

Notice that we’re using here the **terminal-table** gem as a helper for printing out the factors in an easy to grasp fashion. You’ll need the following requires:

```ruby
require 'rubygems'
require 'terminal-table'
```

### The scenario setup

Let’s imagine that we have the following categories to choose from:

```ruby
category = RandomVariable.new :category, [ :veggies, :snacks, :meat, :drinks, :beauty, :magazines ]
```

And the following user features on each request:

```ruby
age      = RandomVariable.new :age,      [ :teens, :young_adults, :adults, :elders ]
sex      = RandomVariable.new :sex,      [ :male, :female ]
relation = RandomVariable.new :relation, [ :single, :in_relationship ]
location = RandomVariable.new :location, [ :us, :canada, :europe, :asia ]
```

Let’s define the data model that resembles logically the one we could have in our real e-commerce application:

```ruby
class LineItem
  attr_accessor :category

  def initialize(category)
    self.category = category
  end
end

class Basket
  attr_accessor :line_items

  def initialize(line_items)
    self.line_items = line_items
  end
end

class User
  attr_accessor :age, :sex, :relationship, :location, :baskets

  def initialize(age, sex, relationship, location, baskets)
    self.age = age
    self.sex = sex
    self.relationship = relationship
    self.location = location
    self.baskets = baskets
  end
end
```

We want to utilize a user’s baskets in order to infer the most probable value for a category, given a set of user’s features. In our example, we can imagine that we’re offering authentication via Facebook. We can grab info about a user’s sex, location, age and whether she/he is in relationship or not. We want to find a category that’s being chosen the most by users with a given set of features.

As we don’t have any real data to play with, we’ll need a generator to create fake data of certain characteristics. Let’s first define a helper class with a method, that will allow us to choose a value out of a given list of options along with their weights:

```ruby
class Generator
  def self.pick(options)
    items = options.inject([]) do |memo, keyval|
      key, val = keyval
      memo << Array.new(val, key)
      memo
    end.flatten
    items.sample
  end
end
```

With all the above we can define a random data generation model:

```ruby
class Model

  # Let's generate `num` users (1000 by default)
  def self.generate(num = 1000)
    num.times.to_a.map do |user_index|
      gen_user
    end
  end

  # Returns a user with randomly selected traits and baskets
  def self.gen_user
    age = gen_age
    sex = gen_sex
    rel = gen_rel(age)
    loc = gen_loc
    baskets = gen_baskets(age, sex)

    User.new age, sex, rel, loc, baskets
  end

  # Randomly select a sex with 40% chance for getting a male
  def self.gen_sex
    Generator.pick male: 4, female: 6
  end

  # Randomly select an age with 50% chance for getting a teen
  # (among other options and weights)
  def self.gen_age
    Generator.pick teens: 5, young_adults: 2, adults: 2, elders: 1
  end

  # Randomly select a relationship status.
  # Depend the chance of getting a given option on the user's age
  def self.gen_rel(age)
    case age
      when :teens        then Generator.pick single: 7, in_relationship: 3
      when :young_adults then Generator.pick single: 4, in_relationship: 6
      else                    Generator.pick single: 8, in_relationship: 2
    end
  end

  # Randomly select a location with 40% chance for getting a united states
  # (among other options and weights)
  def self.gen_loc
    Generator.pick us: 4, canada: 3, europe: 1, asia: 2
  end

  # Randomly select 20 basket line items.
  # Depend the chance of getting a given option on the user's age and sex
  def self.gen_items(age, sex)
    num = 20

    num.times.to_a.map do |i|
      if (age == :teens || age == :young_adults) && sex == :female
        Generator.pick veggies: 1, snacks: 3, meat: 1, drinks: 1, beauty: 9, magazines: 6
      elsif age == :teens  && sex == :male
        Generator.pick veggies: 1, snacks: 6, meat: 4, drinks: 1, beauty: 1, magazines: 4
      elsif (age == :young_adults || age == :adults) && sex == :male
        Generator.pick veggies: 1, snacks: 4, meat: 6, drinks: 6, beauty: 1, magazines: 1
      elsif (age == :young_adults || age == :adults) && sex == :female
        Generator.pick veggies: 4, snacks: 4, meat: 2, drinks: 1, beauty: 6, magazines: 3
      elsif age == :elders && sex == :male
        Generator.pick veggies: 6, snacks: 2, meat: 2, drinks: 2, beauty: 1, magazines: 1
      elsif age == :elders && sex == :female
        Generator.pick veggies: 8, snacks: 1, meat: 2, drinks: 1, beauty: 4, magazines: 1
      else
        Generator.pick veggies: 1, snacks: 1, meat: 1, drinks: 1, beauty: 1, magazines: 1
      end
    end.map do |cat|
      LineItem.new cat
    end
  end

  # Randomly select 5 baskets depending the traits of the basket on user
  # age and sex
  def self.gen_baskets(age, sex)
    num = 5

    num.times.to_a.map do |i|
      Basket.new gen_items(age, sex)
    end
  end
end
```

### Where is the complexity?

The approach described above doesn’t seem that exciting or complex. Usually reading about probability theory applied in the field of machine learning requires going through quite a dense set of mathematical notions. The field is also being actively worked on by researchers. This implies a huge complexity — certainly not the simple definition of probability that we got used to in high school.

The problem becomes a bit more complex if you consider efficiency of computing the probabilities. In our example, the joined probability distribution — to fully describe the scenario — needs to specify probability values for 383 cases:

```ruby
p(:veggies, :teens, :male, :single, :us) # one of 384 combinations
```

Given that the probability distributions have to sum up to 1, the last case can be fully inferred from the sum of all the others. This means that we need 6 * 4 * 2 * 2 * 4 - 1 = 383 parameters in the model: 6 categories, 4 age classes, 2 sexes, 2 relationship kinds and 4 locations. Imagine adding one additional, 4 valued feature (a season). This would grow our number of parameters to **1535**. And this is a very simple training example. We could have a model with close to 100 different features. The number of parameters would clearly be unmanageable even on the biggest servers we could put them in. This approach would also make it very painful to add additional features to the model.

### Very simple but powerful optimization: The Naive Bayes model

In this section I’m going to present you with an equation we’ll be working with when optimizing our example. I’m not going to explain the mathematics behind it as you can easily read about them on e. g. Wikipedia.

The approach is called the **[Naive Bayes model](https://en.wikipedia.org/wiki/Naive_Bayes_classifier)**. It is being used e .g. in spam filters. It also has been used in the past in medical diagnosis field.

It allows us to present the full probability distribution as a product of factors:

```ruby
p(cat, age, sex, rel, loc) == p(cat) * p(age | cat) * p(sex | cat) * p(rel | cat) * p(loc | cat)
```

Where e. g. p(age | cat) represents the probability of a user being a certain age given that this user selects cat products most frequently. This is called the “posterior probability”. The above equation states that we can simplify the distribution to be a product of some number of much more easily manageable factors.

The category from our example is often called a **class** and the rest of random variables in the distribution are often called **features**.

In our example, the number of parameters we’ll need to manage when presenting the distribution in this form drops to:

```ruby
(6 - 1) + (6 * 4 - 1) + (6 * 2 - 1) + (6 * 2 - 1) + (6 * 4 - 1) == 73
```

That’s just around 19% of the original amount! Also, adding another variable (season) would only add 23 new parameters (compared to 1152 in the full distribution case).

The Naive Bayes model limits the number of parameters we have to manage but it comes with very strong assumptions about the variables involved: in our example, that the user features are conditionally independent given the resulting category. Later on I’ll show why this isn’t true in this case even though the results will still be quite okay.

### Implementing the Naive Bayes model

As we now have all the tools we need, let’s get back to the probability theory to figure out how best to model the Naive Bayes in terms of the Ruby blocks we now have.

The approach says that under the assumptions we discussed we can approximate the original distribution to be the product of factors:

```ruby
p(cat, age, sex, rel, loc) = p(cat) * p(age | cat) * p(sex | cat) * p(rel | cat) * p(loc | cat)
```

Given the definition of the conditional probability we have that:

```ruby
p(a | b) = p(a, b) / p(b)
```

Thus, we can express the approximation as:

```ruby
p(cat, age, sex, rel, loc) = p(cat) * ( p(age, cat) / p(cat) ) * ( p(sex, cat) / p(cat) ) * ( p(rel, cat) / p(cat) ) * ( p(loc, cat) / p(cat) )
```

And then simplify it even further as:

```ruby
p(cat, age, sex, rel, loc) = p(age, cat) * ( p(sex, cat) / p(cat) ) * ( p(rel, cat) / p(cat) ) * ( p(loc, cat) / p(cat) )
```

Let’s define all the factors we will need:

```ruby
cat_dist     = Factor.new [ category ]
age_cat_dist = Factor.new [ age, category ]
sex_cat_dist = Factor.new [ sex, category ]
rel_cat_dist = Factor.new [ relation, category ]
loc_cat_dist = Factor.new [ location, category ]
```

Also, we want a full distribution to compare the results:

```ruby
full_dist = Factor.new [ category, age, sex, relation, location ]
```

Let’s generate 1000 random users and looping through them and their baskets - adjust probability distributions for combinations of product categories and user traits:

```ruby
Model.generate(1000).each do |user|
  user.baskets.each do |basket|
    basket.line_items.each do |item|
      cat_dist.observe! category: item.category
      age_cat_dist.observe! age: user.age, category: item.category
      sex_cat_dist.observe! sex: user.sex, category: item.category
      rel_cat_dist.observe! relation: user.relationship, category: item.category
      loc_cat_dist.observe! location: user.location, category: item.category
      full_dist.observe! category: item.category, age: user.age, sex: user.sex,
        relation: user.relationship, location: user.location
    end
  end
end
```

We can now print the distributions as tables to have an insight about the data:

```ruby
[ cat_dist, age_cat_dist, sex_cat_dist, rel_cat_dist, 
  loc_cat_dist, full_dist ].each do |dist|
    puts dist.table
    # Let's print out the sum of all entries to ensure the
    # algorithm works well:
    puts dist.sum
    puts "\n\n"
end
```

Which yields the following to the console (the full distribution is truncated due to its size):

```nohighlight
+-----------+---------------------+
| category  | value               |
+-----------+---------------------+
| veggies   |             0.10866 |
| snacks    | 0.19830999999999863 |
| meat      |             0.14769 |
| drinks    | 0.10115999999999989 |
| beauty    |             0.24632 |
| magazines | 0.19785999999999926 |
+-----------+---------------------+
0.9999999999999978

+--------------+-----------+----------------------+
| age          | category  | value                |
+--------------+-----------+----------------------+
| teens        | veggies   |  0.02608000000000002 |
| teens        | snacks    |  0.11347999999999969 |
| teens        | meat      |  0.06282999999999944 |
| teens        | drinks    |   0.0263200000000002 |
| teens        | beauty    |   0.1390699999999995 |
| teens        | magazines |  0.13322000000000103 |
| young_adults | veggies   | 0.010250000000000023 |
| young_adults | snacks    |  0.03676000000000003 |
| young_adults | meat      |  0.03678000000000005 |
| young_adults | drinks    |  0.03670000000000045 |
| young_adults | beauty    |  0.05172999999999976 |
| young_adults | magazines | 0.035779999999999916 |
| adults       | veggies   | 0.026749999999999927 |
| adults       | snacks    |  0.03827999999999962 |
| adults       | meat      | 0.034600000000000505 |
| adults       | drinks    | 0.028190000000000038 |
| adults       | beauty    |  0.03892000000000036 |
| adults       | magazines |  0.02225999999999998 |
| elders       | veggies   |  0.04558000000000066 |
| elders       | snacks    | 0.009790000000000047 |
| elders       | meat      | 0.013480000000000027 |
| elders       | drinks    | 0.009949999999999931 |
| elders       | beauty    | 0.016600000000000226 |
| elders       | magazines | 0.006600000000000025 |
+--------------+-----------+----------------------+
1.0000000000000013

+--------+-----------+----------------------+
| sex    | category  | value                |
+--------+-----------+----------------------+
| male   | veggies   |  0.03954000000000044 |
| male   | snacks    |   0.1132499999999996 |
| male   | meat      |  0.10851000000000031 |
| male   | drinks    |                0.073 |
| male   | beauty    | 0.023679999999999857 |
| male   | magazines |  0.05901999999999993 |
| female | veggies   |  0.06911999999999997 |
| female | snacks    |  0.08506000000000069 |
| female | meat      |  0.03918000000000006 |
| female | drinks    |  0.02816000000000005 |
| female | beauty    |  0.22264000000000062 |
| female | magazines |  0.13884000000000046 |
+--------+-----------+----------------------+
1.000000000000002

+-----------------+-----------+----------------------+
| relation        | category  | value                |
+-----------------+-----------+----------------------+
| single          | veggies   |  0.07722000000000082 |
| single          | snacks    |  0.13090999999999794 |
| single          | meat      |  0.09317000000000061 |
| single          | drinks    | 0.059979999999999915 |
| single          | beauty    |  0.16317999999999971 |
| single          | magazines |  0.13054000000000135 |
| in_relationship | veggies   | 0.031440000000000336 |
| in_relationship | snacks    |  0.06740000000000032 |
| in_relationship | meat      | 0.054520000000000006 |
| in_relationship | drinks    |  0.04118000000000009 |
| in_relationship | beauty    |  0.08314000000000002 |
| in_relationship | magazines |  0.06732000000000182 |
+-----------------+-----------+----------------------+
1.000000000000003

+----------+-----------+----------------------+
| location | category  | value                |
+----------+-----------+----------------------+
| us       | veggies   |  0.04209000000000062 |
| us       | snacks    |  0.07534000000000109 |
| us       | meat      | 0.055059999999999984 |
| us       | drinks    |  0.03704000000000108 |
| us       | beauty    |  0.09879000000000099 |
| us       | magazines |  0.07867999999999964 |
| canada   | veggies   | 0.027930000000000062 |
| canada   | snacks    |  0.05745999999999996 |
| canada   | meat      |  0.04288000000000003 |
| canada   | drinks    |  0.03078999999999948 |
| canada   | beauty    |  0.06397999999999997 |
| canada   | magazines | 0.053959999999999675 |
| europe   | veggies   | 0.013110000000000132 |
| europe   | snacks    |   0.0223200000000001 |
| europe   | meat      |  0.01730000000000005 |
| europe   | drinks    | 0.011859999999999964 |
| europe   | beauty    | 0.025490000000000183 |
| europe   | magazines | 0.020920000000000164 |
| asia     | veggies   |  0.02552999999999989 |
| asia     | snacks    |  0.04319000000000044 |
| asia     | meat      |  0.03244999999999966 |
| asia     | drinks    |  0.02147000000000005 |
| asia     | beauty    |  0.05805999999999953 |
| asia     | magazines |   0.0442999999999999 |
+----------+-----------+----------------------+
1.0000000000000029

+-----------+--------------+--------+-----------------+----------+------------------------+
| category  | age          | sex    | relation        | location | value                  |
+-----------+--------------+--------+-----------------+----------+------------------------+
| veggies   | teens        | male   | single          | us       |  0.0035299999999999936 |
| veggies   | teens        | male   | single          | canada   |  0.0024500000000000073 |
| veggies   | teens        | male   | single          | europe   |  0.0006999999999999944 |
| veggies   | teens        | male   | single          | asia     |  0.0016699999999999899 |
| veggies   | teens        | male   | in_relationship | us       |   0.001340000000000006 |
| veggies   | teens        | male   | in_relationship | canada   |  0.0010099999999999775 |
| veggies   | teens        | male   | in_relationship | europe   |  0.0006499999999999989 |
| veggies   | teens        | male   | in_relationship | asia     |   0.000819999999999994 |

(... many rows ...)

| magazines | elders       | male   | in_relationship | asia     | 0.00012000000000000163 |
| magazines | elders       | female | single          | us       |  0.0007399999999999966 |
| magazines | elders       | female | single          | canada   |  0.0007000000000000037 |
| magazines | elders       | female | single          | europe   |  0.0003199999999999965 |
| magazines | elders       | female | single          | asia     |  0.0005899999999999999 |
| magazines | elders       | female | in_relationship | us       |  0.0004899999999999885 |
| magazines | elders       | female | in_relationship | canada   | 0.00027000000000000114 |
| magazines | elders       | female | in_relationship | europe   | 0.00012000000000000014 |
| magazines | elders       | female | in_relationship | asia     | 0.00012000000000000014 |
+-----------+--------------+--------+-----------------+----------+------------------------+
1.0000000000000004
```

Let’s define a Proc for inferring categories based on user traits as evidence:

```ruby
infer = -> (age, sex, rel, loc) do

  # Let's map through the possible categories and the probability
  # values the distibutions assign to them:
  all = category.values.map do |cat|
    pc  = cat_dist.value_for category: cat
    pac = age_cat_dist.value_for age: age, category: cat
    psc = sex_cat_dist.value_for sex: sex, category: cat
    prc = rel_cat_dist.value_for relation: rel, category: cat
    plc = loc_cat_dist.value_for location: loc, category: cat

    { category: cat, value: (pac * psc/pc * prc/pc * plc/pc) }
  end

  # Let's do the same with the full distribution to be able to compare
  # the results:
  all_full = category.values.map do |cat|
    val = full_dist.value_for category: cat, age: age, sex: sex,
            relation: rel, location: loc

    { category: cat, value: val }
  end

  # Here's we're getting the most probable categories based on the
  # Naive Bayes distribution approximation model and based on the full
  # distribution:
  win      = all.max      { |a, b| a[:value] <=> b[:value] }
  win_full = all_full.max { |a, b| a[:value] <=> b[:value] }

  puts "Best match for #{[ age, sex, rel, loc ]}:"
  puts "   #{win[:category]} => #{win[:value]}"
  puts "Full pointed at:"
  puts "   #{win_full[:category]} => #{win_full[:value]}\n\n"
end
```

### The results

We’re ready now to use the model and see how well the Naive Bayes model performs in this particular scenario:

```ruby
infer.call :teens, :male, :single, :us
infer.call :young_adults, :male, :single, :asia
infer.call :adults, :female, :in_relationship, :europe
infer.call :elders, :female, :in_relationship, :canada
```

This gave the following results on the console:

```nohighlight
Best match for [:teens, :male, :single, :us]:
   snacks => 0.016252573282200262
Full pointed at:
   snacks => 0.01898999999999971

Best match for [:young_adults, :male, :single, :asia]:
   meat => 0.0037455794492659757
Full pointed at:
   meat => 0.0017000000000000016

Best match for [:adults, :female, :in_relationship, :europe]:
   beauty => 0.0012287311061725868
Full pointed at:
   beauty => 0.0003000000000000026

Best match for [:elders, :female, :in_relationship, :canada]:
   veggies => 0.002156365730474441
Full pointed at:
   veggies => 0.0013500000000000022
```

That’s quite impressive! Even though we’re using a simplified model to approximate the original distribution, the algorithm managed to infer the correct values in all cases. You can notice also that the results differ only by a couple of cases in 1000.

The approximation like that would certainly be very useful in a more complex e-commerce scenario, in the case where the number of evidence variables would be big enough to be unmanageable using the full distribution. There are use cases though, where a couple of errors in 1000 cases would be too many — the traditional example is medical diagnosis. There are also cases where the number of errors would be much greater just because the Naive Bayes assumption of conditional independence of variables is not always a fair an assumption. Is there a way to improve?

The Naive Bayes assumption says that the distribution factorizes the way we did it **only if the features are conditionally independent given the category**. The notion of **conditional independence** (apart from the formal mathematical definition) suggests that if some variables a and b are conditionally independent given c, then if we know the value of c then no additional information about b can alter our knowledge about a. In our example, knowing the category, let say :beauty doesn’t mean that e. g sex is independent from age. In real world examples, it’s often very hard to find a use case for Naive Bayes that would follow the assumption in all the cases.

There are alternative approaches that allow us to apply the assumptions that more rigidly follow the chosen data set. We will explore these in the next articles, building on top of what we saw here.


