---
title: "Making sense of XML/JSON items in the shell"
author: Muhammad Najmi bin Ahmad Zabidi
tags: shell, json
gh_issue_number: 1578
---

![a shell](/blog/2019/12/31/making-sense-of-xml-json-in-shell/image-0.jpg)

Working as a system administrator means I have to spend quite some time during my work (and even during casual surfing) with the terminal. Sometimes I feel that certain information I want could just be fetched and parsed through the terminal, without having to use my mouse and point to the browser.

Some of the websites I visit use XML and JSON, which we could parse with Bash scripting. Previously I wrote a Ruby script to call Nokogiri to parse the XML elements until I found a Bash tool that could do the same thing.

These tools have already been around for quite a while—I’d just like to share what I did with them. The tools I used are xmlstarlet for XML parsing and jq for JSON.

###XML

I have the following XML elements, and I’ll save them to a file called data.xml:

```xml
<rss version="2.0"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
    xmlns:admin="http://webns.net/mvcb/"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:content="http://purl.org/rss/1.0/modules/content/">

    <channel>
        <title>eSolat JAKIM : Waktu Solat Hari Ini</title>
        <link>Gombak,Petaling,Sepang,Hulu Langat,Hulu Selangor,Rawang,S.Alam</link>
        <description>Gombak,Petaling,Sepang,Hulu Langat,Hulu Selangor,Rawang,S.Alam</description>
        <dc:language>ms</dc:language>
        <dc:creator>www.e-solat.gov.my</dc:creator>
        <dc:rights>Copyright JAKIM</dc:rights>
        <dc:date>26-12-2019 00:37:31</dc:date>
        <admin:generatorAgent rdf:resource="expressionengine" />

        <item>
            <title>Imsak</title>
            <description>05:53:00</description>
        </item>
        <item>
            <title>Subuh</title>
            <description>06:03:00</description>
        </item>
        <item>
            <title>Syuruk</title>
            <description>07:14:00</description>
        </item>
        <item>
            <title>Zohor</title>
            <description>13:16:00</description>
        </item>
        <item>
            <title>Asar</title>
            <description>16:39:00</description>
        </item>
        <item>
            <title>Maghrib</title>
            <description>19:13:00</description>
        </item>
        <item>
            <title>Isyak</title>
            <description>20:28:00</description>
        </item>
    </channel>
</rss>
```

I’ll use xmlstarlet, together with a bunch of the related flags to parse these elements into something which is more eye-friendly.

```bash
xmlstarlet sel -T -t -n \
  -o "------------------------------" -n \
  -o "Area: " \
  -m "//channel" -v "link" -n  \
  -o "Date: " \
  -m "//channel" -v "dc:date" -n  \
  -o "------------------------------" -n \
  -t -m "//item" -o "Time: " -v "title" \
  -o " -- " \
  -o "Time: " -v "description" -n  \
  /path/to/data.xml
```

The output looks like this:

```plain
------------------------------
Area: Gombak,Petaling,Sepang,Hulu Langat,Hulu Selangor,Rawang,S.Alam
Date: 26-12-2019 00:37:31
------------------------------
Time: Imsak -- Time: 05:53:00
Time: Subuh -- Time: 06:03:00
Time: Syuruk -- Time: 07:14:00
Time: Zohor -- Time: 13:16:00
Time: Asar -- Time: 16:39:00
Time: Maghrib -- Time: 19:13:00
Time: Isyak -- Time: 20:28:00
```

I’ll put this in a Bash script, and call it xmlstarlet-time.sh.

```bash
#!/bin/bash

XMLPATH=/home/seth/data.xml

if [[ -z $1 ]]; then
  echo "Put the location code"
  echo "$0 <location code>"
  echo -n
  exit
fi

lynx -source "https://www.e-solat.gov.my/index.php?r=esolatApi/xmlfeed&zon=$1" > $XMLPATH

xmlstarlet sel -T -t -n \
  -o "------------------------------" -n \
  -o "Area: " -m "//channel" -v "link" -n  \
  -o "Date: " -m "//channel" -v "dc:date" -n  \
  -o "------------------------------" -n \
  -t -m "//item" -o "Time: " -v "title" -o " -- " -o "Time: " -v "description" -n  \
  $XMLPATH
```

Now, after making it executable with `chmod +x xmlstarlet-time.sh`, I can just run the script whenever I need the info. In my case, I would type `./xmlstarlet-time.sh SGR01` in order to get the above information. I got the code (in my case) from the XML URL above. Your use case will likely be different.

