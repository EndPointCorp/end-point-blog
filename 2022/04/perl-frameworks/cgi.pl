#!/usr/bin/env perl

use utf8; 
use strict;
use warnings;
use CGI;

my $q = CGI->new;
print $q->header;
my $name = 'Marco';
print $q->p("Hello $name");
print "\n";



