---
author: "Ardyn Majere"
title: "Lock down your security with a smartcard based private key."
tags: Security, gpg, Yubikey, encryption, security, airgapped, authentication, ssh
---

Gnu Privacy Guard (or GPG) is a tool we use a lot at End Point. It's simplicity and quite decent security is a perfect fit for us- and there's a way to make it even safer.

Gpg uses the OpenPGP (or Pretty Good Privacy) standard to encrypt files. Normally, one creates a PGP key on their computer and just keeps the keyfile safe. A password is generally used, but as with any private key, it's only as safe as the computer it's on.

Using a smartcard can increase this security, especially if the key is generated on an airgapped machine. This way the keyfile is stored in the hardware security token, and is never exposed to the internet.

In addition, you can even store an SSH key on the card, which will enable you to log in to remote linux machines while keeping your private key secured.

While there isn't full password locking on hardware tokens, Yubikey and almost all OpenPGP keys have two pin numbers- A user pin and an administrative pin to reset the user pin. If you enter either or both three times incorrectly, the card will lock and you'll need to reload from backup (or in some cases, throw the card away) Which is why it's critical to have a backup.

There are several options for smart cards- You can use any OpenPGP compatible card and reader, or an all in one solution that's compatible with OpenPGP. For myself, it was easiest to use a Yubikey, since I already had one. (Note, you'll need a full Yubikey if you go with that brand, not the cheaper Yubico FIDO card. Check the description and make sure it mentions OpenPGP.)

The following instructions do require a basic understanding of both how to create a live CD / USB stick, as well as basic understanding of the command line, but if you're in the position of needing to use gpg, you'll probably already be at least somewhat familiar with these requirements.

To get started- you don't -have- to do this on an airgapped machine, but doing so affords the highest level of security. Simply booting from a live CD / USB is fairly easy, and if you choose an operating system that already has the smart card daemon (or sca

Before you begin, you'll need:

* A smartcard solution as described above.
* A backup smart card, or external media on which to store an encrypted copy of the key.
* A machine on which to generate the key. 
* A live OS- For this demonstration I used TAILS - The Amnesic Incognito Live System.
* A way to access these instructions.

Boot up the live machine. Note, if you're using TAILS- there are two settings you'll need to choose on the welcome screen. Click the plus button and choose the following:
Set an Administrative password- TAILS by default doesn't set a root password, and thus disallows root access, for better security. You can set one yourself.
Disable networking by clicking on 'Network Connection' and disable all networking.

Once booted, run an admin terminal, or load a terminal and type in sudo -i. It'll prompt you for the password you just set.

Ensure you can access the card, and that the smartcard daemon is installed by typing gpg --edit-card. It should display information about your smart card. 

If your live OS is missing the requisite packages needed, don't access the internet with the machine in order to install it, that would defeat the airgap. Instead, copy the installation files across using sneakernet- (Add the files to a USB key, perhaps the one you'll be using to back up your PGP key.) The packages for a Debian based machine would be: scdaemon libccid pcscd rng-tools gnupg2 

https://www.debian.org/doc/manuals/apt-offline/index.en.html

Set a pin for your card, if you haven't. 

`gpg --edit-card`

The default PIN for Yubikeys should 123456, and the default AdminPIN will be 12345678- Check the documentation that came with your key!

`gpg/card> admin` - Enable Admin features first

`gpg/card> passwd` - Set the passwords, both for the regular PIN and the AdminPIN. 

*Do not mix up your pin and adminpin! You can lock up your card, which will require a factory reset. (Which you can also do via gpg --edit-card - `gpg/card> factory-reset`*

Next step: Generate the keys. You'll want to generate at least 4096 bit RSA keys. 

*You can also use ECC & ECC if you're brave- these keys may not work with older systems and implementations of gpg, so your mileage may vary. If you are going to use this, use Curve 25519*


Run the following to generate the key:

`gpg --expert --full-gen-key`

* Key type: 1 (RSA & RSA) 
* Key size should be the maximum supported by your key. Yubikey 4 or 5 can support up to 4096. Use this for both main and subkey.
* Expiry- This is your choice. I'd set it to a year or two. I've left instructions below on how to extend your expiry dates
* Real Name, email, and comment- I recommend leaving the comment blank unless you want to provide information your email address is.  For instance- if you email is sara-jane@tardis.com, You don't need to specify the company you work for is Tardis inc in the comment.
* Next, gpg will ask you to move your mouse around- don't sprain anything while generating entropy!

That's the key generated. If you only have one spare storage which you want to use for backups, copy the revocation certificate and the ssh public key to the storage, sneak this on to your main computer, and only then copy the keys over to the backup drive. Don't attach the backup drive to anything but an airgapped machine once it holds your key!

You might as well generate an SSH key now. If you don't use it, there's no harm in having it.

`gpg --expert --edit-key <your email/key id>`

* `gpg/card> addkey` to add a key
* Type 8, rsa (set your own capabilities)
* Enable authentication and disable signing and encrypting - type s, e, a, then q to save.
* 4096 bits best bits- at least, for RSA on modern Yubikeys- If you have an older key you may be limited to 3072 or 2048. 
* You can choose to have the key expire, but ensure you have a backup method of logging in- this should be easily extended, but…
* Confirm your choices, then quit, confirming you want to save.

*For more indepth instructions, visit: https://opensource.com/article/19/4/gpg-subkeys-ssh*

Once you have the key added to your key ring, you'll need to transfer that key to your card

`gpg --edit-key <key id>`

* `gpg> keytocard` - confirm you want to move the primary key, store this in position 1 of the card
* Enter the commands key 1, keytocard, and store the subkey in position 2,
* repeat this for as many subkeys as you have. 
* Once you're done, quit, and confirm the saved changes.

If you're using an sdcard/thumb drive to back up the key, copy it over now. Remember- label the thumbdrive, keep it safe, and don't connect it to a non-airgapped machine.

To export the public ssh key you'll need to put on remote servers, you can run the command:  gpg --export-ssh-key 0x123456789ABCDE

Test your new key, make sure it works.

And that's it. Publish your new public gpg key, use your new ssh key - secure in the knowledge that your private key is locked away.
