---
author: "Muhammad Najmi bin Ahmad Zabidi"
date: 2021-12-24
title: "Creating Translation and Currency Converter Bot with Telegram and Google App Script"
github_issue_number: 1804
tags:
- google app script
- telegram
- spreadsheet
---

In the previous [writing](/blog/2021/11/forwarding-google-forms-responses-to-api/) written by Afif, he elaborated on how to use Google App Script with Google Form. Coincidentally last year I learned a bit on how to use Google App Script with Telegram Bot as a Personal Ledger Tool written by [Mars Escobin](https://medium.com/@mars_escobin/telegram-inline-keyboards-using-google-app-script-f0a0550fde26).The base code that she wrote can be referred [here](https://github.com/mariannetrizha/budgetter/blob/master/budgetter_bot.js)

The following how the Telegram Bot that I learned from Mars looks like

(/blog/2021/12/creating-translation-and-currency-converter-bot-with-telegram-and-google-app-script/najmi-budget.jpg)

In this writing I will share a bit on how to adapt Mars’ code and use Telegram Bot to get the input from the user and let Google App Script to call Google’s cloud based services (translation and finance) and later return the outputs to the user. 

(/blog/2021/12/creating-translation-and-currency-converter-bot-with-telegram-and-google-app-script/botfather.jpg)

The initial process of having a Telegram bot can be referred [here](https://core.telegram.org/bots). After we had received the Telegram's API key then we could use it inside our Google App Script editor. 

### First: Translation Bot

(/blog/2021/12/creating-translation-and-currency-converter-bot-with-telegram-and-google-app-script/najmi-translation.jpg)

(/blog/2021/12/creating-translation-and-currency-converter-bot-with-telegram-and-google-app-script/najmi_translation_spreadsheet.jpg)


I thought one way that I could use the Telegram Bot and uses whatever the cloud service that Google provides, so I think how about the Google translation. Although (undoubtly) there are possibly tons of mobile app out there, how about I try to learn doing it with Telegram. So I found there is a class that I could use in Google App to realize that.

Google Apps script can be used to manipulate the Google Translation capability by calling the Language.App class which is documented [here](https://developers.google.com/apps-script/reference/language/language-app)

The translation capability could be invoked with the following syntax `LanguageApp.translate(word,source language, target language)`.

In my case, apart from fetching the input from the users, I also want it to store the searched word inside my Google Spreadsheet.

So by using `sheet.appendRow([formattedDate,item[0],item[1],item[2],mytranslation_out]);` we could append the searched word inside the Google Spreadshee and later we can append the input and output which we got from the user

In my case, I removed the keyBoard function from Mars’ code since I don’t have a plan to use it in my bot. Instead, I am going to use the inputs which were sent through the `“item”` variable and let `LanguageApp` to translate it. The translation will virtually take a few seconds delay, so if we do not put an interval within our code, `sendMessage`  will reply with an empty output for the translation. 

In order to handle this, I used the `Utilities.sleep()` function prior to `return sendMessage ()` so that I will be able to grab the answer before returning the output to the requestor. 

The following are my changes for creating the Translation Bot

```.javascript
var token="<insert your Telegram API here";
var telegramUrl = "https://api.telegram.org/bot" + token;
var webAppUrl = "<insert your webAppURL which is generated from Google App Script UI over here>";
 
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
var ssId = "<insert your webAppURL which is generated from Google App Script UI over here>";
var sheet = SpreadsheetApp.openById(ssId).getSheetByName("terjemah");
 
   if (contents.message){
     var id = contents.message.from.id;
     var text = contents.message.text;
    
       if (text.indexOf(",") !== -1){
    
        var dateNow = new Date;
        var formattedDate = dateNow.getDate()+"/"+(dateNow.getMonth()+1);
        var item = text.split(",");
        var mytranslation_out = LanguageApp.translate(item[0], item[1], item[2]);
      
        sheet.appendRow([formattedDate,item[0],item[1],item[2],mytranslation_out]);
 
        Utilities.sleep(200);
        return sendMessage(id, "The translation of " + item[0] + " is "+ mytranslation_out)
     }
  
   else {
 
     return sendMessage(id, "The word that you key in will be kept for our analysis purpose\nPlease use this format : word, source language code, target language code \nRefer cloud.google.com/translate/docs/languages ")
 
   }
 
   }
 
}
``` 



### Second: Currency Converter Bot

(/blog/2021/12/creating-translation-and-currency-converter-bot-with-telegram-and-google-app-script/najmi-currency.jpg)

(/blog/2021/12/creating-translation-and-currency-converter-bot-with-telegram-and-google-app-script/najmi_currency_spreadsheet.jpg)

There are (at least, maybe) two possible ways to create a currency converter bot with Telegram+Google App Script. I could either invoke a curl-alike method by calling an external API (which is not related with Google) or just manipulating whatever Google Finance offers. I did some search but I could not find any built-in class in order to do the conversion within the code. However I remember that Google Spreadsheet could actually call Google Finance within its cell. So I decided  to let Spreadsheet do the conversion and then I will fetch the result and return it to the requestor.

This is shown in the following snippet:
```.javascript
       sheet.getRange('a2').setValue(item[0]);
       sheet.getRange('b2').setValue(item[1]);
       sheet.getRange('c2').setValue(item[2]);
       sheet.getRange('d2').setValue('=GOOGLEFINANCE("currency:"&b2&c2)*a2');
```

and later we fetched the value from `“d2”` cell with

```.javascript
var value = SpreadsheetApp.getActiveSheet().getRange('d2').getValue();
```

As the default value is taking many decimal points, I made it fixed to two decimal points

```.javascript
value=value.toFixed(2);
```

and I returned the value which later converted the currency code to uppercase with .toUpperCase()

```.javascript
return sendMessage(id,item[1].toUpperCase() + " " + item[0] + " = "+ item[2].toUpperCase() + " " + value)
```

You can refer my changes in the following scripts:
```.javascript
var token="<insert your Telegram API here";
var telegramUrl = "https://api.telegram.org/bot" + token;
var webAppUrl = "<insert your webAppURL which is generated from Google App Script UI over here>";

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
var ssId = "<insert the spreadhsheet ID over here, you can get it from the URL on the browser URL bar>"; 
var sheet = SpreadsheetApp.openById(ssId).getSheetByName("mymoney"); // put the name of the spreadsheet page that you want to refer over here
   
    if (contents.message){
      var id = contents.message.from.id;
      var text = contents.message.text;
      
        if (text.indexOf(",") !== -1){
      
        var dateNow = new Date;
        var formattedDate = dateNow.getDate()+"/"+(dateNow.getMonth()+1);
        var item = text.split(",");
         
        sheet.getRange('a2').setValue(item[0]);
        sheet.getRange('b2').setValue(item[1]);
        sheet.getRange('c2').setValue(item[2]);
        sheet.getRange('d2').setValue('=GOOGLEFINANCE("currency:"&b2&c2)*a2');

SpreadsheetApp.getActiveSheet().getRange('c2').setValue('=GOOGLEFINANCE("currency:"&item[1]&item[2])*item[0]');

         var value = SpreadsheetApp.getActiveSheet().getRange('d2').getValue();
         Utilities.sleep(10);
         
         sheet.appendRow([formattedDate,item[0],item[1],item[2],value]);  
                         
         value=value.toFixed(2);
          
         return sendMessage(id,item[1].toUpperCase() + " " + item[0] + " = "+ item[2].toUpperCase() + " " + value)
      }
    
    else {

      return sendMessage(id, "The word that you key in will be kept for our analysis purpose\nPlease use this format : amount, source currency code, target currency code")
   
    }

    }
   
 }
```

## Special Notes
Throughout the process that I learned to use the Google App Script, I found several ways for us to refer to spreadsheet that we want deal inside the code. For example we can use:

```.javascript
var ssId = "<spreadsheet's ID>"; 
var sheet = SpreadsheetApp.openById(ssId).getSheetByName("<the sheet's name>");
```
given that there are (possibly) many sheets inside the spreadsheet file.

Or we could use `SpreadsheetApp.getActiveSpreadsheet()` but it depends on the active sheet inside the spreadsheet's UI, as described [here](https://developers.google.com/apps-script/reference/spreadsheet/spreadsheet-app#getactivesheet)

Nevertheless both of the mentioned method above are inside the `SpreadsheetApp` Class.

# Conclusion

I would say the are many more stuffs that could be done by the Google App Script and it will be really helpful to automate stuffs that we routinely do across many files. In my example that I gave above, it just being used on two different spreadsheets - just as a placeholder so that I could get the result to be returned to my Telegram bot. 




