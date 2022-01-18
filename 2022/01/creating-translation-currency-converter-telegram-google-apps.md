---
author: "Muhammad Najmi bin Ahmad Zabidi"
date: 2022-01-17
title: "Creating Telegram bots with Google Apps Script"
github_issue_number: 1823
tags:
- google-apps-script
- chat
- integration
---

![Empty clothes in the shape of a human sitting on a bench with fall leaves](/blog/2022/01/creating-translation-currency-converter-telegram-google-apps/20201110-165127-sm.jpg)

<!-- Photo by Jon Jensen -->

In a previous post on this blog, Afif wrote about [how to use Google Apps Script with Google Forms](/blog/2021/11/forwarding-google-forms-responses-to-api/). Coincidentally, last year I learned a bit about how to use Google Apps Script with Telegram Bot as a personal ledger tool, as outlined in [this post by Mars Escobin](https://medium.com/@mars_escobin/telegram-inline-keyboards-using-google-app-script-f0a0550fde26).

The Telegram Bot I created from Mars’s code looks like this:

![](/blog/2022/01/creating-translation-currency-converter-telegram-google-apps/najmi-budget.jpg)

In this post I will share a bit on how to adapt Mars’s code and use Telegram Bot to get the input from the user and let Google Apps Script call Google’s cloud-based services (translation and finance) to later return the outputs to the user.

![](/blog/2022/01/creating-translation-currency-converter-telegram-google-apps/botfather.png)

The initial process of creating a Telegram bot is outlined [on Telegram’s website](https://core.telegram.org/bots). After receiving Telegram’s API key we can use it inside our Google Apps Script editor.

### Translation Bot

![](/blog/2022/01/creating-translation-currency-converter-telegram-google-apps/najmi-translation.jpg)

![](/blog/2022/01/creating-translation-currency-converter-telegram-google-apps/najmi_translation_spreadsheet.png)

One way to use the Telegram Bot and Google Cloud Services which came to mind was to create a translation bot. Although there are undoubtedly tons of mobile apps out there which do the same thing, I wanted to learn about it by using Telegram. So I found a class that I could use in Apps Script to realize that.

Google Apps Script can be used to manipulate the Google Translate capability by calling the [`Language.App` class](https://developers.google.com/apps-script/reference/language/language-app). The translation capability is invoked with `LanguageApp.translate(text, sourceLanguage, targetLanguage)`.

In addition to fetching the input from the users, I also wanted to store the searched word inside a Google Sheets spreadsheet.

So by using this:

```js
sheet.appendRow([formattedDate, item[0], item[1], item[2], myTranslationOutput]);
```

we can append the searched word inside the Google spreadsheet, and later append the input and output which we got from the user.

In my case, I removed the inline `keyBoard` function from Mars’s code since I didn’t plan to use it in my bot. Instead, I will use the inputs which were sent through the `item` variable and let `LanguageApp` translate it. The translation will virtually take a few seconds, so if we do not put an interval within our code, `sendMessage`  will reply with an empty output for the translation.

In order to handle this, I used the `Utilities.sleep()` function prior to `return sendMessage()` so that I will be able to grab the answer before returning the output to the requestor.

The following are my changes for creating the translation bot:

```javascript
var token = "<insert your Telegram API token here>";
var telegramUrl = "https://api.telegram.org/bot" + token;
var webAppUrl = "<insert your webAppURL which is generated from Google Apps Script UI here>";

function sendMessage(id, text) {
  var data = {
    method: "post",
    payload: {
      method: "sendMessage",
      chat_id: String(id),
      text: text,
      parse_mode: "HTML",

    }
  };
  UrlFetchApp.fetch('https://api.telegram.org/bot' + token + '/', data);
}

function doPost(e) {
  var contents = JSON.parse(e.postData.contents);
  var ssId = "<insert your webAppURL which is generated from Google Apps Script UI here>";
  var sheet = SpreadsheetApp.openById(ssId).getSheetByName("<sheet name here>");

  if (contents.message) {
    var id = contents.message.from.id;
    var text = contents.message.text;

    if (text.indexOf(",") !== -1) {
      var dateNow = new Date;
      var formattedDate = dateNow.getDate() + "/" + (dateNow.getMonth() + 1);
      var item = text.split(",");
      var myTranslationOutput = LanguageApp.translate(item[0], item[1], item[2]);

      sheet.appendRow([formattedDate, item[0], item[1], item[2], myTranslationOutput]);

      Utilities.sleep(200);
      return sendMessage(id, "The translation of " + item[0] + " is " + myTranslationOutput);
    } else {
      return sendMessage(id, "The word that you key in will be kept for our analysis purpose\nPlease use this format : word, source language code, target language code \nRefer cloud.google.com/translate/docs/languages");
    }
  }
}
```

### Currency Converter Bot

![](/blog/2022/01/creating-translation-currency-converter-telegram-google-apps/najmi-currency.jpg)

![](/blog/2022/01/creating-translation-currency-converter-telegram-google-apps/najmi_currency_spreadsheet.png)

There are at least two possible ways to create a currency converter bot with Telegram and Google Apps Script. I could either invoke a curl-like method by calling an external API (which is not related to Google) or just manipulating whatever Google Finance offers. I did some searching but I could not find any built-in class in order to do the conversion within the code. However, I remember that Google Sheets could actually call Google Finance within its cell. So I decided to let Sheets do the conversion and then I will fetch the result and return it to the requester.

This is shown in the following snippet:

```javascript
sheet.getRange('a2').setValue(item[0]);
sheet.getRange('b2').setValue(item[1]);
sheet.getRange('c2').setValue(item[2]);
sheet.getRange('d2').setValue('=GOOGLEFINANCE("currency:"&b2&c2)*a2');
```

And later we fetched the value from `d2` cell with

```javascript
var value = SpreadsheetApp.getActiveSheet().getRange('d2').getValue();
```

As the default value is taking many decimal points, I made it fixed to two decimal points.

```javascript
value = value.toFixed(2);
```

I then returned the value which later converted the currency code to uppercase with `.toUpperCase()`.

```javascript
return sendMessage(id, item[1].toUpperCase() + " " + item[0] + " = " + item[2].toUpperCase() + " " + value);
```

You can see my changes in the following scripts:

```javascript
var token = "<insert your Telegram API token here>";
var telegramUrl = "https://api.telegram.org/bot" + token;
var webAppUrl = "<insert your webAppURL which is generated from Google Apps Script UI here>";

function setWebhook() {
  var url = telegramUrl + "/setWebhook?url=" + webAppUrl;
  var response = UrlFetchApp.fetch(url);
  Logger.log(response.getContentText());
}


function sendMessage(id, text) {
  var data = {
    method: "post",
    payload: {
      method: "sendMessage",
      chat_id: String(id),
      text: text,
      parse_mode: "HTML",

    }
  };
  UrlFetchApp.fetch('https://api.telegram.org/bot' + token + '/', data);
}

function doPost(e) {
  var contents = JSON.parse(e.postData.contents);
  var ssId = "<insert the spreadsheet ID here, you can get it from the browser URL bar>";
  var sheet = SpreadsheetApp.openById(ssId).getSheetByName("<sheet name here>");

  if (contents.message) {
    var id = contents.message.from.id;
    var text = contents.message.text;

    if (text.indexOf(",") !== -1) {
      var dateNow = new Date;
      var formattedDate = dateNow.getDate() + "/" + (dateNow.getMonth() + 1);
      var item = text.split(",");

      sheet.getRange('a2').setValue(item[0]);
      sheet.getRange('b2').setValue(item[1]);
      sheet.getRange('c2').setValue(item[2]);
      sheet.getRange('d2').setValue('=GOOGLEFINANCE("currency:"&b2&c2)*a2');

      SpreadsheetApp.getActiveSheet().getRange('c2').setValue('=GOOGLEFINANCE("currency:"&item[1]&item[2])*item[0]');

      var value = SpreadsheetApp.getActiveSheet().getRange('d2').getValue();
      Utilities.sleep(10);

      sheet.appendRow([formattedDate, item[0], item[1], item[2], value]);

      value = value.toFixed(2);

      return sendMessage(id, item[1].toUpperCase() + " " + item[0] + " = " + item[2].toUpperCase() + " " + value)
    } else {
      return sendMessage(id, "The word that you key in will be kept for our analysis purpose\nPlease use this format : amount, source currency code, target currency code")
    }
  }
}
```

### Special Notes

Throughout the process, I found several ways for us to refer to a spreadsheet that we want inside the code. For example, we can use:

```javascript
var ssId = "<spreadsheet's ID>";
var sheet = SpreadsheetApp.openById(ssId).getSheetByName("<the sheet's name>");
```

This can select a specific sheet, if your spreadsheet file contains multiple different sheets (tabs).

Or we could use `SpreadsheetApp.getActiveSpreadsheet()` but this method depends on the active sheet inside the spreadsheet's UI, as described [here](https://developers.google.com/apps-script/reference/spreadsheet/spreadsheet-app#getactivesheet).

Nevertheless, both of the methods above are part of the `SpreadsheetApp` Class.

There are many more things that could be done by the Google Apps Script. It is really helpful for automating anything that we routinely do across many files. In my example that I gave above, the function is only being used on two different spreadsheets — as a placeholder so that I could get the result to be returned to my Telegram bot.
