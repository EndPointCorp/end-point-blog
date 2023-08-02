---
title: Upgrade Vue to TypeScript
author: Nicholas Piano
github_issue_number: 2001
date: 2023-08-02
tags:
- vue
- typescript
---

![The view from a mountain ridge. the sky is light blue and partially covered in clouds. Green ridges covered in pine trees lead down to a flat valley populated by a small town.](/blog/2023/07/unix-tools/idaho-mountains.webp)

<!-- Photo by Seth Jensen, 2023. -->

### Introduction

It's important to keep your code up to date. This is especially true for web development as the landscape changes so quickly. I recently upgraded a Vue project to exclusively use Vuex. This was a great opportunity to also upgrade the project from JavaScript to TypeScript. This article will cover the steps I took to upgrade the project.

Some of the changes can be difficult to understand if you are not familiar with TypeScript. I recommend reading the [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) if you are not familiar with TypeScript.

The primary problem to deal with when considering data type in Vue is the `data` property. The `data` property is a function that returns an object. This object is the data that is available to the Vue component. The problem is that TypeScript does not know what the data is. This is because the data is not defined in the component. It is defined in the function that returns the data. This means that TypeScript cannot infer the data type. The solution is to define the data type in the component. This is done by defining an interface that describes the data. The interface is then used to define the data type in the component.

### Installation

Before you begin, make sure the necessary dependencies are installed:

```
~$ vue add typescript
```

Also make sure that VueX is installed:

```
~$ yarn add vuex@next
```

### Conclusion
