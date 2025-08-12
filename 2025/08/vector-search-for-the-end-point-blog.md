---
title: "Vector Search for the End Point Blog"
author: Seth Jensen
date: 2025-08-13
description: "Announcing AI-powered vector search, aka similarity search, for the End Point Blog"
featured:
  image_url: /blog/2025/08/vector-search-for-the-end-point-blog/trees-by-sidewalk.webp
github_issue_number: 2139
tags:
- company
- artificial-intelligence
---

![A sidewalk and road lead to the left of the image, across from an industrial area with train tracks. Along the sidewalk are trees with white petals, many of which have fallen to the sidewalk.](/blog/2025/08/vector-search-for-the-end-point-blog/trees-by-sidewalk.webp)

<!-- Photo by Seth Jensen, 2025 -->

We're excited to announce a new feature on the End Point Blog: AI-powered vector search.

Below the "Our Blog" header at the top of this page, there is a new search bar with two adjacent buttons: "Search" and "LLM Expanded Search." If you click "Search" (or press Enter), your search will be fed directly to our vector search/​similarity search engine. If you click "LLM Expanded Search" (or press Shift+Enter, Control+Enter, or Command+Enter on macOS) your query will first be expanded by an open-source LLM, then sent to the similarity search engine.

The LLM is trained to expand the query to include similar terms, keywords, etc., before sending it to the similarity search engine. For example, if I search `S3`, similarity search alone returns no results — there isn't enough semantic information for vector search to make useful connections. However, an LLM can expand this to `s3, simple storage service, amazon s3, object storage, cloud storage...`, providing more anchor points for vector search to connect to results.

The model improves results fairly well, but it is still an experimental technology, so results will vary. In the `S3` example, you could get posts which don't directly relate to Amazon S3, but relate to cloud object storage, or you could not get some posts which have an exact match of `S3` but not more semantic similarity.

You can read more about the technical side of vector search in our [recent blog post](/blog/2025/07/vector-search/).

Happy searching!
