---
author: David Christensen
gh_issue_number: 597
tags: perl
title: Byte-swap an entire file using perl
---



I recently needed to byte-swap an input file, and came up with an easy way with perl:

```bash
$ perl -0777ne 'print pack(q{V*},unpack(q{N*},$_))' inputfile > outputfile
```

This will byte-swap 4-byte sequences.  If you need to byte-swap 2-byte sequences, you can just adjust the formats for pack/unpack to the lower-case version like so:

```bash
$ perl -0777ne 'print pack(q{v*},unpack(q{n*},$_))' inputfile > outputfile
```

(Of course there are more efficient ways to handle this, but for a quick and dirty job this may just be what you need.)

We use the -0777 option to ensure perl reads the input file in its entirety and doesn’t affect newlines, etc.


