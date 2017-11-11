---
author: Marina Lohova
gh_issue_number: 837
tags: rails
title: has_many filter in RailsAdmin
---



I enjoyed using the RailsAdmin record filtering abilities until one day I needed to find all the orders with the specific product. 

```ruby
class Order < ActiveRecord::Base
   has_many :products, :through => :orders_products
end
```

The following valid piece of RailsAdmin configuration did not break anything but did not work either:

```ruby
RailsAdmin.config do |config|
  config.model Order do
    list do
      field :products do
        searchable :name 
      end
    end
  end
end
```

The reason is that only the belongs_to association is enabled for the search, as stated in the "Field searching" section of the [ documentation](https://github.com/sferik/rails_admin/wiki/List):

```
(3) Belongs_to associations : will be searched on their foreign_key (:team_id) 
or on their label if label is not virtual (:name, :title, etc.)
```
Benoit Bénézech, creator of RailsAdmin, [confirmed this as well](https://groups.google.com/forum/#!topic/rails_admin/POCY-c_knDk):

```
has_many are not added to the include for perf reason. That means that AR won't find the :programs table
```

We only had a few has_many fields configured across the project, so I decided to look into the source code and see if the limitation can be bypassed.

[MainController](https://github.com/sferik/rails_admin/blob/master/app/controllers/rails_admin/main_controller.rb) class in RailsAdmin invokes the "get_collection" method to fetch the records for the list action. It defines the "associations" variable which is used to generate SQL query for the filters. I reopened the class in config/initializers/rails_admin_main_controller.rb:

```ruby
module RailsAdmin
  MainController.class_eval do
    def get_collection(model_config, scope, pagination)
      associations = model_config.list.fields
        .select {|f| f.type == :belongs_to_association || f.type == :has_many_association && !f.polymorphic?}
        .map {|f| f.association[:name] } 
      options = {}
      options = options.merge(:page => (params[:page] || 1).to_i,
        :per => (params[:per] || model_config.list.items_per_page)) if pagination
      options = options.merge(:include => associations) unless associations.blank?
      options = options.merge(get_sort_hash(model_config))
      options = options.merge(:query => params[:query]) if params[:query].present?
      options = options.merge(:filters => params[:f]) if params[:f].present?
      options = options.merge(:bulk_ids => params[:bulk_ids]) if params[:bulk_ids]
      objects = model_config.abstract_model.all(options, scope)
    end
  end
end
```
Take a look at the very first line of the method. It used to be:

```ruby
associations = model_config.list.fields.
select {|f| f.type == :belongs_to_association && !f.polymorphic? }
```
I allowed for :has_many_association to pass through... and it turned out that RailsAdmin search works perfectly with it!

The SQL output for the Orders list action in RailsAdmin is below:

```sql
SELECT * FROM "orders" LEFT OUTER JOIN "orders_products" 
ON "orders"."id" = "orders_products"."order_id" 
LEFT OUTER JOIN "products" ON "products"."id" = "orders_products.product_id"
WHERE "orders"."id" IN (5469, 5448, 5447, 5436, 5428, 5384, 5007, 4960...)
AND (((products.name ILIKE '%BEER%')))
ORDER BY order.id desc
```

There is a more exquisite solution to the same problem in the form of [a pull request](https://github.com/sferik/rails_admin/issues/1434) that never got accepted into the official RailsAdmin repo. Use it at your own risk and watch the performance closely.


