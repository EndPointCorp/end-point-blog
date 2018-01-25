---
author: "Lee Azzarello"
title: "Free Encryption for All, In Our Time"
tags: security
gh_issue_number: 1364
---

<div class="separator" style="clear: both; text-align: center;"><img border="0" src="/blog/2016/06/27/free-encryption-for-all/LAblog.jpg"/></div>

The [commodification of encryption algorithms](https://en.wikipedia.org/wiki/Cryptography#Export_controls) happened in the 1990s. The conversation prior to this event was rife with controversy. Here are some paraphrased FAQs from the era:

- “If encryption is free how will national security continue to be assured?”
- “If these ideas become a commodity, bad people will use them to become worse!”

or one of my favorites,

- “These ideas are dangerous because I do not understand them.”

Fortunately, history was on the side of the algorithm authors and now we have commodified encryption and can securely buy stuff from Amazon. Mission accomplished. <em>Pats own back.</em>

Unfortunately, everything didn’t go as planned. SSL certificate vendors built small empires on asymmetric knowledge about a complicated process. In the USA, the National Security Agency influenced vendors to inject secret backdoors into their security products. Web browsers were installed with poorly implemented SSL certificate management. Academics wrote papers about experiments to break various kinds of security, then published them.

So where does the casual web developer stand in this world? There’s too much chaos for any rational thought — besides, <em>all I want is a secure webpage that just works!</em>

This story typically ends with the casual web developer paying some US dollars (usually around $30 to $80) to a company to sell them a single SSL certificate which is only good for a couple of years and only works for a single URL. The process to perform this transaction is esoteric, confusing, and requires a pretty decent understanding of the underlying infrastructure to comprehend, let alone transact.

This created a business culture of “SSL experts,” to which the author belongs. These are usually people who know enough about encryption to bring existing applied cryptography to any software application. These people understood that their title was an illusion and the only reason they are considered expert is because OpenSSL was authored as a monolithic Swiss Army chainsaw and they took the time to read the operations manual in order to use it without killing themselves. We thought: <strong>“There must be a better way!”</strong>

[CAcert](http://www.cacert.org) was a swing and a miss, in part because their political clout didn’t reach deep into the Illuminati of root level Certificate Authority holders.

So-called “self-signed” certificates are worthless because they carry with them no authenticity. You needn’t waste your time using encryption when you don’t even know if the encrypted thing originated from the author you so desperately want to protect.

Turns out, in 2016, there is a better way. It’s called...

### Let’s Encrypt!

Through [good partners](https://letsencrypt.org/sponsors/), the [Internet Security Research Group](https://letsencrypt.org/isrg/) was created and built a software pipeline to issue valid, signed SSL certificates in a programmatic way, for free, to anyone in the world.

They’ve got sick [APIs](https://letsencrypt.readthedocs.io/en/latest/)!

This means that casual web developer can now use the software tools, like they do for developing websites, to give those websites transport security. For free.

Now, when someone asks me to provide expert services for SSL, I will use Let’s Encrypt. I strongly encourage anyone who makes webpages to use Let’s Encrypt.

[Encrypt all the things](https://encryptallthethings.net). Ensure your rights online!
