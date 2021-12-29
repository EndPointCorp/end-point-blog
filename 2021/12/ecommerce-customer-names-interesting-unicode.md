---
title: "Ecommerce customer names with interesting Unicode characters"
author: Jon Jensen
github_issue_number: 1811
tags:
- ecommerce
- unicode
- sql
- postgresql
date: 2021-12-29
---

![Photo of a small garden in front of a house basement window with two cats looking out](/blog/2021/12/ecommerce-customer-names-interesting-unicode/20210710_085128-sm.jpg)

<!-- photo by Jon Jensen -->

One of our clients with a busy ecommerce site sees a lot of orders, and among those, sometimes there are unusual customer name and address submissions.

We first noticed in 2015 that they had a customer order come in with an emoji in the name field of the order. The emoji was 😏 and we half-jokingly wondered if that was a new sign of fraud.

Over the following 3 years only a few more orders came in with various emoji in customer's names, but in mid-2018 emoji started to appear increasingly frequently until now one now appears on average every day or two.

Why the sudden appearance of emoji in 2015? It correlates with the rapid shift to browsing the web and shopping on mobile devices. Mobile visits now represent more than half of this client's ecommerce traffic.

Most people in 2015 didn't even know how to type emoji on a desktop or laptop computer, but mobile touchscreen keyboards began showing emoji choices around that time, so the mobile explanation makes sense. And mobile keyboard autocorrect also sometimes offers emoji in addition to words, making them even more common in the past few years.

Just for fun I wanted to automatically find all such "interesting" names, so I wrote a simple report that uses SQL to query their PostgreSQL ecommerce database.

To preserve customer privacy, names shown here have been changed and limited to a few names that are common in the United States.

### Real names with bonuses

First let's look at the apparently real names with emoji and other non-alphabetical Unicode characters mixed in:

Amy 🩺<br>
Amy💕<br>
Amy👑<br>
👸Amy<br>
Anna 💫<br>
Anna 😎<br>
Anna ❤️<br>
Anna💊💉<br>
Bob☯️<br>
Bob😍😘😜👑💞<br>
Bob🐞<br>
Brenda 🌙<br>
Brenda 🥳🤪<br>
Brenda☠️<br>
B R E N D A 💕💅🏾💃🏾👜<br>
Cameron 🌻<br>
Cameron 😎<br>
Cameron 💁🏻‍♀️<br>
Doug 💕<br>
Doug 🅱️<br>
Doug 🌸🤩<br>
Doug 👦🏻❤️<br>
Emily 🌷<br>
Emily 😊🇨🇺<br>
Emily😚<br>
Emily 🎰👑❤️<br>
Frank 🥰<br>
Frank ⚗️<br>
Frank🔆<br>
Frank💞💰<br>
Jane 💕<br>
Jane⁸<br>
Jane ❤️❤️<br>
Jane🔆<br>
Jill 👑🎀<br>
Jill 👼🏽✨🌫<br>
Jill🍓🍒🍒<br>
Jill👸🏽💖<br>
Jim 🐰<br>
Jim, 💕<br>
Jim’s iPhone✨<br>
Joe 🐯<br>
Joe 🇦🇺<br>
Joe😏<br>
Joe🏀🎸‼️<br>
John 👪<br>
John⁵<br>
John🎭<br>
Karen 🌻🌹<br>
Karen 👑✨<br>
Karen 🔒❤️<br>
Karen🎀👑<br>
Kate💙💚<br>
Kate🤪🤞🏽💙<br>
Kate.💘<br>
K$ate💉<br>
Liz🌺<br>
Liz❣️<br>
Liz❤️🙃<br>
Liz Mama💙💙<br>
Mary 🎀<br>
Mary💘<br>
Mary👼🏼💓<br>
Mary⁹<br>
Mike 👑<br>
Mike 👑🌸<br>
Mike 👩🏻‍🌾<br>
Mike⁶<br>
Sarah 👑<br>
Sarah👑A.<br>
✨Sarah✨<br>
💛🌻 Sarah<br>
Steve🐑<br>
Steve 🦁<br>
Steve♓️💓<br>
Victoria 🥴<br>
Victoria🌻<br>
V𝚒𝚌𝚝𝚘𝚛𝚒𝚊<br>
V I C T O R I A 🤍<br>

Would you have expected all that in ecommerce orders? I didn't!

### Fake names

Next let's look at placeholder names with people's role or self-description or similar:

Amor ⚽️<br>
Babe ❤️<br>
C𝚒𝚝𝚒𝚣𝚎𝚗<br>
Daddy🥴😏<br>
Daddy😘👴👨🙏👨👩👧🙇🏾<br>
Fly High 🕊<br>
Forever 💍💜<br>
Granny 👵🏽<br>
HOME ❤️<br>
Home🏠<br>
Home🏠💜<br>
Hubby🥰<br>
💦Juicy🍑<br>
me!! 💛<br>
mi amor ❤️<br>
Mom💗<br>
Mom♥️<br>
Mom 🐥💛<br>
MOMMY 💗<br>
Myself 😘<br>
Princess👑<br>
princess❤️<br>
Queen 😍💖🔓<br>
Queen💘<br>
The Husband💍❤️<br>
Wifey 😈✌🏽👅<br>

