---
author: Selvakumar Arumugam
gh_issue_number: 1042
tags: ruby, rails
title: Rails Recursive Sorting for Multilevel Nested Array of Objects
---


Whenever you display data as a list of records, sorting them in a particular order is recommended. Most of the time, Rails treats data as an array, an array of objects, or as a nested array of objects (tree). We would like to use a general sorting mechanism to display the records in ascending or descending order, to provide a decent view to end users. Luckily, Rails comes with a sorting method called 'sort_by' which helps to sort the array of objects by specific object values.

## Simple Array:

Trivially, an array can be sorted just by sorting using the “sort” method:

```ruby
my_array = [ 'Bob', 'Charlie', 'Alice']

my_array = my_array.sort;  # (or just my_array.sort!)
```

This is the most basic way to sort elements in an array and is part of Ruby’s built-in API.

## Array of Objects:

Usually, the result set of the Rails will have an array of objects and should be sorted based on specific attributes of the object in the array. Here is a sample array of objects which need to be sorted by date and fullname.

```ruby
s_array =
[  
    {
        "date"=> "2014-05-07",
        "children"=> [],
        "fullname"=> "Steve Yoman"
    },
    {
        "date"=> "2014-05-06",
        "children"=> [],
        "fullname"=> "Josh Tolley"
    }
]
```

### Solution:

#### ***1) Simple sorting***

We can use the Rails sort_by method to sort the array of objects by date and fullname in order:

```ruby
s_array = s_array.sort_by{|item| [ item['date'], item['fullname'] ]}
```

sort_by is passed an anonymous function which operates on each item, returning a value to be used as a sort key (returned as an anonymous array in this case). Because Ruby’s array have the Enumerable property, they will automatically be able to be used as sort keys as long as the elements containing them are as well. Because we are returning string properties, we get this for free. We can make use of Rails sort_by method to sort the array of objects by date and fullname in order.

#### ***2) Handling case on strings***

Sometimes sorting directly on the object attribute will produce undesirable results, for instance if there is inconsistent case in the data. We can further normalize the case of the string used to get records to sort in the expected order:

```ruby
s_array = s_array.sort_by{|item| [ item['date'], item['fullname'].downcase ]}
```

Here again we are returning an array to be used as a sort key, but we are using a normalized version of the input data to return.

## Multilevel Nested Array of Objects

Sometimes objects in an array will contain the array as element and it continues multilevel. Sorting this kind of array requires recursive sorting to sort the all the levels of array of objects based on specific attributes in object. The following array has nested array and objects alternatively:

```ruby
m_array =
[
    {
        "name"=> "Company",
        "children"=> [
            {
                "name"=> "Sales",
                "children"=> [
                    {
                        "date"=> "2014-05-07",
                        "children"=> [],
                        "fullname"=> "Steve Yoman"
                    },
                    {
                        "date"=> "2014-05-06",
                        "children"=> [],
                        "fullname"=> "Josh Tolley"
                    }
                ]
            },
            {
                "name"=> "Change Requests",
                "children"=> [
                    {
                        "name"=> "Upgrade Software",
                        "children"=> [
                            {
                                "date"=> "2014-05-01",
                                "children"=> [],
                                "fullname"=> "Selvakumar Arumugam"
                            },
                            {
                                "date"=> "2014-05-02",
                                "children"=> [],
                                "fullname"=> "Marina Lohova"
                            }
                        ]
                    },
                    {
                        "name"=> "Install Software",
                        "children"=> [
                            {
                                "date"=> "2014-05-01",
                                "children"=> [],
                                "fullname"=> "Selvakumar Arumugam"
                            },
                            {
                                "date"=> "2014-05-01",
                                "children"=> [],
                                "fullname"=> "Josh Williams"
                            }
                        ]
                    }
                ]
            }
        ]
    }
]
```

### Solution:

In order to tackle this issue, we will want to sort all of the sub-levels of the nested objects in the same way. We will define a recursive function in order to handle this. We will also want to add additional error-handling.

In this specific example, we know each level of the data contains a “children” attribute, which contains an array of associated objects.  We write our sort_multi_array function to recursively sort any such arrays it finds, which will in turn sort all children by name, date and case-insensitive fullname:

```ruby
def sort_multi_array(items)
  items = items.sort_by{|item| [ item['name'], item['date'], item['fullname'].to_s.downcase ]}
  items.each{ |item| item['children'] = sort_multi_array(item['children']) if (item['children'].nil? ? [] : item['children']).size > 0 }
  items
end

m_array = sort_multi_array(m_array);
```

You can see that we first sort the passed-in array according to the object-specific attributes, then we check to see if there is an attribute ‘children’ which exists, and then we sort this array using the same function. This will support any number of levels of recursion on this data structure.

### Notes about this implementation:

#### *1. Case-insensitive sorting*

The best practice when sorting the strings is to convert to one unique case (i.e upper or lower) on sorting. This ensures that records show up in the order that the user would expect, not the computer:

```ruby
item['fullname'].downcase
```

#### *2. Handling null values in case conversion*

The nil values on the attributes need to be handled on the string manipulation process to avoid the unexpected errors. Here we converting to string before applying the case conversion:

```ruby
item['fullname'].to_s.downcase
```

#### *3. Handling null values in array size check*

The nil values on the array attributes need to be handled on the sorting process to avoid the unexpected errors. Here we guard against the possibility of item[‘children’] being nil, and if it is, then we return an empty array instead:

```ruby
(item['children'].nil? ? [] : item['children']).size
```


