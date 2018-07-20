---
author: Sonny Cook
gh_issue_number: 323
tags: perl, testing
title: Mock Testing with Perl
---



I’ll start by saying that I probably should have started with [Test::MockObject](https://metacpan.org/pod/release/CHROMATIC/Test-MockObject-1.09/lib/Test/MockObject.pm) and saved myself all of this trouble. But sometimes things don’t work out that way.

So, I’m building unit tests in Perl the hard way. By the hard way, I mean that I am constructing ever more elaborate, interdependent, complex, and brittle test data sets to test the functions that I am hacking on. The data model is moderately complex, so there really isn’t any way around it (since I’m doing it the hard way, after all).

At one point, one function (which I am not testing) returns a result that I need for the function I am testing. The problem is that it reaches pretty far away into a section of the data model that I’d rather not set up test data for at the moment just to get that one value. This is where I’m sitting there wishing I had mock objects more than usual, since this would be a perfect place to mock the method. Since I couldn’t be bothered to see if someone had written such a handy module, I looked for a hard way to do it. Turns out that there is one.

It’s not actually hard, but it could be considered complex if you are not familiar with typeglobs and the workings of the symbol table in Perl. A good discussion can be found in the Perl Cookbook in ch10.14.

In the following example, the function Base::Shipping::Package::weight is called at some point in create_shipment. Being able to call it is imperative to completing create_shipment. In my case, I have to have a successful result from create_shipment in order to test process_shipment.

```perl
{
  local *Base::Shipping::Package::weight = \&test_weight
  my $shipment = $class->create_shipment($shipment);
  my $result = $class->process_shipment($shipment);
  test $result;
}

sub test_weight { 4.0 }
```

In here then, the local call redefines the weight function inside the scope of the block. This turns out to be fairly convenient given that I already had the structure in place to test things this way. There are possibly other cases where something like this might make more sense than using Test::MockObject in the first place although I am somewhat skeptical.


