---
author: Steph Skardal
gh_issue_number: 448
tags: performance, perl
title: 'Benchmarking in Perl: Map versus For Loop'
---



Last week, I was coding in Perl for an [Interchange](http://www.icdevgroup.org/i/dev) project. I've been in and out of Perl and Ruby a lot lately. While I was working on the project, I came across the following bit of code and wanted to finally sit down and figure out how to use the [map](http://perldoc.perl.org/functions/map.html) function in Perl on this bit of code.

```perl
my @options;
for my $obj (@$things) {
    push @options, {
        value => $obj->{a},
        label => $obj->{b}
    };        
}
return \@options;
```

I'm a big fan of Ruby's [inject method](http://www.ruby-doc.org/core/classes/Enumerable.html#M001494) and in general a fan of the [Enumerable Module](http://www.ruby-doc.org/core/classes/Enumerable.html), but I have a brain block when it comes to using the map method in both Perl and Ruby. I spent a little time investigating and working on a small local Perl script to test the implementation of the map method. I came up with the following:

```perl
return [ map {
    {
        value => $_->{a},
        label => $_->{b}
    }
} @$things ];
```

After that, I wanted to make sure the code change was justified. The Interchange application that is the source of this code is built for performance, so I wanted to ensure this change didn't hinder performance. It's been a while since I've done benchmarking in Perl, so I also had to refresh my memory regarding using the [Benchmark module](http://perldoc.perl.org/Benchmark.html). I came up with:

```perl
#!/usr/bin/perl

use Benchmark;

my $count = 1000000;
my $things = [
    {'a' => 123, 'b' => 456, 'c' => 789 },
    {'a' => 456, 'b' => 789, 'c' => 123 }
];

#Test definitions as methods to mimic use in application
my $test1 = sub {
    my @options;
    for my $obj (@$things) {
        push @options, {
            value => $obj->{a},
            label => $obj->{b} 
        };
    }
    return \@options;
};
my $test2 = sub {
    return [ map {
        { 
            value => $_->{a},
            label => $_->{b}
        }
    } @$things ];
};

#Benchmark tests & results.
$t0 = Benchmark->new;
$test1->() for(1..$count);
$t1 = Benchmark->new;
$td = timediff($t1, $t0);
print "the code for test 1 took:",timestr($td),"\n";

$t0 = Benchmark->new;
$test2->() for(1..$count);
$t1 = Benchmark->new;
$td = timediff($t1, $t0);

print "the code for test 2 took:",timestr($td),"\n";
```

The results were:

<table cellpadding="5" cellspacing="0" style="margin-left:20px;">
<tbody><tr>
<td>Test #</td>
<td>Before (For Loop)</td>
<td>After (Map)</td>
</tr>
<tr>
<td>1</td>
<td>5 sec</td>
<td>4 sec</td>
</tr>
<tr>
<td>2</td>
<td>5 sec</td>
<td>4 sec</td>
</tr>
<tr>
<td>3</td>
<td>5 sec</td>
<td>5 sec</td>
</tr>
<tr>
<td>4</td>
<td>5 sec</td>
<td>5 sec</td>
</tr>
<tr>
<td>5</td>
<td>6 sec</td>
<td>4 sec</td>
</tr>
<tr>
<td>6</td>
<td>6 sec</td>
<td>4 sec</td>
</tr>
<tr>
<td>7</td>
<td>6 sec</td>
<td>4 sec</td>
</tr>
<tr>
<td>8</td>
<td>5 sec</td>
<td>5 sec</td>
</tr>
<tr>
<td>9</td>
<td>5 sec</td>
<td>4 sec</td>
</tr>
<tr>
<td>10</td>
<td>5 sec</td>
<td>4 sec</td>
</tr>
<tr>
<td>Average</td>
<td>5.3 sec</td>
<td>4.3 sec</td>
</tr>
</tbody></table>

In this case, replacing the [imperative programming](http://en.wikipedia.org/wiki/Imperative_programming) style here with [Functional programming](http://en.wikipedia.org/wiki/Functional_programming) (via map) yielded a small performance improvement, but the script executed each method 1,000,000 times, so the performance gain yielded by just one method call is very small. I doubt it's worth it go on a code cleanup rampage to update and test this, but it's good to keep in mind moving forward as small bits of the code are touched. I also wonder if the performance will vary when the size of $things changes — something I didn't test here. It was nice to practice using Perl's map method and Benchmark module. Yippee.


