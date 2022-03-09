---
title: "Using a YubiKey as authentication for an encrypted disk"
author: "Zed Jensen"
tags:
- security
- sysadmin
- tips
date: 2022-03-07
github_issue_number: 1838
---

![Keys hanging on a wall](/blog/2022/03/disk-decryption-yubikey/banner.jpg)
[Image](https://unsplash.com/photos/C1P4wHhQbjM) by [Silas Köhler](https://unsplash.com/@silas_crioco) on Unsplash

Recently I built a small desktop computer to run applications that were a bit much for my laptop to handle, intending to bring it with me when I work outside my apartment. However, there was an immediate issue with this plan. Because this computer was intended for use with sensitive information/​source code, I needed to encrypt the disk, which meant that I'd need to enter a passphrase before I could boot it up.

I didn’t really want to haul a keyboard and monitor around with me, so I came up with an alternative solution: using a YubiKey as my method of authentication. This allowed me to avoid the need to type a password without giving up security. In this post I'll show you how you can do the same.

### Preparation

First off, you need a YubiKey, if you don't have one already. I ended up getting the [YubiKey 5C NFC](https://www.yubico.com/product/yubikey-5c-nfc/).

While I waited for my YubiKey to arrive, I installed Ubuntu 20.04 with full-disk encryption (using the default option of LUKS, or Linux Unified Key Setup) on the computer. I set a passphrase like normal—the process I describe in this post allows access with either this passphrase or the YubiKey.

Next, there were two packages that I needed to configure everything:

- [yubikey-personalization](https://github.com/Yubico/yubikey-personalization) allows you to change the settings on your YubiKey. I installed it from the Ubuntu repository and had no problems.
- [yubikey-luks](https://github.com/cornelinux/yubikey-luks) is what lets you use the YubiKey as an authentication method for a LUKS setup. I initially installed this from Ubuntu’s repository as well, but the version they’ve got is fairly out of date and required both a YubiKey and passphrase instead of just the YubiKey. As I mentioned earlier, the main objective of setting this up was booting without a keyboard, so I installed the tool from source as detailed in its README.

### Setup

Once you’ve got the above libraries installed, setup is simple. Step by step:

###### 1. Configure your YubiKey to use challenge-response mode

A YubiKey has at least 2 "slots" for keys, depending on the model.

We will change only the second YubiKey slot so you will still be able to use your YubiKey for two-factor auth like normal.

Plug in your YubiKey and run the following command:

```sh
ykpersonalize -2 -ochal-resp -ochal-hmac -ohmac-lt64 -oserial-api-visible
```

###### 2. Find a free LUKS slot to use for your YubiKey

LUKS also allows for multiple key slots so that you can have different passphrases to unlock the encrypted data. Up to 8 key slots are available for LUKS1, and up to 32 for LUKS2.

Most setups only use the first slot for the main passphrase, but we can check by following these steps:

- First run `lsblk` and figure out the name of your LUKS-encrypted disk partition. Mine was `nvme0n1p3`.
- Now run `sudo cryptsetup luksDump /dev/nvme0n1p3`. The output should look something like this:

```plain
LUKS header information
Version:        2
Epoch:          11
Metadata area:  [a smallish number] [bytes]
Keyslots area:  [a medium number] [bytes]
UUID:           [a UUID]
Label:          (no label)
Subsystem:      (no subsystem)
Flags:          (no flags)

Data segments:
  0: crypt
        offset: [a big number] [bytes]
        length: (whole device)
        cipher: aes-xts-plain64
        sector: 512 [bytes]

Keyslots:
  0: luks2
				[Lots of information about this slot]
Tokens:
Digests:
  0: pbkdf2
        Hash:       sha256
        Iterations: 370259
        Salt:       [A bunch of bytes in hex format]
        Digest:     [A bunch of bytes in hex format]
```

You're looking specifically for a free keyslot, and the output here only shows anything in slot 0, so slot 1 should be free.

###### 3. Assign your YubiKey to a free slot

You can do this with the following command (substituting in your own partitition name and slot number):

```sh
sudo yubikey-luks-enroll -d /dev/nvme0n1p3 -s 1
```

This command will ask you for a passphrase. It doesn't need to be a particularly complex one, because it'll only work with your YubiKey.

###### 4. Update crypttab and ykluks.cfg

Now you need to add `keyscript=/usr/share/yubikey-luks/ykluks-keyscript` to `/etc/crypttab`. For example, mine started as:

```sh
nvme0n1p3_crypt UUID=[uuid-here] none luks,discard
```

After the change, it should look like this:

```sh
nvme0n1p3_crypt UUID=[uuid-here] none luks,discard,keyscript=/usr/share/yubikey-luks/ykluks-keyscript
```

Finally, you need to configure yubikey-luks to give the passphrase you just set so you don't have to. Open `/etc/ykluks.cfg` and add the line

```sh
YUBIKEY_CHALLENGE="[your new passphrase here]"
```

Once you've added this line, run `sudo update-initramfs -u` and you're done!

### Conclusion

Now if you shut your machine off, plug in your YubiKey, and turn it on, it should boot all the way without needing a passphrase. If you forget to plug in the YubiKey before turning the computer on, you'll probably need to hold the contact button on it for a second or two and then it should boot just the same.

And there you go! A YubiKey provides neat way to securely start up a computer with an encrypted disk without needing a passphrase.
