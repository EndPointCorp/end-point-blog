---
author: "Kevin Campusano"
title: "Using esbuild and pnpm to Set Up Frontend Asset Bundling in an ASP.NET Core Web App"
github_issue_number: 2145
featured:
  image_url: /blog/2025/08/using-esbuild-to-set-up-frontend-asset-bundling-in-an-asp-net-core-web-app/mountains.webp
description: A nice approach for handling frontend asset bundling with support for JavaScript and Sass.
date: 2025-08-25
tags:
- aspdotnet
- javascript
- css
---

![Layers of mountains are exposed by light with a red tint](/blog/2025/08/using-esbuild-to-set-up-frontend-asset-bundling-in-an-asp-net-core-web-app/mountains.webp)

<!-- Photo by Seth Jensen, 2025. -->

Recently we had to build an admin dashboard on ASP.NET Core. We decided to hit the ground running by looking for a template online. Luckily, we found a very cool one from Start Bootstrap that [met our requirements](https://startbootstrap.com/template/sb-admin). It was built using [Bootstrap](https://getbootstrap.com/), had nice styling, and included examples of graphs, tables, and basic common pages like login and registration.

However, integrating the template into an ASP.NET Core web app was a bit involved. The template uses tools like [Pug](https://pugjs.org/api/getting-started.html) and [Sass/SCSS](https://sass-lang.com/documentation/syntax/), which are not supported out of the box by ASP.NET. So some work had to be done to properly integrate it.

We ended up with a nice approach for handling frontend asset bundling using [pnpm](https://pnpm.io/) and [esbuild](https://esbuild.github.io/), with support for JavaScript and Sass.

> You can find a codebase that uses the setup we'll be discussing here on [Github](https://github.com/megakevin/razor-start-bootstrap-admin). It's an empty ASP.NET Core Razor Pages project that implements Start Bootrap's admin template. Feel free to review it alongside this article and/or use it for your own projects.

> We've also [uploaded to NuGet](https://www.nuget.org/packages/EndPointDev.RazorEsbuildProjectTemplate) a template for an empty ASP.NET Core Razor Pages web app that has implemented the esbuild-based frontend asset bundling.

### Installing pnpm and the necessary packages

First of all we need to have the [.NET framework installed](https://dotnet.microsoft.com/en-us/download). We also need to [install Node.js](https://nodejs.org/en/download) and [the pnpm package manager](https://pnpm.io/installation).

```
$ dotnet --version
9.0.302
$ node --version
v22.18.0
$ pnpm --version
10.14.0
```

Once we have those, we need a Razor Pages project to apply the changes to. For our purposes, I'm going to assume we're starting off with a fresh project, created using something like `dotnet new webapp`.

With that out of the way, we can create a `package.json` file in the root of our project:

```sh
$ pnpm init
Wrote to /path/to/code/package.json

{
  "name": "demo",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "packageManager": "pnpm@10.14.0"
}
```

We can adjust the resulting `package.json` to better reflect our project. Maybe remove the `main` and `scripts.test` settings, which we don't need. Maybe also set a `name` and `description`.

In any case, now that we have this, we can install the Node.js packages that we need. I mentioned that we were going to use esbuild and SCSS so let's install those as dev dependencies:

```sh
$ pnpm add esbuild esbuild-sass-plugin sass@1.78.0 --save-dev
Packages: +41
+++++++++++++++++++++++++++++++++++++++++
Progress: resolved 103, reused 50, downloaded 0, added 41, done

devDependencies:
+ esbuild 0.25.9
+ esbuild-sass-plugin 3.3.1
+ sass 1.78.0 (1.90.0 is available)

╭ Warning ───────────────────────────────────────────────────────────────────────────────────╮
│                                                                                            │
│   Ignored build scripts: esbuild.                                                          │
│   Run "pnpm approve-builds" to pick which dependencies should be allowed to run scripts.   │
│                                                                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────╯

Done in 2.5s using pnpm v10.14.0
```

> I've pinned the version of the `sass` package to `1.78.0` in order to work around some compatibility warnings with Bootstrap's stylesheets. You may or may not need to do this in your own projects.

We have to address the warning message and allow `esbuild` to run scripts. Running `pnpm approve-builds` and selecting `esbuild` (by pressing either the "Space" or "a" keys) takes care of that:

```sh
$ pnpm approve-builds
✔ Choose which packages to build (Press <space> to select, <a> to toggle all, <i> to invert selection) · esbuild
✔ The next packages will now be built: esbuild.
Do you approve? (y/N) · true
node_modules/.pnpm/esbuild@0.25.9/node_modules/esbuild: Running postinstall script, done in 40ms
```

With that, the `package.json` file should be looking like this:

```json
// ./package.json

{
  "name": "demo",
  "version": "1.0.0",
  "description": "",
  "scripts": {},
  "keywords": [],
  "author": "",
  "license": "ISC",
  "packageManager": "pnpm@10.14.0",
  "devDependencies": {
    "esbuild": "^0.25.9",
    "esbuild-sass-plugin": "^3.3.1",
    "sass": "1.78.0"
  }
}
```

There should also be a new `pnpm-workspace.yaml` file that contains the setting for the approval we gave for `esbuild`:

```yaml
# ./pnpm-workspace.yaml

onlyBuiltDependencies:
  - esbuild
```

In this particular example, we're adapting Start Bootrap's admin template, so we're going to install the packages that it needs:

```sh
$ pnpm add @fortawesome/fontawesome-free bootstrap chart.js jquery simple-datatables
Packages: +9
+++++++++
Progress: resolved 112, reused 59, downloaded 0, added 9, done

dependencies:
+ @fortawesome/fontawesome-free 7.0.0
+ bootstrap 5.3.7
+ chart.js 4.5.0
+ jquery 3.7.1
+ simple-datatables 10.0.0

Done in 2.9s using pnpm v10.14.0
```

These are the ones we need for this project but of course, in your own projects you can install whatever you want.

### Authoring JavaScript and SCSS source files

Now that we have the Node.js part of the project set up, we need a place where we can put our JavaScript and SCSS files. For that, we created two new directories: `JavaScript` and `Stylesheets`.

Since we're adapting Start Bootrap's admin template, we copied all its SCSS files into the `Stylesheets` directory and put its JavaScript into the `JavaScript` directory. It all ended up looking like this:

```diff
 .
+├── JavaScript
+│   └── site.js
 ├── Pages
+├── Stylesheets
+│   ├── layout
+│   ├── navigation
+│   ├── plugins
+│   ├── variables
+│   ├── _global.scss
+│   ├── site.scss
+│   └── _variables.scss
 ├── wwwroot
 │   ├── css
 │   ├── js
 │   └── favicon.ico
 ├── appsettings.Development.json
 ├── appsettings.json
+├── package.json
+├── pnpm-lock.yaml
+├── pnpm-workspace.yaml
 ├── Program.cs
 ├── RazorStartBootstrapAdmin.csproj
 └── README.md
```

Of course, the specific file contents will be different in your own projects, but the take home message is that these two new directories are meant for the source files of your frontend assets.

### Bundling frontend assets with esbuild

With that, we have the NodeJS package management ready, the tools we need, and a project directory structure that supports writing JavaScript and SCSS.

Now we need to put together an `esbuild.config.mjs` file that processes these files and produces the bundles. Here it is:

```javascript
// ./esbuild.config.mjs

import * as esbuild from 'esbuild';
import { sassPlugin } from 'esbuild-sass-plugin';

// SCSS
// This is a list of all the SCSS files that we want to bundle and their
// respective output files. In this project's case, we have only one.
// We put the resulting file under ./wwwroot/css. "wwwroot" is the default
// location used to expose files to the public in ASP.NET Core Razor Pages
// projects.
const scssFiles = [
  { entry: './Stylesheets/site.scss', outfile: './wwwroot/css/site.css' },
];

// Here we tell esbuild to take the entry SCSS files as input and produce CSS
// files ready to be interpreted by a browser. Since the source files are SCSS,
// we use the esbuild-sass-plugin plugin to translate them into CSS.
scssFiles.forEach(async file => {
  await esbuild.build({
    entryPoints: [file.entry],
    bundle: true,
    sourcemap: true,
    // Some libraries, like Bootstrap, include icons as woff and woff2 font
    // files. To handle this, we specify this loader setting. Instructing
    // esbuild to use the "file" loader, when it encounters such files. The
    // "file" loader takes care of copying the files into the output
    // location.
    // More info: https://esbuild.github.io/content-types/#file
    loader: { '.woff': 'file', '.woff2': 'file' },
    outfile: file.outfile,
    plugins: [sassPlugin()]
  });
});

// JavaScript
// Similar to the stylesheet files, for JavaScript we also declare a list of the
// files that we want to bundle.
const jsFiles = [
  { entry: './JavaScript/site.js', outfile: './wwwroot/js/site.js' },
];

// Bundling here is simpler than SCSS because we don't need custom loaders or
// plugins. Just specify entry points and output files and esbuild knows what to
// do.
jsFiles.forEach(async file => {
  await esbuild.build({
    entryPoints: [file.entry],
    bundle: true,
    sourcemap: true,
    outfile: file.outfile,
  })
});
```

> One important thing to note here is that with `esbuild`, we can safely use JavaScript modules and `import` statements for both JavaScript and SCSS. This means that our frontend logic and styling rules can be broken up into any number of files, forming a tree of dependencies through `import` statements. We need only to specify the root files, or entry points, and `esbuild` takes care of building a complete and self-contained bundle. Not really a revolutionary idea in the grand scheme of things, but not always a given when working with JavaScript on the browser.

With this, we can trigger the bundling process: `node esbuild.config.mjs`. However, it'd be nice to have it better integrated with a typical .NET development flow. For that, we can add the following under `scripts` in `package.json`:

```json
// ./package.json

{
  // ...
  "scripts": {
    "build": "node esbuild.config.mjs"
  },
  // ...
}
```

This allows us to run `pnpm run build` instead.

Finally, we can have this command run automatically as part of `dotnet build` if we add the following to our `.csproj` file:


```xml
<!-- ./RazorStartBootstrapAdmin.csproj -->

<Project Sdk="Microsoft.NET.Sdk.Web">

  <!-- ... -->

  <Target Name="BundleFrontendAssets" BeforeTargets="Build">
    <Exec Command="pnpm install" />
    <Exec Command="pnpm run build" />
  </Target>

</Project>
```

All this will result in our build process producing `./wwwroot/css/site.css`, and `./wwwroot/js/site.js` bundles. Which we can include in our `.cshtml` files like we would any other `.js` or `.css` file:

```html
<!-- ./Pages/Shared/_Layout.cshtml -->

<!-- ... -->
<link rel="stylesheet" href="~/css/site.css" asp-append-version="true" />
<!-- ... -->
<script src="~/js/site.js" asp-append-version="true"></script>
<!-- ... -->
```

### Importing libraries as modules

One interesting aspect to note is that, with `esbuild`, we are using [JavaScript modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) with [`import` statements](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules#importing_features_into_your_script). This is particularly important for libraries, since some of them won't necessarily support being included as JavaScript modules by default or in an obvious manner.

Our `site.js` demonstrates this. For example, it loads Bootstrap and the Font Awesome icons using the following statements:

```javascript
// ./JavaScript/site.js

import 'bootstrap';
import '@fortawesome/fontawesome-free/js/all';

// ...
```

This makes it so any page that includes `site.js` will also have Bootstrap and the Font Awesome icons available.

To get the same for something like JQuery, for example, the strategy is a little different:

```javascript
// ./JavaScript/site.js

import jQuery from 'jquery';
window.$ = window.jQuery = jQuery;

// ...
```

A similar scenario happens with the stylesheets. For SCSS, we have to use the `@import` statement. Our `site.scss` contains examples of this. Here's how we load Bootstrap's CSS, for instance:

```scss
// ./Stylesheets/site.scss

// ...
@import "bootstrap/scss/bootstrap.scss";
// ...
```

In your projects, you'll encounter libraries with varying levels of support for JavaScript modules, and you will have to adapt accordingly, depending on the library itself and how you want to use it.

### Importing libraries via HTML tags

There are also some libraries that only work via traditional `<script>` tags. For these, you might want to have `esbuild` copy files directly from the `node_modules` directory into `wwwroot`, without any preprocessing. You could use something like this in your `esbuild.config.mjs` file for that:

```javascript
// ./esbuild.config.mjs

// Raw files
const rawFiles = [
  { entry: './node_modules/path/to/package.js', outfile: './wwwroot/lib/package.js' },
  { entry: './node_modules/path/to/package.css', outfile: './wwwroot/lib/package.css' },
];

rawFiles.forEach(async file => {
  await esbuild.build({
    entryPoints: [file.entry],
    bundle: false,
    sourcemap: false,
    loader: { ".*": 'copy' },
    outfile: file.outfile
  });
});
```

Then you can include the files from `wwwroot` using the appropriate `<script>` or `<link rel="stylesheet">` tags.

### Summary

So, in the end, using `esbuild` and `pnpm` to set up frontend asset bundling in an ASP.NET Core web app is perfectly doable and can be summarized like this:

1. Install NodeJS and `pnpm`
2. Create a `package.json` file with `pnpm init`
3. Install `esbuild` as a dev dependency with `pnpm add esbuild --save-dev`

    Also make sure to run `pnpm approve-builds` to allow `esbuild` to run scripts

4. Install any additional preprocessor that you might need like `sass` with `esbuild-sass-plugin`, etc.
5. Create `JavaScript` and `Stylesheets` directories and put your source files in them
6. Add an `esbuild.config.mjs` file that can bundle your assets
7. Include the asset bundling step as part of the `dotnet build` command

Your package.json should end up looking something like this:

```json
{
  "name": "",
  "version": "1.0.0",
  "description": "",
  "scripts": {
    // Register this so that esbuild can be called with "pnpm run build"
    "build": "node esbuild.config.mjs"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "dependencies": {
    // Add your dependencies here.
  },
  "devDependencies": {
    "esbuild": "0.25.9",
    // Add other preprocessors and plugins here, like:
    "esbuild-sass-plugin": "3.3.1",
    "sass": "1.78.0"
  }
}
```

Here's an example of an `esbuild.config.mjs` that covers the common scenarios:

```javascript
import * as esbuild from 'esbuild';
import { sassPlugin } from 'esbuild-sass-plugin';

// SCSS
const scssFiles = [
  { entry: './Stylesheets/site.scss', outfile: './wwwroot/css/site.css' },
  // Add other stylesheet files here.
];

scssFiles.forEach(async file => {
  await esbuild.build({
    entryPoints: [file.entry],
    bundle: true,
    sourcemap: true,
    loader: { '.woff': 'file', '.woff2': 'file' },
    outfile: file.outfile,
    plugins: [sassPlugin()]
  });
});


// JavaScript
const jsFiles = [
  { entry: './JavaScript/site.js', outfile: './wwwroot/js/site.js' },
  // Add other JavaScript files here.
];

jsFiles.forEach(async file => {
  await esbuild.build({
    entryPoints: [file.entry],
    bundle: true,
    sourcemap: true,
    outfile: file.outfile,
  })
});

// Raw files
const rawFiles = [
  { entry: './node_modules/path/to/package.js', outfile: './wwwroot/lib/package.js' },
  { entry: './node_modules/path/to/package.css', outfile: './wwwroot/lib/package.css' },
  // Add other library files here.
];

rawFiles.forEach(async file => {
  await esbuild.build({
    entryPoints: [file.entry],
    bundle: false,
    sourcemap: false,
    loader: { ".*": 'copy' },
    outfile: file.outfile
  });
});
```

This is the addition that the `.csproj` file needs in order to bundle the frontend assets during `dotnet build`:

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">

  <!-- ... -->

  <Target Name="BundleFrontendAssets" BeforeTargets="Build">
    <Exec Command="pnpm install" />
    <Exec Command="pnpm run build" />
  </Target>

</Project>
```

With that, you're free to add the bundles and raw files in your pages using traditional methods like:

```html
<link rel="stylesheet" href="~/css/site.css" asp-append-version="true" />
<link rel="stylesheet" href="~/lib/package.css" asp-append-version="true" />
```

and...

```html
<script src="~/js/site.js" asp-append-version="true"></script>
<script src="~/lib/package.js" asp-append-version="true"></script>
```

As you create more entrypoint JavaScript and SCSS files, you have to remember to add them to their respective arrays in `esbuild.config.mjs`.

You can add more packages using `pnpm add <package_name>`. Just remember that they have to be imported by your JavaScript files as modules. If you need to add raw files, especially from libraries that don't support being imported as JavaScript modules, the `esbuild.config.mjs` file also supports that thanks to the "raw files" section. These raw files can be loaded normally via `<link>` and `<script>` HTML tags.

All right, that's it for now. We've seen how to integrate `esbuild` with ASP.NET Core in order to setup a basic frontend asset bundling process. We did that through adapting Smart Bootstrap's free admin template into an ASP.NET Core Razor Pages web app project — a project that's up on [GitHub](https://github.com/megakevin/razor-start-bootstrap-admin). We saw how to organize source files in our repo, a basic `esbuild` config script that handles the most common scenarios, and how to handle a few different cases when it comes to including NodeJS packages into our apps.
