---
author: David Christensen
gh_issue_number: 390
tags: database, interchange, perl
title: 'Character encoding in perl: decode_utf8() vs decode(''utf8'')'
---

When doing some recent encoding-based work in Perl, I found myself in a situation which seemed fairly unexplainable.  I had a function which used some data which was encoded as UTF-8, ran Encode::decode_utf8() on said data to convert to Perl's internal character format, then converted the "wide" characters to the numeric entity using HTML::Entities::encode_entities_numeric().  Logging/printing of the data on input confirmed that the data was properly formatted UTF-8, as did running `iconv -f utf8 -t utf8 output.log >/dev/null` for the purposes of review.

However when I ended up processing the data, it was as if I had not run the decode function at all.  In this case, the character in question was € (unicode code point U+20AC).  The expected behavior from encode_entities_numeric() would be to turn any of the hi-bit characters in the perl string (i.e. all Unicode code points > 0x80) into the corresponding numeric entity (€ - &#x20AC; in this case).  However instead of that specific character's numeric entity appearing in the output, the entities which appeared were: &#xE2;&#x82;&#xAC; i.e., the raw UTF-8 encoded value for €, with each octet being treated as an independent character instead of part of the whole encoded value.

What was particularly confusing was that extracting the relevant parts from the script in question resulted in the expected answer, so it was clearly not an issue of HTML::Entities not being able to deal with Unicode characters, as this code snippet demonstrates:

```bash
$ perl -MHTML::Entities+encode_entities_numeric -MEncode -e '$c=qq{\xE2\x82\xAC}; print encode_entities_numeric(decode_utf8($c))'
--> &#x20AC;
```

In the actual non-extracted version of the code, I was scratching my head.  This was exhibiting the signs of doubly-encoded data, however I couldn't see how that could be the case.  There were no PerlIO layers (e.g., :utf8 or :encoding) at play, the data I was outputting to a log file for verification purposes was being written via a brand new filehandle from a bare open(); I verified in multiple ways that the raw octets being passed in to the function were not doubly-encoded (printing the raw character points, counting lengths of the runs of octets and verifying that these matched the length of the UTF-8 encoded value for the represented characters, etc).  The more things I tried the more puzzled I got.  Finally, I changed the Encode::decode_utf8() call to a Encode::decode('utf8') one, providing the encoding explicitly.  At this point, the processing pipeline started working as expected, and hi-bit characters were being output as their full numeric entities.

Since the documentation for decode_utf8 indicated that it should be identical to decode('utf8'), I resorted to the code to find out why it worked with the version that specified the encoding explicitly.  I found that decode_utf8() does one additional thing that the regular decode('utf8') does not, and that is that before processing via the regular decode() function, decode_utf8 first checks the UTF-8 flag of the data that is being passed in, and if it is set it returns the data without further decoding*.  My best guess is that this is to prevent errors if someone attempts to decode UTF-8 data in a string which is already in Perl's internal format, so in most cases this will provide a caller-friendly interface that will DWYM in many expected cases.

Armed with this knowledge, I verified that for some reason, the data that was being passed into the function had the UTF-8 flag set, so using the explicit decode('utf8') in lieu of decode_utf8() fixed the issue for me.  (Tracing down the reason for the UTF-8 flag being set on this data was out of scope for this exercise, but is the true fix.)  And just to verify that this was in fact the cause of the issue at hand, here's our example, modified slightly (we use the utf8::upgrade function to turn the UTF-8 flag on in the data and treat as actual encoded characters instead of raw octets):

```bash
$ perl -l -MHTML::Entities+encode_entities_numeric -MEncode -Mutf8 -e '$c=qq{\xE2\x82\xAC}; utf8::upgrade($c); print encode_entities_numeric(decode_utf8($c))'
--> &#xE2;&#x82;&#xAC;
```

*  The UTF-8 flag is more or less an implementation detail of how Perl is able to deal with legacy 8-bit binary data in no particular encoding (i.e., raw octets, which it treats as latin-1) as well as the full range of Unicode data, and deal with both efficiently and in a backwards-compatible manner.
