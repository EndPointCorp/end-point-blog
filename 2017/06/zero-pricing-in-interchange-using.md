---
author: Mark Johnson
title: Zero Pricing in Interchange using CommonAdjust
github_issue_number: 1315
tags:
- ecommerce
- interchange
date: 2017-06-26
---



Product pricing can be quite complex. A typical Interchange catalog will have at least one table in the ProductFiles directive (often products plus either options or variants) and those tables will often have one or more pricing fields (usually price and sales_price). But usually a single, static price isn’t sufficient for more complex needs, such as accessory adjustments, quantity pricing, product grouping--not to mention promotions, sales, or other conditional features that may change a product’s price for a given situation, dependent on the user’s account or session.

Typically to handle these variety of pricing possibilities, a catalog developer will implement a CommonAdjust algorithm. CommonAdjust can accommodate all the above pricing adjustments and more, and is a powerful tool (yet can become quite arcane when reaching deeper complexity).  CommonAdjust is enabled by setting the PriceField directive to a non-existent field value in the tables specified in ProductFiles.

To give an adequate introduction and treatise on CommonAdjust would be at a minimum its own post, and likely a series. There are many elements that make up a CommonAdjust string, and subtle operator nuances that instruct it to operate in differing patterns. It is even possible for elements themselves to return new CommonAdjust atoms (a feature we will be leveraging in this discussion). So I will assume for this writing that the reader is familiar generally with CommonAdjust and we will implement a very simple example to demonstrate henceforth.

To start, let’s create a CommonAdjust string that simply replaces the typical PriceField setting, and we’ll allow it to accommodate a static sales price:

```
ProductFiles products
PriceField 0
CommonAdjust :sale_price ;:price
```

The above, in words, indicates that our products live in the products table, and we want CommonAdjust to handle our pricing by setting PriceField to a non-existent field (0 is a safe bet not to be a valid field in the products table). Our CommonAdjust string is comprised of two atoms, both of which are settors of type database lookup. In the products table, we have 2 fields: sale_price and price. If sale_price is “set” (meaning a non-zero numeric value or another CommonAdjust atom) it will be used as it comes first in the list. The semicolon indicates to Interchange “if a previous atom set a price by this point, we’re done with this iteration” and, thus, the price field will be ignored.  Otherwise, the next atom is checked (the price field), and as long as the price field is set, it will be used instead.

A few comments here:

- The bare colon indicates that the field is not restricted to a particular table. Typically, to specify the field, you would have a value like “products:price” or “variants:price”. But part of the power of ProductFiles holding products in different tables is you can pick up a sku from any of them. And at that point, you don’t know whether you’re looking at a sku from products, variants, or as many additional tables as you’d like to grab products from. But if all of them have a price and sales_price field, then you can pick up the pricing from any of them by leaving the table off. You can think of “:price” as “*:price” where asterisk is “table this sku came from”.
- The only indicator that CommonAdjust recognizes as a terminal value is a non-zero numeric value. The proposed price is coerced to numeric, added on to the accumulated price effects of the rest of the CommonAdjust string (if applicable), and the final value is tested for truth. If it is false (empty, undef, or 0) then the process repeats.
- What happens if *none* of the atoms produce a non-zero numeric value? If Interchange reaches the end of the original CommonAdjust string without hitting a set atom, it will relent and return a zero cost.

At this point, we finally introduce our situation, and one that is not at all uncommon. What if I *want* a zero price? Let’s say I have a promotion for buy one product, get this other product for free. Typically, a developer would be able to expect to override the prices from the database optionally by leveraging the “mv_price” parameter in the cart. So, let’s adjust our CommonAdjust to accommodate that:

```
CommonAdjust $ ;:sale_price ;:price
```

The $ settor in the first atom means “look in the line-item hash for the mv_price parameter and use that, if it’s set”. But as we’ve discussed above, we “set” an atom by making it a non-zero numeric value or another CommonAdjust atom. So if we set mv_price to 0, we’ve gained nothing. CommonAdjust will move on to the next atom (sale_price database settor) and pick up that product’s pricing from the database.  And even if we set that product’s sale_price and price fields to 0, it means *everyone* purchasing that item would get it for free (not just our promotion that allows the item to be free with the specific purchase of another item).

In the specific case of using the $ settor in CommonAdjust, we *can* set mv_price to the keyword “free”, and that will allow us to price the item for 0. But this restricts us to *only* be able to use $ and mv_price to have a free item. What if the price comes from a complex calculation, out of a usertag settor? Or out of a calc block settor? The special “free” keyword doesn’t work there.

Fortunately, there is a rarely used CommonAdjust settor that will allow for a 0 price item in a general solution. As I mentioned above, CommonAdjust calculations can themselves return other CommonAdjust atoms, which will then be operated on in a subsequent iteration. This frees us from just the special handling that works on $ and mv_price as such an atom can be returned from *any* of the CommonAdjust atoms and work.

The settor of interest is >>, and according to what documentation there is on it, it was never even intended to be used as a pricing settor! Rather, it was to be a way of redirecting to additional modes for shipping or tax calculations, which can also leverage CommonAdjust for their particular purposes. However, the key to its usefulness here is thus: it does not perform any test on the value tied to it. It is set, untested, into the final result of this call to the chain_cost() routine and returned. And with no test, the fact that it’s Perly false as numeric 0 is irrelevant.

So building on our current CommonAdjust, let’s leverage >> to allow our companion product to have a zero cost (assuming it is the 2nd line item in the cart):

```
[calcn]
    $Items->[1]{mv_price} = '>>0';
    return;
[/calcn]
```

Now what happens is, $ in the first atom picks up the value out of mv_price and, because it’s a CommonAdjust atom, is processed in a second iteration. But this CommonAdjust atom is very simple: take the value tied to >> and return it, untested.

Perhaps our pricing is more complex than we can (or would like to) support with using $. So we want to write a usertag, where we have the full power of global Perl at our disposal, but we still have circumstances where that usertag may need to return zero-cost items. Using the built-in “free” solution, we’re stuck, short of setting mv_price in the item hash within the usertag, which we may not want to do for a variety of reasons. But using >>, we have no such restriction. So let’s change CommonAdjust:

```
CommonAdjust $ ;[my-special-pricing] ;:sale_price ;:price
```

Now instead of setting mv_price in the item, let’s construct [my-special-pricing] to do some heavy lifting:

```
UserTag my-special-pricing Routine <<EOR
sub {
    # A bunch of conditional, complicated code, but then ...
    elsif (buy_one_get_one_test($item)) {
        # This is where we know this normally priced item is supposed to be
        # free because of our promotion. Excellent!

        return '>>0';
    }
    # remaining code we don't care about for this discussion
}
EOR
```

Now we haven’t slapped a zero cost onto the line item in a sticky fashion, like we do by setting mv_price. So presumably, above, if the user gets sneaky and removes the “buy one” sku identified by our promotion, our equally clever buy_one_get_one_test() sniffs it out, and the 0 price is no longer in effect.

For more information on CommonAdjust, see the [Custom Pricing section of ‘price’ glossary entry](http://www.icdevgroup.org/docs/glossary/price.html). And for more examples of leveraging CommonAdjust for quantity and attribute pricing adjustments, see the [Examples section of the CommonAdjust document entry](http://www.icdevgroup.org/docs/confs/CommonAdjust.html#CommonAdjust_examples).


