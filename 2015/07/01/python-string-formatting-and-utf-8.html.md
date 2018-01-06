---
author: Muhammad Najmi bin Ahmad Zabidi
gh_issue_number: 1138
tags: python
title: Python string formatting and UTF-8 problems workaround
---

Recently I worked on a program which required me to filter hundred of lines of blog titles. Throughout the assignment I stumbled upon a few interesting problems, some of which are outlined in the following paragraphs. 

### Non Roman characters issue

During the testing session I missed one title and investigating why it happened, I found that it was simply because the title contained non-Roman characters.

Here is the code’s snippet that I was previously using:

```python
for e in results:                                                                                                                        
    simple_author=e['author'].split('(')[1][:-1].strip()                                                             
    if freqs.get(simple_author,0) < 1:                                                                                               
        print parse(e['published']).strftime("%Y-%m-%d") , "--",simple_author, "--", e['title']
```

And here is the fixed version

```python
for e in results:                                                                                                                        
    simple_author=e['author'].split('(')[1][:-1].strip().encode('UTF-8')                                                             
    if freqs.get(simple_author,0) < 1:                                                                                               
        print parse(e['published']).strftime("%Y-%m-%d") , "--",simple_author, "--", e['title'].encode('UTF-8') 
```

To fix the issue I faces I added .encode('UTF-8') in order to encode the characters with the UTF-8 encoding. Here is an example title that would have been otherwise left out:

```bash
2014-11-18 -- Unknown -- Novo website do Liquid Galaxy em Português!
```

Python 2.7 uses ASCII as its default encoding but in our case that wasn’t sufficient to scrape web contents which often contains UTF-8 characters. To be more precise, this program fetches an RSS feed in XML format and in there it finds UTF-8 characters. So when the initial Python code I wrote met UTF-8 characters, while using ASCII encoding as the default sets, it was unable to identify them and returned an error.

Here is an example of the parsing error it gave us while fetching non-roman characters while using ASCII encoding:

```bash
UnicodeEncodeError: 'ascii' codec can't encode character u'\xea' in position 40: ordinal not in range(128)
```

### Right and Left text alignment

In addition to the error previously mentioned, I also had the chance to dig into several ways of formatting output.

The following format is the one I used as the initial output format:

```python
print("Name".ljust(30)+"Age".rjust(30))
Name                                                     Age
```

#### Using “ljust” and “rjust” method

I want to improve the readability in the example above by left-justify “Name” by 30 characters and “Age” by another 30 characters distance.

Let’s try with the “*” fill character. The syntax is str.ljust(width[, fillchar])

```python
print("Name".ljust(30,'*')+"Age".rjust(30))
Name**************************                           Age
```

And now let’s add .rjust:

```python
print("Name".ljust(30,'*')+"Age".rjust(30,'#'))
Name**************************###########################Age
```

By using str, it counts from the left by 30 characters including the word “Name” which has four characters

and then another 30 characters including “Age” which has three letters, by giving us the desired output.

#### Using “format” method

Alternatively, it is possible to use the same indentation approach with the *format* string method:

```python
print("{!s:<{fill}}{!s:>{fill}}".format("Name", "Age",fill=30))
Name                                                     Age
```

And with the same progression, it is also possible to do something like:

```python
print("{!s:*<{fill}}{!s:>{fill}}".format("Name", "Age",fill=30))
Name**************************                           Age
print("{!s:*<{fill}}{!s:#>{fill}}".format("Name", "Age",fill=30))
Name**************************###########################Age
```

“format” also offers a feature to indent text in the middle. To put the desired string in the middle of the “fill” characters trail, simply use the ^ (caret) character:

```python
print("{!s:*^{fill}}{!s:#^{fill}}".format("Age","Name",fill=30))
*************Age**************#############Name#############
```

Feel free to refer the Python’s documentation on Unicode here:

[https://docs.python.org/2/howto/unicode.html](https://docs.python.org/2/howto/unicode.html)

And for the “format” method it can be referred here:

[https://www.safaribooksonline.com/library/view/python-cookbook-3rd/9781449357337/ch02s13.html](https://www.safaribooksonline.com/library/view/python-cookbook-3rd/9781449357337/ch02s13.html)