Perhaps the occurrence of "home" several times reflects a mobile address book auto-fill function for billing or shipping address fields?

### Not names at all!

Then there are those customers who didn't provide any kind of name at all, just emoji and other special characters:

🦋<br>
💙<br>
🤡🎪<br>
💗☁️<br>
🍌<br>
♥️<br>
🌙<br>
⁵<br>
∅<br>

I guess only one or two of those per year doesn't amount to much, but they're interesting to see.

### Strange addresses

In addition to the name fields we also checked the address fields for unusual characters and found (again, details changed to preserve privacy):

125 E 27😎<br>
227 W 24 Circle ⭕️<br>
3 Blvd. George Washington™<br>

### Simply odd

The prizewinner for oddity, which seems like some kind of copy-and-paste mistake, is this in the city field of an address:

Indian® Roadmaster™ Classic

Maybe at least one motorcycle has achieved sentience and needed to do some online shopping!

### "Interesting" Unicode ranges

When searching for interesting Unicode ranges, we could just look for characters in the [Unicode emoji ranges](https://unicode.org/emoji/charts/full-emoji-list.html). That would be fairly straightforward since there are just a few ranges to match.

But we were curious what other unusual characters were getting used aside from emoji, so we wanted to include other classes of characters. So perhaps we should include everything to start and then exclude the entire class of Unicode "word characters"? That covers the world's standard characters used for names and addresses, including not just Roman/Latin with optional diacritics, but also other character sets such as Cyrillic, Arabic, Hebrew, Korean, Chinese, Japanese, Devanagari, Thai, and many others.

[PostgreSQL POSIX regular expressions](https://www.postgresql.org/docs/current/functions-matching.html#POSIX-CLASS-SHORTHAND-ESCAPES-TABLE) include the class "word character" represented by either `[[:word:]]` or the Perl shorthand `\w`. I started with that, but found it covered too many things I did want to see, such as the visually double-width Latin characters that are part of the Chinese word character range, and some special numbers.

So I switched back to matching what I want, rather than excluding what I don't want, and I manually went through the [Unicode code charts](https://www.unicode.org/charts/) and noted the ranges to include.

The list of Unicode code ranges I came up with, in hexadecimal, is:

```plain
250-2ba
2bc-2c5
2cc-2dc
2de-2ff
58d-58e
fd5-fd8
1d00-1dbf
2070-2079
207b-209f
20d0-2104
2106-2115
2117-215f
2163-218b
2190-2211
2213-266e
2670-2bff
2e00-2e7f
2ff0-2fff
3004
3012-3013
3020
3200-33ff
4dc0-4dff
a000-abf9
fff0-fffc
fffe-1d35f
1d360-1d37f
1d400-1d7ff
1ec70-1ecbf
1ed00-1ed4f
1ee00-1eeff
1f000-10ffff
```

Those ranges exclude several fairly common characters that people (or their software's autocorrect) used in their address fields, which we wanted to ignore, such as:

- Music sharp sign: ♯ (instead of # before a number)
- numero: №
- care of: ℅
- replacement character: � (though this could be interesting if it reveals unknown encoding errors)

### The SQL query

PostgreSQL allows us to represent Unicode characters in hexadecimal numbers as either `\u` plus 4 digits or `\U` plus 8 digits. So the character 2ba is written in a Postgres string as `\u02ba` and the range fffe-1d35f is written in a Postgres regex range as `[\ufffe-\U0001d35f]`.

With a little scripting to put it all together, I came up with:

```sql
SELECT order_number, order_timestamp::date AS order_date,
    fname, lname, company, address1, address2, city, state, b_fname, b_lname, b_company, b_address1, b_address2, b_city, b_state, phone
FROM orders
WHERE concat(fname, lname, company, address1, address2, city, state, b_fname, b_lname, b_company, b_address1, b_address2, b_city, b_state, phone)
    ~ '[\u0250-\u02ba\u02bc-\u02c5\u02cc-\u02dc\u02de-\u02ff\u058d-\u058e\u0fd5-\u0fd8\u1d00-\u1dbf\u2070-\u2079\u207b-\u209f\u20d0-\u2104\u2106-\u2115\u2117-\u215f\u2163-\u218b\u2190-\u2211\u2213-\u266e\u2670-\u2bff\u2e00-\u2e7f\u2ff0-\u2fff\u3004\u3012-\u3013\u3020\u3200-\u33ff\u4dc0-\u4dff\ua000-\uabf9\ufff0-\ufffc\ufffe-\U0001d35f\U0001d360-\U0001d37f\U0001d400-\U0001d7ff\U0001ec70-\U0001ecbf\U0001ed00-\U0001ed4f\U0001ee00-\U0001eeff\U0001f000-\U0010ffff]'
    -- limit how many years back to go
    AND order_timestamp > (SELECT CURRENT_TIMESTAMP - interval '3 years')
    -- exclude any order that had PII expunged for GDPR
    AND expunged_at IS NULL
ORDER BY order_timestamp DESC
```

Try a similar query on databases you have access to, and see what interesting user submissions you discover. I always find surprises and in addition to being fun, sometimes we find things that help us improve our input validation and user guidance so that more mistakes are caught when they're easy for the customer to correct.

Happy holidays!
