---
author: Edgar Mlowe
title: "Making Blog Search Smarter with LLMs and Open WebUI"
github_issue_number: 
featured:
  image_url: 
description: "Using Open WebUI and LLMs to automatically expand search queries before vector similarity matching"
date: 2025-09-19
tags: 
 - search
 - api
 - open-source
 - artificial-intelligence
 - performance
 - tools
 - python
---




## Making Blog Search Smarter with LLMs and Open WebUI

We recently released  "LLM Expanded Search" for our blog's vector search. It builds on what we covered in our earlier posts about AI-powered search and vector search basics. Here's how we built it with our internal AI setup (Open WebUI running an OpenAI-compatible API), why it makes search better, and what's coming next.

- Announcement: https://www.endpointdev.com/blog/2025/08/vector-search-for-the-end-point-blog/
- Vector search overview: https://www.endpointdev.com/blog/2025/07/vector-search/

## What "LLM Expanded Search" actually does

Here's the basic idea: when you search for something, we first ask an LLM to come up with related terms and phrases. Then we search for all of those terms, not just your original query.

- Your search gets expanded by an open-source LLM through our AI portal (Open WebUI with an OpenAI-compatible API)
- Those extra terms give our vector index more ways to find posts that match what you're looking for
- We combine the results, remove duplicates, and sort by relevance before showing the best matches with snippets and links

This really helps with short or vague searches like "S3" where regular vector search might miss the relevant context.

## How it works

The frontend is pretty straightforward, our search bar has two options: regular Search (just hit Enter) or LLM Expanded Search (Shift/Ctrl/Command+Enter).

When you use expanded search, here's what happens:
- We call our Open WebUI endpoint with a prompt that asks for 8-15 related terms
- We turn both your original query and the expanded terms into embeddings
- We search our vector store with all these terms and combine the results
- Caching and rate limiting keep things fast and cheap

Here's a simple example of how we expand queries:

```python
from openai import OpenAI
import os

client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),   # e.g., http://openwebui.local/api/v1
    api_key=os.getenv("OPENAI_API_KEY")      # token managed in your environment
)

def expand_query(raw_query: str) -> list[str]:
    messages = [
        {
            "role": "system",
            "content": (
                "You expand a short search query into a concise, comma-separated list of "
                "synonyms and closely related phrases (8–15 items). No explanations."
            )
        },
        {"role": "user", "content": raw_query}
    ]
    res = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "local-llm"),
        messages=messages,
        temperature=0.2,
        max_tokens=200,
    )
    text = res.choices[0].message.content
    return [t.strip() for t in text.split(",") if t.strip()]
```

After that, we:

- Turn the original query and all expansions into embeddings
- Search the vector index for each term
- Combine results by relevance score, remove duplicates, and grab the top matches
- Format everything into nice snippets

## Why we chose Open WebUI

A few reasons made Open WebUI the right choice:

- It's open source and works great on-premises
- The OpenAI-compatible API means we can drop it into existing code
- We can use whatever models and inference backends we want
- It's easy to experiment with different prompts and workflows

## What's next: Moving more into Open WebUI

We're thinking about moving more of the search pipeline directly into Open WebUI workflows:

1. Query expansion (LLM)
2. Vector retrieval (custom tool that hits our index)

This would give us tighter integration, fewer network calls, simpler deployment, and make it easier to try new approaches.

## What you'll notice when using it

- Short searches work way better, you get more relevant results and fewer dead ends
- It's still experimental, so sometimes results might drift into related topics. Stick with regular "Search" if you want exact matches
- Most searches are pretty fast, and we cache common terms to keep things smooth

## Give it a try at our website [https://www.endpointdev.com/blog/](https://www.endpointdev.com/blog/)

Just use the search bar in our [header](https://www.endpointdev.com/blog/): Enter for regular search, or Shift/Ctrl/Command+Enter for LLM Expanded Search. 

Want to know more about why we built this? Check out the announcement and vector search posts linked above.

If you're interested in setting up LLM-expanded vector search or running something similar on-premises with Open WebUI, we'd love to help out.