###JSON

Let’s say I want to grab the latest currency exchange, taking the base of USD from exchangeratesapi.io. I can use curl to get the data.

```bash
$ curl -s 'https://api.exchangeratesapi.io/api/latest?base=USD'
```

Which will return:

```json
{"rates":{"CAD":1.3160649819,"HKD":7.7879061372,"ISK":122.3826714801,"PHP":50.8402527076,"DKK":6.7429602888,"HUF":299.4223826715,"CZK":23.0009025271,"GBP":0.7719584838,"RON":4.3131768953,"SEK":9.4361913357,"IDR":13985.0180505415,"INR":71.2567689531,"BRL":4.0835740072,"RUB":62.0877256318,"HRK":6.719765343,"JPY":109.3772563177,"THB":30.155234657,"CHF":0.9817689531,"EUR":0.9025270758,"MYR":4.1364620939,"BGN":1.7651624549,"TRY":5.9561371841,"CNY":7.0074909747,"NOK":8.94566787,"NZD":1.5086642599,"ZAR":14.1935018051,"USD":1.0,"MXN":18.9626353791,"SGD":1.3553249097,"AUD":1.4457581227,"ILS":3.4714801444,"KRW":1162.1931407942,"PLN":3.8445848375},"base":"USD","date":"2019-12-24"}
```

Using jq, we can format the information more readably:

```bash
$ curl -s 'https://api.exchangeratesapi.io/api/latest?base=USD' | jq
{
  "rates": {
    "CAD": 1.3160649819,
    "HKD": 7.7879061372,
    "ISK": 122.3826714801,
    "PHP": 50.8402527076,
    "DKK": 6.7429602888,
    "HUF": 299.4223826715,
    "CZK": 23.0009025271,
    "GBP": 0.7719584838,
    "RON": 4.3131768953,
    "SEK": 9.4361913357,
    "IDR": 13985.0180505415,
    "INR": 71.2567689531,
    "BRL": 4.0835740072,
    "RUB": 62.0877256318,
    "HRK": 6.719765343,
    "JPY": 109.3772563177,
    "THB": 30.155234657,
    "CHF": 0.9817689531,
    "EUR": 0.9025270758,
    "MYR": 4.1364620939,
    "BGN": 1.7651624549,
    "TRY": 5.9561371841,
    "CNY": 7.0074909747,
    "NOK": 8.94566787,
    "NZD": 1.5086642599,
    "ZAR": 14.1935018051,
    "USD": 1,
    "MXN": 18.9626353791,
    "SGD": 1.3553249097,
    "AUD": 1.4457581227,
    "ILS": 3.4714801444,
    "KRW": 1162.1931407942,
    "PLN": 3.8445848375
  },
  "base": "USD",
  "date": "2019-12-24"
}
```

Next, I can make use of the tool in my shell script.

```bash
#!/bin/bash -l

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

if [ -z `which jq` ]; then
  printf "You need to install jq, a JSON parsing tool \n"
  exit
fi

sourcemoney=$(echo $2 | tr '[:lower:]' '[:upper:]')
target=$(echo $3 | tr '[:lower:]' '[:upper:]')

sumber=$(curl -s "https://api.exchangeratesapi.io/api/latest?base=$sourcemoney" | jq . | grep -i $target | awk -F ':|,' '{ print $2 }')

jumlah=$(printf "%f*%f\n" $1 $sumber | bc)

printf "Price per unit: ${GREEN}1 $sourcemoney${NC} = ${YELLOW}$target %.2f${NC}\n" $sumber

echo -e "Source money: ${YELLOW}$sourcemoney $1${NC}"
echo -n

printf "Total money after the conversion: ${YELLOW}$target %.2f ${NC}\n" $jumlah
```

Then I can save the script into a file called moneychanger-with-api.sh and make it executable with `chmod +x moneychanger-with-api.sh`.

And now the script will do the parsing for me, without the need for a browser.

```
$ ./moneychanger-with-api.sh 100 usd eur
Price per unit: 1 USD =  EUR 0.90
Source money: USD 100
Total money after the conversion: EUR 90.25

$ ./moneychanger-with-api.sh 100 eur sgd
Price per unit: 1 EUR =  SGD 1.50
Source money: EUR 100
Total money after the conversion: SGD 150.17
```
