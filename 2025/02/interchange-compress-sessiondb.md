---
author: "Mark Johnson"
title: "Interchange Compression for SessionDB"
date: 2025-02-15
tags:
- ecommerce
- interchange
---

New support for compression of sessions and more lists stored in a RDBMS has been added to core Interchange<sup>1</sup>.

A new module, `Vend::Util::Compress`, operates as a general interface for compressing and uncompressing scalar data in Interchange. The module currently offers hooks for the following compression algorithms:

* Zstd (preferred)
* Gzip
* Brotli

Additional algorithms can be easily added as needed.

`Vend::Util::Compress` exports `compress()` and `uncompress()` on demand. In scalar context, they return the reference to the scalar holding the transformed data. In list context, they return additional measurements from the process.

List `compress()` returns an array of:

* $ref
* $before_size
* $after_size
* $elapsed_time
* $alert

List `uncompress()` returns an array of:

* $ref
* $elapsed_time
* $alert

Any errors encountered when called in scalar context are written to the catalog error log. Errors encountered when called in list context are returned in $alert.

### Compression Performance Comparison

The following chart summarizes the results of running the same Interchange instance through several steps of session growth to measure performance and impact of the 3 supported compression algorithms. Tests ranged from a minimum session size of 68 kilobytes up to a maximum of 110 megabytes. Fields marked in green indicate the best performance of the particular parameter, across all algorithms, for the test of the given session size. Any fields marked in yellow indicate performance measurements reaching a level of concern. Any fields marked in red indicate measurements reaching a level of unacceptable performance in any typical situation.

![Results chart for tests of compression algorithms](/blog/2025/02/interchange-compress-sessiondb/compression_reduction_chart.png)

### Configuring Your Catalog to Use Vend::Util::Compress

To begin using session compression, add the new catalog configuration parameter, `SessionDBCompression`, set to one of the aforementioned compression algorithms. Note the values for specifying compression type to use are case-sensitive. To enable Zstd, e.g.,

```plain
SessionDBCompression Zstd
```

An empty value for the parameter bypasses compression. An invalid value logs an error and passes through the data unmodified. If the catalog is configured for file-based sessions, the setting has no impact.

The same compression applies to both sessions and more lists when MoreDB is also set.

### References

1. [https://www.interchangecommerce.org/](https://www.interchangecommerce.org/)
