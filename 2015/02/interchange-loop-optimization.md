---
author: Mark Johnson
title: Interchange Loop Optimization
github_issue_number: 1089
tags:
- ecommerce
- interchange
- optimization
- performance
- perl
date: 2015-02-09
---



It’s important to understand both how loops work in Interchange and the (very) fundamental differences between interpolating Interchange tag language (ITL) and the special loop tags (typically referred to as [PREFIX-*] in the literature). Absent this sometimes arcane knowledge, it is very easy to get stuck with inefficient loops even with relatively small loop sets. I’ll discuss both the function of loops and interpolation differences between the tag types while working through a [query] example. While all loop tags--[item-list], [loop], [search-list], and [query]--process similarly, it is to [query] where most complex loops will gravitate over time (to optimize the initiation phase of entering the loop) and where we have the most flexibility for coming up with alternative strategies to mitigate sluggish loop-processing.

### Loop Processing

All loop tags are *container* tags in Interchange, meaning they have an open and close tag, and in between is the body. Only inside this body is it valid to define [PREFIX-*] tags (notable exception of [PREFIX-quote] for the sql arg of [query]). This is because the [PREFIX-*] tags are not true ITL. They are tightly coupled with the structure of the underlying rows of data and they are processed by distinct, optimized regular expressions serially. Outside the context of the row data from a result set, they are meaningless.

Moreover, the body of a loop tag is slurped into a scalar variable (as all bodies of container tags are handled via the ITL parser) and for each row in the record set of the loop, the contents are acted upon according to the [PREFIX-*] tags defined within the body. The first important distinction to recognize here is, the per-row action on this scalar is limited to *only* the [PREFIX-*] tags. The action occurring at loop time ignores any embedded ITL.

At the end of each row’s processing, the copy of the body tied to that one row is then concatenated to the results of all previous rows thus processed. For a loop with N rows (assuming no suppression by [if-PREFIX-*] conditionals) that means every instance of ITL originally placed into the loop body is now present N times in the fully assembled body string. Simple example:

```
[loop list='1 2 3']
[tmp junk][loop-code][/tmp]
[if scratch junk == 2]
I declare [loop-code] to be special!
[else]
Meh. [loop-code] is ordinary.
[/else]
[/if]
[/loop]
```

Once this result set with N=3 is processed, but **before** Interchange returns the results, the assembled return looks like the following string:

```
[tmp junk]1[/tmp]
[if scratch junk == 2]
I declare 1 to be special!
[else]
Meh. 1 is oridinary
[/else]
[/if]

[tmp junk]2[/tmp]
[if scratch junk == 2]
I declare 2 to be special!
[else]
Meh. 2 is oridinary
[/else]
[/if]

[tmp junk]3[/tmp]
[if scratch junk == 2]
I declare 3 to be special!
[else]
Meh. 3 is oridinary
[/else]
[/if]
```

Some important observations:

- It doesn’t take much ITL to turn a loop body into a monster interpolation process. One must consider the complexity of the ITL in the body by a factor of the number of rows (total, or the “ml” matchlimit value).
- ITL does *nothing* to short-circuit action of the [PREFIX-*] tags. Having [PREFIX-param], [PREFIX-calc], etc. inside an ITL [if] means all those loop tags parse regardless of the truth of the if condition.

### ITL vs. Loop Tags

ITL maps to routines, both core and user-defined, determined at compile time. They are processed in order of discovery within the string handed to the ::interpolate_html() routine and have varied and complex attributes that must be resolved for each individual tag. Further, for many (if not most) tags, the return value is itself passed through a new call to ::interpolate_html(), acting on all embedded tags, in an action referred to as *reparse*. There is, relatively speaking, a good deal of overhead in processing through ::interpolate_html(), particularly with reparse potentially spawning off a great many more ::interpolate_html() calls.

Loop tags, by contrast, map to a pre-compiled set of regular expressions. In contrast to crawling the string and acting upon the tags in the order of discovery, each regex in turn is applied globally to the string. The size of the string is limited to the exact size of the single loop body, and there is no analogue to ITL’s reparse. Further, given this processing pattern, a careful observer might have noted that the order of operations can impact the structure. Specifically, tags processed earlier cannot depend on tags processed later. E.g., [PREFIX-param] processes ahead of [PREFIX-pos], and so:

