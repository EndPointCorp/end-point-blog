---
author: Piotr Hankiewicz
title: Sort product attribute options by the position property in Magento
github_issue_number: 1190
tags:
- ecommerce
- magento
date: 2016-01-11
---

### Introduction

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2016/01/sort-product-attribute-options-by/image-0.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2016/01/sort-product-attribute-options-by/image-0.jpeg"/></a></div>

Recently I was working with Magento 1.9.1, trying to get a list of dropdown attribute options sorted by the position property. However there is a known bug in Magento 1.9.1, where the position property is not respected.

I looked for a patch to fix this issue, however there was no official patch, and none of the available community fixes were good enough. So again, I needed to fix it by myself.

**Tip!** If you know how to apply a patch file it is [here](https://gist.githubusercontent.com/peter-hank/4d33c4cad7efd8441c99/raw/377a8894f3766f045f523768fb4c237cdc6ed2ab/magento-1.9-patch-sorted-attribue-options). If not, please continue.

### Part 1

We need to overwrite some Magento core code unfortunately. The good thing is that there is a cool way of doing this in Magento so we don’t need to overwrite the files directly, we need to create a local copy.

Copy app/code/Core/Mage/Catalog/Model/Resource/Product/Type/Configurable/Attribute/Collection.php file to app/code/local/Mage/Catalog/Model/Resource/Product/Type/Configurable/Attribute/Collection.php. You need to create the whole directory structure. If you use Unix system it is simple as: (running from Magento root)

```bash
mkdir -p app/code/local/Mage/Catalog/Model/Resource/Product/Type/Configurable/Attribute/
cp app/code/Core/Mage/Catalog/Model/Resource/Product/Type/Configurable/Attribute/Collection.php app/code/local/Mage/Catalog/Model/Resource/Product/Type/Configurable/Attribute/Collection.php
```

### Part 2

Fill a local file with a content from this source: [https://gist.github.com/peter-hank/c917394ea9f1171ddeb8](https://gist.github.com/peter-hank/c917394ea9f1171ddeb8)

### Notes

After these changes it will work as expected and attribute options will be sorted by a position set.

This fix should work for any Magento 1.9.* version.
