#!/usr/bin/env perl
use Dancer;
 
get '/' => sub {
    my $name = "Marco";
    return "Hello $name\n";
};
 
start;