```
[if-PREFIX-pos 2 eq [PREFIX-param bar]]
```

will work, but:

```
[if-PREFIX-param bar eq [PREFIX-pos 2]]
```

will not. While the above is a somewhat contrived exampled, the impacts of loop tag processing can be more easily seen in an example using [PREFIX-next]:

```
[PREFIX-next][PREFIX-param baz][/PREFIX-next]
Code I only want to run when baz is false, like this [PREFIX-exec foo][/PREFIX-exec] call
```

Because [PREFIX-next] is the absolute last loop tag to run, *every other loop tag in the block is run* before the next condition is checked. All [PREFIX-next] does is suppress the resulting body from the return, unlike Perl’s next, which short-circuits the remaining code in the loop block.

### An Optimization Example

As long as you’re familiar with the idiosyncracies of [PREFIX-*] tags, you should make every effort to use them instead of ITL because they are substantially lighter weight and faster to process. A classic case that can yield remarkable performance gains is to directly swap an embedded [perl] or [calc] block with an equivalent [PREFIX-calc] block.

Let’s take a typical query with little consideration given to whether we use loop tags or ITL, not unlike many I’ve seen where the resource has just become unusably slow. This code originally was developed processing 50 records per page view, but the team using it has requested over time to increase that count.

```
[query
    list=1
    ml=500 [comment]Ouch! That's a big N[/comment]
    sql="
        SELECT *
        FROM transactions
        WHERE status = 'pending'
        ORDER BY order_date DESC
    "
]
Order [sql-param order_number]
[if global DEVELOPMENT]
    Show [sql-exec stats_crunch][sql-param stats][/sql-exec], only of interest to developers
[/if]
Date: [convert-date format="%b %d, %Y at %T"][sql-param order_date][/convert-date]
[if cgi show_inventory]
Inv:
[if cgi show_inventory eq all]
* Shipped: [either][sql-param is_shipped][or]pending[/either]
* Count: [inventory type=shipped sku=[sql-param sku]]
[/if]
* On Hand: [inventory type=onhand sku=[sql-param sku]]
* Sold: [inventory type=sold sku=[sql-param sku]]
* Shipping: [inventory type=shipping sku=[sql-param sku]]
[/if]
Order details:
    <a href="[area
                href=order_view
                form="
                    order=[sql-param order_number]
                    show_status=[either][cgi show_status][or]active[/either]
                    show_inventory=[cgi show_inventory]
                "
            ]">View [sql-param order_number]</a>
[/query]
```

Considering this block out of context, it doesn’t seem all that unreasonable. However, let’s look at some of the pieces individually and see what can be done.

- We use [if] in 3 different circumstances in the block. However, those values they test are static. They don’t change on any iteration. (We are excluding the potential of any other ITL present in the block from changing their values behind the scenes.)
- [convert-date] may be convenient, but it is only one of a number of ways to address date formatting. Our database itself almost certainly has date-formatting routines, but one of the benefits of [convert-date] is you could have a mixed format underlying the data and it can make sense out of the date to some degree. So perhaps that’s why the developer has used [convert-date] here.
- Good chance that stats_crunch() is pretty complicated and that’s why the developer wrote a catalog or global subroutine to handle it. Since we only want to see it in the development environment, it’d be nice if it only ran when it was needed. Right now, because of ITL happening on reparse, stats_crunch() fires for every row even if we have no intention of using its output.
- We need that link to view our order, but on reparse it means ::interpolate_html() has to parse 500 [area] tags along with [either] and [cgi] x 500. All of these tags are lightweight, but parsing numbers are really going to catch up to us here.

Our goal here is to replace any ITL we can with an equivalent use of a loop tag or, absent the ability to remove ITL logically, to wrap that ITL into a subroutine that can itself be called in loop context with [PREFIX-exec]. The first thing I want to address are those [if] and [either] tags, the lowest hanging fruit:

