---
author: David Christensen
gh_issue_number: 477
tags: database, postgres, tools
title: Announcing pg_blockinfo!
---



I'm pleased to announce the initial release of [pg_blockinfo](http://github.com/machack666/pg_blockinfo/). It is a tool to examine your PostgreSQL heap data files, written in Perl.

Similar in purpose to pg_filedump, it is used to display (and soon validate) buffer-page-level information for PostgreSQL page/heap files.

pg_blockinfo aims to work in a portable and non-destructive way, using read-only "mmap", sys-level IO functions, and "unpack" in order to minimize any Perl overhead.

What we buy for the compromise of writing this in Perl instead of C is two-fold:

1. **portability/low impact** — pg_blockinfo has no other dependencies than Perl and several core Perl modules and will work in environments where you can't or won't easily install other packages or compile based on specific headers.

1. **expressibility** — while not currently supported in full, one of pg_blockinfo's future goals is to allow you to specify criteria for display of both page-level and tuple-level info.  It will allow you to define arbitrary Perl expressions to filter the objects you're looking at (i.e., pages, tuples, etc; think "grep" but on a tuple level).  It will support a DSL for querying based off of the named fields as well as allow you to supply arbitrary Perl for scanning for any criteria.

## Requirements

We require a perl version with PerlIO ":mmap" support, which basically means any perl >= 5.8.  We do not require any non-core perl modules; currently we only use Data::Dumper and Getopt::Long for debugging and option parsing respectively, the former only when requested.

## Getting pg_blockinfo

The canonical git repo for development for pg_blockinfo is located at github: [http://github.com/machack666/pg_blockinfo/](http://github.com/machack666/pg_blockinfo/)

.

For the development repo, simply run:

```bash
$ git clone git://github.com/machack666/pg_blockinfo.git
```

Or you can just grab the current script directly [here](https://raw.github.com/machack666/pg_blockinfo/master/pg_blockinfo).

## Using pg_blockinfo

To get help including available options, canonical and alternate/abbreviated names of recognized fields, range syntax:

```bash
$ pg_blockinfo -h
```

To dump all fields for all page headers for all pages in a relation:

```bash
$ pg_blockinfo /path/to/relfile
```

To include only specific fields in the output you can specify multiple -f options and/or include multiple options per -f argument by comma delimiting.  Field specifiers are processed in order, so only the final logical set will be included.

"all" is a special shorthand type which will expand to all known columns.  pg_blockinfo may support other shorthand groups in the future.  When no fields are provided explicitly, "all" is implicitly assumed.

There are both positive and negative field inclusions.  An example of a positive inclusion is:

```bash
$ pg_blockinfo /path/to/relfile -f prune_xid,tli
```

This will display only the indicated fields in question for all blocks in relfile.  To include all fields *except* certain ones, prefix their name with a '-' sign:

```bash
$ pg_blockinfo -f -pagesize_version /path/to/relfile
```

This will display all page header fields in all blocks with the exception of the pagesize_version header field.

One consequence of the way these field display options are designed (particularly going forward with additional field/tuple display options) that you could define a "view" of the column data using a shell alias, then add/remove columns/criteria by passing additional -f options to it:

```bash
# using this as a shorthand to display just those fields
$ alias lsn='pg_blockinfo -f lsn_seq,lsn_off,tli'
$ lsn -f -tli /path/to/foo                          # remove fields from the display
$ lsn -f prune_xid /path/to/foo                     # or add to the list as well
```

Similar functionality is available for selecting the specific blocks available using the range option (-r or -b), which lets you specify a range of blocks to look at instead of the entire file.

```bash
$ pg_blockinfo -r 2-49 /path/to/relfile
$ pg_blockinfo -r -100 /path/to/relfile
$ pg_blockinfo -r 2,4,120-140,0xFF-0x1100 /path/to/relfile
```

Range options can be provided multiple times, each with one or more comma-delimited block-range specifications.  Blocks are numbered from 0, can be provided in decimal or hexadecimal (when prefixed via 0x), and can appear singly or in a range (unbounded or unbounded) when separated by a hyphen.

## Planned future features/TODO

In no particular order:

- dump tuples/tuple headers.
- better output/interpretation of bitflags.
- support alternate structures to allow detection/specification of different target versions of the page/tuple headers.
- allow querying/filtering pages/tuples.
- validation/sanity checking of various pages.
- actual extraction of ranges in the heap file.
- extract/dump tuples by raw ctid.
- allow arbitrary expressions to define powerful filtering options when querying/displaying information about the tuples/data files.
- detections of invalid toast tuple pointers/corrupted lz_compressed data (will require connection to theactive system catalog).
- detect relfile type?
- mvcc queries against tuples at a given arbitrarily-constructed snapshot
- detect xids that are invalid (i.e. map to non-existent pages in the pg_clog directory).
- better/shorter name?

I look forward to any feedback, patches, or other improvements/interest.


