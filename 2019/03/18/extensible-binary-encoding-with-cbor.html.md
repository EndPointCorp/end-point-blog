---
author: "Matt Vollrath"
title: "Extensible Binary Encoding with CBOR"
tags: performance, optimization, browsers, scalability, nodejs, benchmarks
gh_issue_number: 1509
---

<img src="/blog/2019/03/18/extensible-binary-encoding-with-cbor/convert-crop.png" alt="illustration of man converting something in a machine" />

[//]: # (freely usable without royalty or attribution, from https://gallery.manypixels.co/license)

CBOR is a relatively new IETF draft standard extensible binary data format. Compared to similar formats like MessagePack and BSON, CBOR was developed from the ground up with clear goals:

> 1. unambiguous encoding of most common data formats from Internet standards
> 2. code compactness for encoder and decoder
> 3. no schema description needed
> 4. reasonably compact serialization
> 5. applicability to constrained and unconstrained applications
> 6. good JSON conversion
> 7. extensibility
>
> —[RFC 7049](https://tools.ietf.org/html/rfc7049) Appendix E, Copyright © 2013 IETF Trust, Bormann & Hoffman

In the context of data storage and messaging, most developers can relate to CBOR as a binary drop-in replacement for JSON. While CBOR doesn’t share the human readability of JSON, it can efficiently and unambiguously encode types of data that JSON struggles with. CBOR can also be extended with tags to optimize serialization beyond its standard primitives.

### Encoding Binary Data

JSON is a ubiquitous data format for web and beyond, for many good reasons, but encoding blobs of binary data is an area where JSON falters. For example, if you are designing a JSON protocol to wrap the storage or transfer of arbitrary objects, your options are:

- Require that all input data can be represented as JSON. When possible this is potentially a reasonable solution, but limits the types of data that can be encoded. Notable exceptions include most popular image encodings, excluding SVG.
- Base64 encode any binary data values to a string. This can encode any binary data, but increases the size of the data by a minimum of 1/3, incurs encoding and decoding cost, and requires magic to indicate that the string is Base64 encoded.
- Encode the bytes as an array of numbers or a hex string. These are probably not things you should do, but it seemed worth mentioning that these techniques increase the size of the data by anywhere from 2x to 5x and also require magic to indicate that the data is really binary.

With CBOR, binary blobs of any length are supported out of the box and are encoded 1:1. Encoding and decoding CBOR byte strings is extremely fast, even in higher-level languages. In the case of JavaScript, CBOR byte strings can be transcoded to and from the very fast and efficient `Uint8Array`.

For example, let’s try encoding a simple object with two fields: “name” and “data”. An abstract view of this object:

```plain
name: "Strawberry Pie"
data: <00 01 02 03 04 05 06 07 08 09>
```

A C struct of this raw data would be absolute minimum of 24 bytes.

If you Base64 the data into JSON, your output might look like this:

```json
{"name":"Strawberry Pie","data":"AAECAwQFBgcICQ=="}
```

Length: 51 bytes.

This illustrates the “magic” problem with Base64 encoding binary data in JSON. Unless you have a JSON schema or special protocol fields, the decoder has no indication that the data in this object needs to be Base64 decoded, because it looks like a string. It is not self-describing.

The CBOR representation of the same input data, as a hex string:

```
a2646e616d656e5374726177626572727920506965696a7065675f646174614a00010203040506070809
```

Whoa, there. What do all these numbers and letters mean? I miss my JSON! The Node [cbor](https://www.npmjs.com/package/cbor) package has a handy [`cbor2comment` tool](https://github.com/hildjj/node-cbor/blob/master/bin/cbor2comment) to annotate this hex string for us.

```plain
  a2                -- Map, 2 pairs
    64              -- String, length: 4
      6e616d65      -- {Key:0}, "name"
    6e              -- String, length: 14
      5374726177626572727920506965 -- {Val:0}, "Strawberry Pie"
    64              -- String, length: 4
      64617461 -- {Key:1}, "data"
    4a              -- Bytes, length: 10
      00010203040506070809 -- {Val:1}, 00010203040506070809
```

Length: 35 bytes.

Now let’s [benchmark JSON against CBOR using real JPEG data](https://github.com/mvollrath/cbor-bench). For this test I used a [modified version of cbor-js](https://github.com/mvollrath/cbor-js/tree/fast_byte_array_encoding), a library compatible with both Node and browsers, and encoded a 910,226 byte JPEG of strawberry rhubarb pie.

```plain
|                           | JSON      | CBOR    |
| :------------------------ | --------: | ------: |
| Median encoding time (ms) | 3.983     | 0.538   |
| Median decoding time (ms) | 3.151     | 0.006   |
| Encoded size (bytes)      | 1,213,676 | 910,262 |
```

As the numbers show, CBOR is both faster and more concise for this particular data. Also, CBOR pie tastes better.

![strawberry rhubarb pie](/blog/2019/03/18/extensible-binary-encoding-with-cbor/strawberry_pie.jpg)

Food always looks good in pictures!

### Optimizing CBOR with Tags

In the case of encoding homogeneous numeric arrays, CBOR encoders can struggle with optimizing the packing of the data. For example, if you have an array of floating point numbers in a higher-level language like Python or JavaScript, the CBOR encoder implementation won’t necessarily determine how many bits are required to encode the numbers, defaulting to the largest available. Additionally, each value in the array will be individually described as a floating point number. This increases the cost and size of the data considerably.

CBOR has an answer to this problem. The [Draft Typed Array Tags](https://datatracker.ietf.org/doc/draft-ietf-cbor-array-tags/?include_text=1) spec includes tags specifying typed arrays which happen to match JavaScript `TypedArray` flavors.

For example, let’s say you have a `Float32Array` with a few values:

```js
const floats = new Float32Array([1.234567, 2.345678, 3.456789]);
```

JSON has a really funny way of encoding a `Float32Array`, lookit all those bytes:

```json
{"0":1.2345670461654663,"1":2.3456780910491943,"2":3.456789016723633}
```

Length: 69 bytes.

If we were to help the encoder by sending it a regular `Array` it would still be pretty verbose, but the precision we weren’t using is truncated, so the overall length will vary wildly depending on the values in the `Array`:

```plain
[1.234567,2.345678,3.456789]
```

Length: 28 bytes.

The well-meaning Node cbor library can encode the `Float32Array` directly, but doesn’t try to optimize for size:

```plain
  83                -- Array, 3 items
    fb              -- Float, next 8 bytes
      3ff3c0c960000000 -- [0], 1.2345670461654663
    fb              -- Float, next 8 bytes
      4002c3f2e0000000 -- [1], 2.3456780910491943
    fb              -- Float, next 8 bytes
      400ba78100000000 -- [2], 3.456789016723633
```

Length: 28 bytes.

Look at all that wasted precision, 64 bits for each 32-bit float, this just won’t do! The CBOR spec allows you to “tag” data for special treatment. According to the [list of registered CBOR tags](https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml), “IEEE 754 binary32, little endian, Typed Array” is tag 85. The consecutive bytes of the three numbers follow.

```plain
  d8                --  next 1 byte
    55              -- Tag #85
      4c            -- Bytes, length: 12
        4b069e3f971f1640083c5d40 -- 4b069e3f971f1640083c5d40
```

Length: 15 bytes.

The contained 12 byte string is equivalent to the values in the ArrayBuffer underneath our Float32Array.

The CBOR decoder will spit out the tag alongside its associated blob, so our optimization is self-described. Now we need to ensure that a byte string with this tag is correctly converted to the typed array, minding endianness. In a mature JavaScript implementation, this is both easy and very fast. Because we encoded the values of the `ArrayBuffer` underneath a `Float32Array`, we can construct a new `Float32Array` from the `ArrayBuffer`.

```js
const floats = new Float32Array(bytes);  // assuming platform and bytes are same endianness!
```

This is a very scalable way to read and write arrays of numeric values into JavaScript.

### When to Use CBOR

As [King Crimson teaches us](https://youtu.be/9FBmHB-YoQw?t=57), “it doesn’t mean you should / just because you can.”

I’ve found CBOR useful as an alternative to JSON for large (>2kB) chunks of raw data or numeric arrays. In many other cases JSON is equivalent or superior, because most languages have native JSON encoding and decoding in their standard libraries. CBOR encoders are not always so optimized, but the gap is closing with wider adoption. Run your own tests and benchmarks on real data against real libraries before deciding to use CBOR.

Many readers will recognize that schemaful formats such as protocol buffers are an endgame for structured data. If the infrastructure demands make sense for your application, this is also a good way to go. If you’re working with an application that already uses JSON, the difference in development and maintenance costs of porting it to CBOR or protobuf-likes should be measured against the size and performance gains of each approach.

It’s tempting to let numbers alone decide what format to use, but don’t underestimate the value of JSON’s human readability for structured data. The value of human readability diminishes quickly when dealing with large numeric arrays or binary blobs, so once again CBOR is an appealing choice for these data.