```
[query
    list=1
    ml=500
    sql="
        <b>SELECT *,
            '[if global DEVELOPMENT]1[/if]' AS is_development,
            [sql-quote][cgi show_inventory][/sql-quote] AS show_inventory,
            COALESCE(is_shipped,'pending') AS show_inventory_shipped</b>
        FROM transactions
        WHERE status = 'pending'
        ORDER BY order_date DESC
    "
]
Order [sql-param order_number]
<b>[if-sql-param is_development]</b>
    Show [sql-exec stats_crunch][sql-param stats][/sql-exec], only of interest to developers
<b>[/if-sql-param]</b>
Date: [convert-date format="%b %d, %Y at %T"][sql-param order_date][/convert-date]
<b>[if-sql-param show_inventory]</b>
Inv:
<b>[if-sql-param show_inventory eq all]</b>
* Shipped: <b>[sql-param show_inventory_shipped]</b>
* Count: [inventory type=shipped sku=[sql-param sku]]
<b>[/if-sql-param]</b>
* On Hand: [inventory type=onhand sku=[sql-param sku]]
* Sold: [inventory type=sold sku=[sql-param sku]]
* Shipping: [inventory type=shipping sku=[sql-param sku]]
<b>[/if-sql-param]</b>
Order details:
    <a href="[area
                href=order_view
                form="
                    order=[sql-param order_number]
                    show_status=[either][cgi show_status][or]active[/either]
                    show_inventory=[cgi show_inventory]
                "
            ]">View [sql-param order_number]</a>
[/query]
```

By moving those evaluations into the SELECT list of the query, we’ve reduced the number of interpolations to arrive at those static values to 1 or, in the case of the [either] tag, 0 as we’ve offloaded the calculation entirely to the database. If is_shipped could be something perly false but not null, we would have to adjust our field accordingly, but in either case could still be easily managed as a database calculation. Moreover, by swapping in [if-sql-param is_development] for [if global DEVELOPMENT], we have kept stats_crunch() from running at all when in the production environment.

Next, we’ll consider [convert-date]:

```
Date: [convert-date format="%b %d, %Y at %T"][sql-param order_date][/convert-date]
```

My first attempt would be to address this similarly to the [if] and [either] conditions, and try to render the formatted date from a database function as an aliased field. However, let’s assume the underlying structure of the data varies and that’s not easily accomplished, and we still want [convert-date]. Luckily, Interchange supports that same tag as a filter, and [PREFIX-filter] is a loop tag:

```
Date: <b>[sql-filter convert_date."%b %d, %Y at %T"]</b>[sql-param order_date]<b>[/sql-filter]</b>
```

[PREFIX-filter] is very handy to keep in mind as many transformation tags have a filter wrapper for them. E.g., [currency] -> [PREFIX-filter currency]. And if the one you’re looking at doesn’t, you can build your own, easily.

Now to look at that [inventory] tag. The most direct approach assumes that the code inside [inventory] can be run in Safe, which often it can even if [inventory] is global. However, if [inventory] does run-time un-Safe things (such as creating an object) then it may not be possible. In such a case, we would want to create a global sub, like our hypothetical stats_crunch(), and invoke it via [PREFIX-exec]. However, let us assume we can safely (as it were) invoke it via the $Tag object to demonstrate another potent loop option: [PREFIX-sub].

```
[if-sql-param show_inventory]
<b>[sql-sub show_inventory]
    my $arg = shift;
    return $Tag->inventory({ type => $arg, sku => $Row->{sku} });
[/sql-sub]</b>
Inv:
[if-sql-param show_inventory eq all]
* Shipped: [sql-param show_inventory_shipped]
* Count: <b>[sql-exec show_inventory]shipped[/sql-exec]</b>
[/if-sql-param]
* On Hand: <b>[sql-exec show_inventory]on_hand[/sql-exec]</b>
* Sold: <b>[sql-exec show_inventory]sold[/sql-exec]</b>
* Shipping: <b>[sql-exec show_inventory]shipping[/sql-exec]</b>
[/if-sql-param]
```

Let’s go over what this gives us:

