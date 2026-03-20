---
author: Edgar Mlowe
title: "Why I Am Focusing on Intelligent Document Processing"
description: "How looking at real project patterns led me to discover IDP, a fast-growing field in enterprise AI."
date: 2026-03-20
tags:
- artificial-intelligence
- IDP
- career
- data-processing
- opinion
---

[AI moves fast. A new model drops, a new framework launches, a new thing comes out, and suddenly what you learned last month feels old. LLMs, agents, fine-tuning, RAG, computer vision, multimodal models, prompt engineering, AI coding tools. The list keeps growing and it is hard to know where to focus.

Recently I decided to stop trying to follow all of it and focus on one area. In this post, I will explain what that area is, how I found it, and why I think it is worth paying attention to.

### The problem with being an AI generalist

When AI started becoming a practical tool for software engineers (not just researchers), I jumped in. I wrote about [deploying LLMs with Mixture of Experts](/blog/2025/06/deploying-llms-efficiently-with-mixture-of-experts/), built an [LLM-powered blog search](/blog/2025/09/llm-expanded-vector-search/), and worked on [AI extraction pipelines for document processing](/blog/2026/03/why-ai-extractor-fails-on-msg-emails-and-how-to-fix-decoding/). At work, our team was building document processing systems with LLMs. On the side, I was reading about everything else.

I was learning a lot, but I could not clearly say what I specialize in. If someone asked, "What is your thing in AI?" my answer was too broad to be useful.

### Looking at the pattern in the projects

The turning point was stepping back and looking at the projects I had been involved in. Not the articles I had been reading, but the real systems I had been working on with the team.

At End Point, one of the main projects our team has been working on is an order AI processing system. The problem was simple: a client receives purchase orders from dealers and resellers via multiple channels including email. PDFs, attachments, sometimes just email body text. Before the solution, someone had to open each email, read what was being ordered, and manually type the data into the ERP system. Invoicing addresses, delivery addresses, line items, quantities, all entered by hand.

The solution is a pipeline that takes those raw email exports and PDF attachments, extracts structured data using LLMs with a defined schema, validates the output, handles exceptions through a human-in-the-loop review step, and produces a clean CSV that imports directly into the ERP. No more manual data entry.

Looking at these projects, I started seeing the same pattern repeat. Different industries, different source documents, different target systems. But the same core problem:

**Unstructured data in > AI extraction and validation > Structured data out > Business system integration.**

### That pattern has a name

I thought this was just a type of project that kept showing up. But when I researched it, I found out it is an established market with a formal name: **Intelligent Document Processing (IDP)**.

IDP is about using AI (OCR, NLP, LLMs, computer vision) to automatically extract, classify, and transform data from unstructured documents like PDFs, emails, scanned forms, images, and legacy files into structured formats that plug into business systems.

This is not something small. Major research firms track it:

- [Gartner](https://www.gartner.com/reviews/market/intelligent-document-processing-solutions) publishes a Market Guide for Intelligent Document Processing Solutions
- [Everest Group](https://www.everestgrp.com/intelligent-document-processing-idp) releases annual IDP State of the Market reports
- [IDC](https://www.processexcellencenetwork.com/tools-technologies/news/idc-rates-22-intelligent-document-processing-idp-vendors) rated 22 IDP vendors in their some of their MarketScape assessment

The vendor landscape includes names you already know: Google ([Document AI](https://cloud.google.com/document-ai)), Microsoft ([Azure Document Intelligence](https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence)), Amazon ([Textract](https://aws.amazon.com/textract/)), ABBYY, UiPath, Automation Anywhere, and many more.

### The market is real and growing fast

The numbers vary by research firm because they define the market scope differently, but they all point in the same direction:

| Source | 2024-2026 Estimate | Projected By 2034 | Annual Growth |
|---|---|---|---|
| [Precedence Research](https://www.precedenceresearch.com/intelligent-document-processing-market) | $4.3B (2026) | $43.9B | ~34% per year |
| [Fortune Business Insights](https://www.fortunebusinessinsights.com/intelligent-document-processing-market-108590) | $14.2B (2026) | $91.0B | ~26% per year |
| [Research Nester](https://www.researchnester.com/reports/intelligent-document-processing-market/4826) | $3.8B (2025) | $39.5B | ~26% per year |

Growing at 26-34% per year makes IDP one of the fastest-growing areas in enterprise AI. A [McKinsey global survey](https://www.mckinsey.com/capabilities/operations/our-insights/the-next-horizon-for-industrial-operations-six-cross-industry-trends) found that 70% of organizations are already testing automation of document workflows, and close to 90% plan to scale these efforts across their whole company.

This matters because market growth creates demand for people who can actually build these systems. Not just people who buy vendor platforms, but people who can design extraction schemas, debug LLM outputs, build validation pipelines, and connect everything to real business systems.

### What skills matter in IDP

Knowing the field has a name also made it clear what skills matter most. IDP work sits at the intersection of a few areas:

- **LLM-based data extraction**: schema design, prompt engineering for structured output, few-shot examples for edge cases
- **Document parsing**: handling PDFs, emails (.msg, .eml), scanned documents, HTML exports
- **Data validation and QA**: confidence scoring, exception routing, human-in-the-loop review workflows
- **Pipeline architecture**: from document intake to extraction, normalization, validation, and output
- **Business system integration**: understanding ERP and CRM import formats, APIs, and data models


### Why this matters

When a client has purchase orders stuck in email inboxes that nobody can process fast enough, what they need is a reliable pipeline that extracts the right fields, handles the edge cases (like [character encoding issues in .msg files](/blog/2026/03/why-ai-extractor-fails-on-msg-emails-and-how-to-fix-decoding/)), validates the output, and delivers a clean import file.

That is what IDP is about: turning data that businesses already have but cannot use into data that their existing systems can act on. Structured, validated output that goes into the ERP, the CRM, or the database, and saves real time and money.

### Final thoughts

AI is broad enough that no one person can master all of it. But looking at the projects I was actually working on, instead of trying to follow every new trend, made it much easier to find direction.

In my case, that field turned out to be Intelligent Document Processing.](https://github.com/Mloweedgar/end-point-blog/edit/main/2026/03/why-i-am-focusing-on-intelligent-document-processing.md)
