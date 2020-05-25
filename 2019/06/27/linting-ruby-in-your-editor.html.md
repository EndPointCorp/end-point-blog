---
author: "Patrick Lewis"
title: "Linting Ruby In Your Editor"
tags: ruby, vim, emacs, visual-studio-code, tools
gh_issue_number: 1533
---

<img src="/blog/2019/06/27/linting-ruby-in-your-editor/banner.jpg" alt="Cotton" /> [Photo](https://flic.kr/p/azENYB) by [Kimberly Vardeman](https://www.flickr.com/people/kimberlykv/), used under [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)

Ruby developers have access to a variety of [linters](https://en.wikipedia.org/wiki/Lint_(software)) and [static program analysis](https://en.wikipedia.org/wiki/Static_program_analysis) tools that can greatly improve developer efficiency and code quality by catching syntax errors, detecting [code smells](https://en.wikipedia.org/wiki/Code_smell), and making coding style suggestions based on popular style guides.

I have been a long-time advocate of configuring development environments with automatic code linting and will use this post to highlight some of the available tools for Ruby and methods for integrating them with popular code editors (Vim, Emacs, and Visual Studio Code).

Configuring your editor for automatic linting makes it much easier to identify and fix issues with your code at development time, and in-editor integration is very convenient for highlighting problems as you type (or save), making it easy to evaluate and improve the quality of your code as it is written.

Three popular linting plugins/extensions for Vim, Visual Studio Code, and Emacs are:

### [Asynchronous Lint Engine (ALE)](https://github.com/w0rp/ale) Plugin for Vim

Provides asynchronous linting in Vim while you edit, and displays warnings/error messages in the editor. Supports the following tools for Ruby development and runs them automatically if they are found in your PATH:

* [brakeman](https://brakemanscanner.org)
* [rails_best_practices](https://github.com/flyerhzm/rails_best_practices)
* [reek](https://github.com/troessner/reek)
* [rubocop](https://github.com/rubocop-hq/rubocop)
* [ruby -wc](https://www.ruby-lang.org/en/) (verbose syntax check)
* [rufo](https://github.com/ruby-formatter/rufo)
* [solargraph](https://solargraph.org)
* [standardrb](https://github.com/testdouble/standard)

### [Ruby](https://marketplace.visualstudio.com/items?itemName=rebornix.Ruby#linters) Extension for Visual Studio Code

Requires configuring the settings JSON file to enable each tool on an individual basis:

```json
// Basic settings: turn linter(s) on
"ruby.lint": {
	"reek": true,
	"rubocop": true,
	"ruby": true, //Runs ruby -wc
	"fasterer": true,
	"debride": true,
	"ruby-lint": true
},
```

* [debride](https://github.com/seattlerb/debride)
* [fasterer](https://github.com/DamirSvrtan/fasterer)
* [reek](https://github.com/troessner/reek)
* [rubocop](https://github.com/rubocop-hq/rubocop)
* [ruby -wc](https://www.ruby-lang.org/en/) (verbose syntax check)
* [ruby-lint](https://gitlab.com/yorickpeterse/ruby-lint) (unmaintained)

### [Flycheck](https://www.flycheck.org/en/latest/) Extension for Emacs

Detects and uses the following tools when editing Ruby code:

* [reek](https://github.com/troessner/reek)
* [rubocop](https://github.com/rubocop-hq/rubocop)
* [ruby -wc](https://www.ruby-lang.org/en/) (verbose syntax check)
* [ruby-lint](https://gitlab.com/yorickpeterse/ruby-lint) (unmaintained)

### Linter Selection

I suggest starting small and only installing one or two linters to begin with; some choices provide similar features and will display conflicting or redundant warnings/errors if used at the same time. I think that [RuboCop](https://github.com/rubocop-hq/rubocop) is a great first choice, and I have spent years using it as my primary linter, though recently I have started supplementing it with [Reek](https://github.com/troessner/reek) and [Fasterer](https://github.com/DamirSvrtan/fasterer).

I highly recommend the use of these tools and consider them essential for any Ruby developer that is interested in improving the quality, reliability, and maintainability of their code.