- [PREFIX-sub] creates an in-line catalog sub that is compiled at the start of processing, before looping actually begins. As such, the [PREFIX-sub] definitions can occur anywhere within the loop body and are then removed from the body to be parsed.
- The body of the [PREFIX-exec] is passed to the sub as the first argument. We use that here for our static values to the "type" arg. If we also wanted to access [sql-param sku] from the call, we would have to include that in the body and set up a parser to extract it out of the one (and only) arg we can pass in. Instead, we can reference the $Row hash within the sub body just as we can do when using a [PREFIX-calc], with one minor adjustment to our [query] tag--we have to indicate to [query] we are operating on a row-hash basis instead of the default row-array basis. We do that by adding the hashref arg to the list:

```
[query
    list=1
    ml=500
    <b>hashref=1</b>
```

- We still have access to the full functionality of [inventory] but we’ve removed the impact of having to parse that tag 2000 times (in the worst-case scenario) if left as ITL in the query body. If we run into Safe issues, that same sub body can either be created as a pre-compiled global sub or, if available, we can set our catalog AllowGlobal in which case catalog subs will no longer run under Safe.

Finally, all we have left to address is [area] and its args which themselves have ITL. I will leverage [PREFIX-sub] again as an easy way to manage the issue:

```
<b>[sql-sub area_order_view]
    my $show_status = $CGI->{show_status} || 'active';
    return $Tag->area({
        href => 'order_view',
        form => "order=$Row->{order_number}\n"
              . "show_status=$show_status\n"
              . "show_inventory=$CGI->{show_inventory}",
    });
[/sql-sub]</b>
Order details:
    <a href="<b>[sql-exec area_order_view][/sql-exec]</b>">View [sql-param order_number]</a>
```

By packaging all of [area]’s requirements into the sub body, I can address all of the ITL at once.

So now, let’s put together the entire [query] rewrite to see the final product:

```
[query
    list=1
    ml=500
    hashref=1
    sql="
        SELECT *,
            '[if global DEVELOPMENT]1[/if]' AS is_development,
            [sql-quote][cgi show_inventory][/sql-quote] AS show_inventory,
            COALESCE(is_shipped,'pending') AS show_inventory_shipped
        FROM transactions
        WHERE status = 'pending'
        ORDER BY order_date DESC
    "
]
Order [sql-param order_number]
[if-sql-param is_development]
    Show [sql-exec stats_crunch][sql-param stats][/sql-exec], only of interest to developers
[/if-sql-param]
Date: [sql-filter convert_date."%b %d, %Y at %T"][sql-param order_date][/sql-filter]
[if-sql-param show_inventory]
[sql-sub show_inventory]
    my $arg = shift;
    return $Tag->inventory({ type => $arg, sku => $Row->{sku} });
[/sql-sub]
Inv:
[if-sql-param show_inventory eq all]
* Shipped: [sql-param show_inventory_shipped]
* Count: [sql-exec show_inventory]shipped[/sql-exec]
[/if-sql-param]
* On Hand: [sql-exec show_inventory]on_hand[/sql-exec]
* Sold: [sql-exec show_inventory]sold[/sql-exec]
* Shipping: [sql-exec show_inventory]shipping[/sql-exec]
[/if-sql-param]
[sql-sub area_order_view]
    my $show_status = $CGI->{show_status} || 'active';
    return $Tag->area({
        href => 'order_view',
        form => "order=$Row->{order_number}\n"
              . "show_status=$show_status\n"
              . "show_inventory=$CGI->{show_inventory}",
    });
[/sql-sub]
Order details:
    <a href="[sql-exec area_order_view][/sql-exec]">View [sql-param order_number]</a>
[/query]
```

Voila! Our new query body is functionally identical to the original body, though admittedly a little more complicated to set up. However, the trade-off in efficiency is likely to be substantial.

I recently worked on a refactor for a client that was overall very similar to the above example, with a desired N value of 250. The code prior to refactoring took ~70s to complete. Once we had completed the refactor using the same tools as I’ve identified here, we brought down processing time to just under 3s, losing no functionality.

Time taken optimizing Interchange loops will almost always pay dividends.


