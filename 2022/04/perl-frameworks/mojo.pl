#!/usr/bin/env perl
use utf8;
use strict;
use warnings;

use Mojolicious::Lite;

get '/' => sub {
    my ($c) = @_;
    $c->stash(name => "Marco");
    $c->render(template => 'index');
};

app->start;

__DATA__
@@ index.html.ep
Hello <%= $name %>
