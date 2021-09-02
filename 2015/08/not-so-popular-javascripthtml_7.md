---
author: Piotr Hankiewicz
title: Not so popular JavaScript/HTML functionalities
github_issue_number: 1148
tags:
- html
- javascript
date: 2015-08-07
---

There are multiple things in a front-end developer work that can be easily fixed by a native browser functions. Based on experience, JavaScript learning path for a big part of front-end developers is not perfect. Therefore, I will give you some examples, for some people as a reminder, for others as a new thing to think about. It is always good to learn, right?

### document.execCommand

[W3C definition](https://w3c.github.io/editing/execCommand.html)

It lets you use built-in browser functions as you wish from JavaScript, simple functions to do simple things. execCommand is very useful when you work with text ranges selected by a user. It’s also popular that it comes together with a contentEditable HTML element attribute.

#### Practical examples

- You want to have redo button in your application, so when user will click on it, the latest changes will be discarded.

```javascript
// after running just this, the latest user changes will be discarded (text input changes)
execCommand('redo', false, null);
```

- You want to remove text after the cursor position.

```javascript
// after running this script one character after the cursor
// position in a current element will be removed
execCommand('forwardDelete', false, null);
```

There are more than 30 functions ([look here](https://developer.mozilla.org/en-US/docs/Web/API/Document/execCommand)) that can be used with a limited amount of code. You need to be careful though, keep on testing, multiple browsers have different implementations, but will be unified in the future.

### document.designMode

[W3C definition](https://www.w3.org/TR/html5/editing.html#making-entire-documents-editable-the-designmode-idl-attribute)

I want you to make a small experiment. On the current page please open developer console (Firebug or DevTools) and try to run this code:

```javascript
document.designMode = 'on';
```

Have you noticed anything? What has happened now is that the whole page is editable now, you can edit any paragraph of this page, any header, any link. It’s not so practical anymore as you can’t run this command on any element, only on the Document object, but it’s cool to know that stuff like this exists. Every HTML element has a contentEditable attribute set now with a value set to true.

### element.contentEditable

[W3C definition](https://www.w3.org/TR/html5/editing.html#making-document-regions-editable-the-contenteditable-content-attribute)

“contentEditable” attribute can be set to any HTML document element. What it does is it makes element editable or not. By default, every HTML element is not editable, you can easily change it by setting contentEditable attribute value to true like this:

```javascript
document.getElementById('word-open').contentEditable = 'true';
```

If you will again run this script on the current page you will be able to edit big slogan on the left side of this text, well, only the “OPEN” word. This can be extremely useful when you need to build an online rich text editor.

### navigator

[W3C definition](http://www.w3.org/TR/2013/CR-html5-20130806/webappapis.html#navigator)

Navigator object is not standardized yet by W3C but it’s supported by around 90% of the global browsers (known and popular browsers not supporting it are IE8 and Opera Mini). It contains multiple client browser information. For example:

```javascript
// will return a list of supported/installed browser plugins, you can
// check if the user has the Flash software installed, or to check if user uses Ad-block plugin
console.log(navigator.plugins);

// will return a geolocation object, you can track client geo position
console.log(navigator.geolocation);

// will return a browser engine name, useful when you need to check it instead
// of a browser name
console.log(navigator.engine);
```

### Conclusion

I recommend everyone interested in the front-end development to go through W3C standardization documents, read it chapter by chapter. There are resources not widely popular but very helpful.
