---
author: Terry Grant
title: Vim — working with encryption
github_issue_number: 615
tags:
- security
- vim
date: 2012-05-16
---



On occasion I have to work with encrypted files for work or personal use. I am partial to a Linux environment and I prefer Vim as my text editor, even when I am only reading a file. Vim supports quite a few different ways of interfacing with external encryption packages. I only use two of those variations as described below.

Vim comes packaged with a default encryption mechanism referred to as VimCrypt in the documentation. I typically use this functionality as a temporary solution in a situation where my GPG is not immediately available, like a remote system that is not mine. 

### Using Vim’s default VimCrypt feature

Creating a new encrypted file or open a plain text file you wish to encrypt:

```
vim -x <filename></filename>
```

This will create a new file if it does not exist or open an existing file and then prompt you for a password. This password is then used as the key to encrypt and decrypt the specified file. Upon saving and exiting this file, it will be saved in this encrypted format using your crypt key.

You can also save and encrypt an open file you are currently working on like so. Please note this is a **capital X**: 

```
:X 
```
This will also ask you for a password to encrypt the file.

**Reasons I usually don’t use this option:**

- Vim uses a weak encryption method by default. Vim encrypts the file using an encryption method ‘zip’, the same encryption algorithm that is used by Pkzip (known to be flawed). You can set the default encryption to use the more secure ‘blowfish’ cipher. For more information see the documentation.

```
Set the cryptmethod to use the blowfish cipher
:setlocal cm=blowfish 

Documentation on Vim Encryption
:h :X
```
  - Typically uses swap files that can compromise the security of the encrypted file. You can turn this off by using the 'n' flag.

```
vim -xn <filename>
```

### Integrating with GPG

In order to seamlessly integrate with GPG encrypted files you will need to add the following to your .vimrc file

```plain
" Transparent editing of gpg encrypted files.
" By Wouter Hanegraaff
augroup encrypted
  au!

  " First make sure nothing is written to ~/.viminfo while editing
  " an encrypted file.
  autocmd BufReadPre,FileReadPre *.gpg set viminfo=
  " We don't want a swap file, as it writes unencrypted data to disk
  autocmd BufReadPre,FileReadPre *.gpg set noswapfile

  " Switch to binary mode to read the encrypted file
  autocmd BufReadPre,FileReadPre *.gpg set bin
  autocmd BufReadPre,FileReadPre *.gpg let ch_save = &ch|set ch=2
  " (If you use tcsh, you may need to alter this line.)
  autocmd BufReadPost,FileReadPost *.gpg '[,']!gpg --decrypt 2> /dev/null

  " Switch to normal mode for editing
  autocmd BufReadPost,FileReadPost *.gpg set nobin
  autocmd BufReadPost,FileReadPost *.gpg let &ch = ch_save|unlet ch_save
  autocmd BufReadPost,FileReadPost *.gpg execute ":doautocmd BufReadPost " . expand("%:r")

  " Convert all text to encrypted text before writing
  " (If you use tcsh, you may need to alter this line.)
  autocmd BufWritePre,FileWritePre *.gpg '[,']!gpg --default-recipient-self -ae 2>/dev/null
  " Undo the encryption so we are back in the normal text, directly
  " after the file has been written.
  autocmd BufWritePost,FileWritePost *.gpg u
augroup END
```
Source: [Vim Wiki—​Encryption](http://vim.wikia.com/wiki/Encryption) 

This works by detecting the extension on the files you are opening with Vim. This allows you to open, edit, and save files as if they were plain text in a seamless fashion.

Now you can create a new GPG encrypted file or edit an existing GPG encrypted doing this: 

```
vim <filename>.gpg
```

This should prompt you for GPG password either with a GUI window or command line depending on your environment’s configuration. If the file did not exist Vim creates one and when you save it will encrypt when you write and quit.

Another thing I like to do is save a file that I have already decrypted, but want to save in plain text. This can be done by simply opening the encrypted GPG file as seen above and change the extension when saving. Simply save like so: 

```
:w <newfilename>.txt
```
Any extension other than .gpg will save your file as plain text.  

**Reason to use GPG**

- Much safer encryption as it uses GPG 
- No swap files thanks to this line in .vimrc autocmd BufReadPre,FileReadPre *.gpg set noswapfile

Of course when using Vim there are many features and many different ways of doing this. This is simply how I use Vim to easily work with encrypted files in my daily life.

For more information on Vim and external encryption programs please see and making use of GPG: 

- [Vim Encryption](http://vim.wikia.com/wiki/Encryption)
- [Working with GPG — Linux](http://www.cyberciti.biz/tips/linux-how-to-encrypt-and-decrypt-files-with-a-password.html)


