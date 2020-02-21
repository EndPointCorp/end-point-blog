---
author: "Kevin Campusano"
title: "A Webpack 4 Primer: Setting up a modern JavaScript front end application"
tags: web development, front end development, javascript, webpack, module bundler, babel, ES2015, ES6
---

![Banner](/blog/2019/08/07/a-webpack-4-primer/banner.png)

I've got a confession to make: Even though I've developed many a JavaScript-heavy, client side project with complex build pipelines, I've always been somewhat confused by the engine that drives it all under the hood: [Webpack](https://webpack.js.org).

Up until now, when it came to set up a build system for front end development, I always deferred to some framework's default set up or some recipes discovered after some Googling or StackOverflow browsing. I never really understood Webpack in a detail level where I could feel confortable reading, understanding and modifying a config file.

This "learn enough to be effective" approach has served me well so far and it works great for being able to get something working, while also spending time efficiently. When everything works as it should, that is. This aproach starts to fall appart when weird, more obscure issues pop up and you don't know enough about the underlying system concepts to get a better idea of what could've gone wrong. Which can sometimes lead to frustrating Googling sessions accompanied with a healthy dose of trial and error. Ask me how I know...

Well, all that ends today. I've decided to go back to basics with Webpack and learn about the underlying concepts, components and basic configuration. Spoiler alert: it's all super simple stuff.

Let's dive in.

### The problem that Webpack solves

Webpack is a module bundler. That means that its main purpose is to take a bunch of disparate files and "bundling" them together into single, aggregated files. Why would we want to do this? Well, for modularity. I.e. to be able to write code that's modular.

Writing modular code is not as easy in JavaScript that runs in a browser as it is in other languages or environments. Traditionally, the way to achieve good modularity in the web front end has been via including separate scripts via multiple script tags. This approach comes with its own host of problems. Things like the order in which the scripts are included suddenly matter, because the browser executes them top to bottom, which means that you have to be very careful to include them in an order where dependencies of the later files are included first. Also, this approach encourages the pollution of the global scope, where every script file declares some global variables which are then used by other scripts. This is problematic because it is not clear which scripts depend on which ones. Unit testing becomes harder as well, since you need to mock these dependencies at a global scope. You also run the risk of some scripts overriding these global resources anytime. It's just not very clean.

Over the years, solutions have been devised by the community to solve this issue, which have taken the form of module loaders like CommonJS and AMD. Finally, ES2015 introduced a native module loading system into the language itself via the `import` statement. The life of JavaScript in the browser is not so easy though, as these new specifications take time to implement. This is where Webpack comes in. Part of its offerings is the ability to use this standard, modern module loading mechanism without having to worry about browser compatibility. Which unlocks the potential for front end developers to write modern, beautiful, modularized JavaScript. This is huge.

### Entry Points and Output

Now, what does that look like in Webpack terms? Well, we define an entry point (that has our code and can `import` other files), an output specification, and let Webpack do its thing.

This is a good time to formally introduce two of Webpack's core concepts. First, we have Entry Points. 



### The other problem that Webpack solves

browser compatibility issues with new JS features.

### Loaders and Plugins

```
code
```

`inline code`

![Image](/blog/2019/08/07/a-webpack-4-primer/wordpress-language-select.png)

[link](https://getcomposer.org/download/)