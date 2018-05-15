gh_issue_number: 1163
tags: html, javascript
title: Int’l — JavaScript numbers and dates formatting, smart strings comparison
---

<img border="0" src="/blog/2015/10/16/intl-javascript-numbers-and-dates/image-0.png" style="width: 100%;"/>

### Introduction

*** WARNING *** At the time of writing this text all of the things mentioned below are not yet supported by Safari and most of the mobile browsers.

It’s almost three years now since Ecma International published the 1st version of “ECMAScript Internationalization API Specification”. It’s widely supported by most of the browsers now. A new object called Intl has been introduced. Let’s see what it can do.

To make it easier imagine that we have a banking system with a possibility of having accounts in multiple currencies. Our user is Mr. White, a rich guy.

### Intl powers

#### Number formatting

Mr. White has four accounts with four different currencies: British pound, Japanese yen, Swiss franc, Moroccan dirham. If we want to have a list of current balances, with a correct currency symbols, it’s pretty simple:

```javascript
// locales and balances object
var accounts = [
    {
        locale: 'en-GB',
        balance: 165464345,
        currency: 'GBP'
    },
    {
        locale: 'ja-JP',
        balance: 664345,
        currency: 'JPY'
    },
    {
        locale: 'fr-CH',
        balance: 904345,
        currency: 'CHE'
    },
    {
        locale: 'ar-MA',
        balance: 4345,
        currency: 'MAD'
    }
];

// now print how rich is Mr. White!
accounts.forEach(function accountsPrint (account) {
    console.log(new Intl.NumberFormat(account.locale, {style: 'currency', currency: account.currency}).format(account.balance));
});
```

The output looks like:

```
"£165,464,345"
"￥664,345"
"CHE 904 345"
"د.م.‏ ٤٬٣٤٥"
```

In a real application you’d typically use the same locale for a view/language/page, the different examples above are just to show the power of Intl!

#### Date and time easier

Mr. White changed his UI language to Norwegian. How to show dates and weekdays without a big effort?

```javascript
// we need a list of the current week dates and weekdays
var startingDay = new Date();

var thisDay = new Date();
var options = {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'};
for(var i=0; i < 7; i++) {
    thisDay.setDate(startingDay.getDate() + i);

    console.log(new Intl.DateTimeFormat('nb-NO', options).format(thisDay));
}
```

The output is:

```
"onsdag 23. september 2015"
"torsdag 24. september 2015"
"fredag 25. september 2015"
"lørdag 26. september 2015"
"søndag 27. september 2015"
"mandag 28. september 2015"
"tirsdag 29. september 2015"
```

Trust me, it’s correct (;p).

#### String comparison

Mr. White has a list of his clients from Sweden. He uses his UI in German as it’s a default language, but Mr. White is Swedish.

```javascript
var clients = ["Damien", "Ärna", "Darren", "Adam"];
clients.sort(new Intl.Collator('de').compare);
console.log(clients);
```

Here Mr. White will expect to find Mr. Ärna at the end of the list. But in German alphabet Ä is in a different place than in Swedish, that why the output is:

```
["Adam", "Ärna", "Damien", "Darren"]
```

To make Mr. White happy we need to modify our code a bit:

```javascript
var clients = ["Damien", "Ärna", "Darren", "Adam"];
clients.sort(new Intl.Collator('sv').compare);
console.log(clients);
```

Now, we are sorting using Collator object with Swedish locales. The output is different now:

```
["Adam", "Damien", "Darren", "Ärna"]
```

### Conclusion

Be careful with using the Intl object—​its implementation is still not perfect and not supported by all the browsers. There is a nice library called: [Intl.js](https://github.com/andyearnshaw/Intl.js/) by Andy Earnshaw. It’s nothing more than a compatibility implementation of the ECMAScript Internationalization API. You can use it to use all the Intl object features now, without being worried about different browsers’ implementations.
