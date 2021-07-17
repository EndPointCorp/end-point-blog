---
author: Steph Skardal
title: CRUD, RESTful, and JSON for Address Management in Interchange
github_issue_number: 504
tags:
- ecommerce
- interchange
- json
- perl
- rest
date: 2011-10-04
---



Recently, I worked on a large project for [Paper Source](https://www.papersource.com/) that introduced the functionality to allow users to split orders into multiple addresses, which is especially valuable during the holiday season for gift purchase. Paper Source runs on [Interchange](http://www.icdevgroup.org/i/dev), one of the ecommerce frameworks End Point is intimately familiar with.

<div class="separator" style="clear: both; text-align: left;">
<a href="/blog/2011/10/crud-restful-and-json-for-address/image-0.png" imageanchor="1" style="margin-left:1em; margin-right:1em"><img border="0" src="/blog/2011/10/crud-restful-and-json-for-address/image-0.png" width="740"/></a></div>

This project requires [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) functionality for address editing during the checkout process; users must be able to add, edit, list, and remove addresses to be assigned to the various items in the cart. Another challenge here is that both logged in and logged out users are required to have this functionality, where addresses modified by logged in users would persist between sessions, and addresses of logged out users are available during their session and destroyed after they end the session (or in Paper Source’s case, when they close the browser window).

With these requirements, I set off to develop an architecture that followed [RESTful practices](https://en.wikipedia.org/wiki/Representational_state_transfer), described below:

### Listing Addresses

A Perl module contains a method for listing user addresses, which is shown below in simplified form. The user_addresses scratch variable is created and contains an array of hashed addresses. *For those unfamiliar with Interchange, [scratch space](http://www.icdevgroup.org/docs/glossary/scratch.html) is created as part of a user session which contains variables accessible throughout the user session or limited to a single page request. The Tag->tmpn call below sets the scratch variable accepting arguments key, value that is accessible during the current page request. This is not unlike setting a variable in a controller to be used in the view in MVC architecture.*

Also of note is the use of to_json, which transforms the address into JSON-ified form, which is used rather than manually looping through the addresses.

```perl
sub list {
  my $addresses;
  if($::Session->{username}) {    # user is logged in
    # $results = SELECT * FROM addresses WHERE username = ?
    foreach my $key (keys %$results) {
       push @$addresses, $results->{$key};
    }
  }
  else {
    $addresses = $::Session->{stored_addresses};
  }

  foreach my $address (@$addresses) {
    $address->{json} = to_json($address);
  }
  $:Tag->tmpn("user_addresses", $addresses);
  return;
}
```

In the HTML template, Interchange’s loop tag is used to loop through the addresses. Note: There may be a better way to avoid trailing commas in Interchange’s loop tag – please share it if you know the secret!

```nohighlight
<script type="text/javascript">
var addresses = {
[loop object.mv_results=`$Scratch->{user_addresses}`]
    'address_[loop-param id]': [loop-param json],[/loop]
    'dummy' : ''
};
</script>
```

For example, the above code might yield the JSON object shown below. These addresses are also used in the dropdowns shown in the screenshot at the beginning of this article.

```javascript
<script type="text/javascript">
var addresses = {
 'address_116971': {"country":"US","nickname":"Sister","fname":"Jackie", ... },
 'address_116969': {"country":"US","nickname":"Personal","fname":"Stephanie", ... },
 'dummy' : ''
};
</script>
```

### Creating an Address

Next, I added functionality for creating an address. Similar to the method above, the **add** subroutine is called with the use of a custom [Interchange Actionmap](http://interchange.rtfm.info/icdocs/config/ActionMap.html). The add method handles logged in and logged out use cases:

```perl
sub add {
  # do server-side error checking

  my $result;
  eval {
    my $address;
    if($::Session->{username}) {
      # store address in database with INSERT
      # $address is new address, with id of last_insert_id
    }
    else {
      # determine key to store address in session
      # store address in Session->{stored_addresses}
      # $address is new address, with key as id
    }
    $result = { address => to_json($address), success => 1 };
  };
  if($@) {
    $result = { error_msg => "Error: ...", success => 0 };
  }

  $::Tag->tmpn("result", to_json($result));
  $::CGI->{mv_nextpage} = "ajax/standard.html";  # sets HTML template used

  return;
}
```

This method was called via AJAX, which looks like this:

```javascript
$.ajax({
  url: "/address_management/add",
  data: address_data,  //parameterized address data
  dataType: "JSON",
  success: function(data) {
    if(data.success) {
      //updated addresses JavaScript variable
      //updated on page HTML (adds to dropdown)
    } else {
      //notifies user of errors
    }
  },
  failure: function(data) {
    //alert that could not process
  }
});
```

### Edit Address

The edit address functionality is similar to the code for creating an address, the only difference being that the database and Session variable was updated, and the URL called for editing is "/address_management/edit/:id". [Mustache](https://mustache.github.io/) is used to render the form prepopulated with the current address values.

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2011/10/crud-restful-and-json-for-address/image-1.png" imageanchor="1" style="margin-left:1em; margin-right:1em"><img border="0" src="/blog/2011/10/crud-restful-and-json-for-address/image-1.png" width="750"/></a></div>

### Remove Address

Finally, an address management page was created to include the ability to remove addresses. This method uses an AJAX method similar to the one shown above, and the Perl module contains the following:

```perl
sub remove {
  my ($self, $dbh) = @_;
  my $result;
  eval {
      # database DELETE FROM addresses
      $result->{success} = 1;
  };
  if ($@) {
      $result->{success} = 0;
  }

  $::Tag->tmpn("result", to_json($result));
  $::CGI->{mv_nextpage} = 'ajax/standard.html';
  return;
}
```

### Conclusion

The advantages to the RESTful CRUD methods described here is that the client side JavaScript and HTML code is reused for both logged in and logged out users. The server-side responds to all requests in a similar manner for both logged in and logged out use cases. Reusing client-side code eases maintenance because there is less code to support and less code to update when changes are necessary. Additionally, these CRUD methods are reused in the user address management page (shown below), which takes advantage of reusable server-side and client-side modular elements.

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2011/10/crud-restful-and-json-for-address/image-2.png" imageanchor="1" style="margin-left:1em; margin-right:1em"><img border="0" src="/blog/2011/10/crud-restful-and-json-for-address/image-2.png" width="615"/></a></div>

In addition to the work described here, quite a bit of work was done on the backend for order processing to create a new structure for storing addresses per order. Out of the box Interchange functionality stores the billing and shipping addresses in the transactions (orders) table, and individual item information in the orderlines table (item sku, quantity, price, etc.). With this new functionality, shipping addresses were pulled out of the transactions table into their own table (shipped_addresses), and orderline items mapped to these shipping addresses. To preserve historical order data, shipped_addresses is copied from addresses for logged in users and remains untouched by the user.

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr><td align="center" valign="top">Data Model Before<br/><img border="0" src="/blog/2011/10/crud-restful-and-json-for-address/image-3.png" width="250"/></td>
<td align="center" valign="top">Data Model After<br/><img border="0" src="/blog/2011/10/crud-restful-and-json-for-address/image-4.png" width="400"/></td></tr>
</tbody></table>

Paper Source has several special products, like gift cards and a large set of personalized products. Additional changes were required as well to accomodate the new data model. For example, a script that reported on gift card shipping addresses required updating to adhere to the new data structure.


