---
title: Aligning monospace font text columns with an old Unix tool
author: Jon Jensen
date: 2022-05-30
tags:
- tips
- tools
- vim
- visual-studio-code
- intellij-idea
github_issue_number: 1868
---

![Photo of old wooden bridge with moss on it](/blog/2022/05/aligning-fixed-width-font-text-columns/20220316_183928.webp)
Photo by Garrett Skinner

### A blast from 1990: column

A while back I learned of a nice old Unix command-line tool called `column`. It first appeared in 4.3BSD-Reno, released in July 1990. (This is not to be confused with the different, even older Unix tool `col`.)

`column` formats plain text into nice columns based on the width of the input separated by tabs or groups of spaces.

For example, take this mess found in a server's `/etc/fstab` file defining filesystem mount points. It is a real example lightly redacted to remove business details. You may need to scroll right to see the end of the fairly long lines:

```plain
/data3/customer_uploads   /home/interch/htdocs/shared/customer_uploads none    rw,bind 0   0
/data3/customer_images    /home/interch/htdocs/shared/customer_images  none    rw,bind 0   0
/data3/images/items       home/interch/htdocs/images/items     none    rw,bind 0       0
/data3/images/thumb       home/interch/htdocs/images/thumb     none    rw,bind 0       0
/data3/upload_images       /home/interch/upload_images     none    rw,bind 0       0
/data3/design    /home/interch/htdocs/shared/design  none    rw,bind 0   0
/data3/design_temp   /home/interch/htdocs/shared/design_temp none    rw,bind 0   0
/data3/reports/cat1       /home/interch/htdocs/cat-numero-uno/images/reports     none    rw,bind 0       0
/data3/reports/cat2       /home/interch/htdocs/cat-zahl-zwei/images/reports     none    rw,bind 0       0
/data3/reports/cat3	/home/interch/htdocs/cat-number-three/images/reports	none	rw,bind	0	0
/data3/reports/cat4    /home/interch/htdocs/cat-quatre/images/reports     none    rw,bind 0       0
/data3/reports/cat5    /home/interch/htdocs/cat-pět/images/reports     none    rw,bind 0       0
/data3/shared_var /home/interch/catalogs/shared/var none    rw,bind 0 0
```

That is really unsightly and includes a mix of spaces and tabs.

If we feed it to `column -t` we get the same data aligned much nicer:

```plain
% column -t /etc/fstab
/data3/customer_uploads  /home/interch/htdocs/shared/customer_uploads          none  rw,bind  0  0
/data3/customer_images   /home/interch/htdocs/shared/customer_images           none  rw,bind  0  0
/data3/images/items      home/interch/htdocs/images/items                      none  rw,bind  0  0
/data3/images/thumb      home/interch/htdocs/images/thumb                      none  rw,bind  0  0
/data3/upload_images     /home/interch/upload_images                           none  rw,bind  0  0
/data3/design            /home/interch/htdocs/shared/design                    none  rw,bind  0  0
/data3/design_temp       /home/interch/htdocs/shared/design_temp               none  rw,bind  0  0
/data3/reports/cat1      /home/interch/htdocs/cat-numero-uno/images/reports    none  rw,bind  0  0
/data3/reports/cat2      /home/interch/htdocs/cat-zahl-zwei/images/reports     none  rw,bind  0  0
/data3/reports/cat3      /home/interch/htdocs/cat-number-three/images/reports  none  rw,bind  0  0
/data3/reports/cat4      /home/interch/htdocs/cat-quatre/images/reports        none  rw,bind  0  0
/data3/reports/cat5      /home/interch/htdocs/cat-pět/images/reports           none  rw,bind  0  0
/data3/shared_var        /home/interch/catalogs/shared/var                     none  rw,bind  0  0
```

That isn't just prettier! It also makes some things stand out prominently at a glance:

* In the second column there are two mount points not starting with `/`.
* It's easy to see that most of the paths in the second column start with `/home/interch/htdocs/` and the few that don't, stand out.
* The final 4 columns are all identical, which was unclear in the unaligned original.

### Text tables to JSON

The [util-linux](https://en.wikipedia.org/wiki/Util-linux) version of `column` includes extra options beyond the original. One very useful one is `-J` or `--json` which produces a JSON object for each row based on column names you define in the argument `-N` or `--table-columns`.

Reviewing [`man fstab`](https://www.man7.org/linux/man-pages/man5/fstab.5.html) for details on what each column is used for in the sample above, we can instruct `column` to produce JSON output like this:

```sh
% column -J -n fstab -N spec,file,vfstype,mntops,freq,passno /etc/fstab
```

Which gives us this result:

```json
{
   "fstab": [
      {
         "spec": "/data3/customer_uploads",
         "file": "/home/interch/htdocs/shared/customer_uploads",
         "vfstype": "none",
         "mntops": "rw,bind",
         "freq": "0",
         "passno": "0"
      },{
         "spec": "/data3/customer_images",
         "file": "/home/interch/htdocs/shared/customer_images",
         "vfstype": "none",
         "mntops": "rw,bind",
         "freq": "0",
         "passno": "0"
      },{
         "spec": "/data3/images/items",
         "file": "home/interch/htdocs/images/items",
         "vfstype": "none",
         "mntops": "rw,bind",
         "freq": "0",
         "passno": "0"
      },{
         "spec": "/data3/images/thumb",
         "file": "home/interch/htdocs/images/thumb",
         "vfstype": "none",
         "mntops": "rw,bind",
         "freq": "0",
         "passno": "0"
      },{
         "spec": "/data3/upload_images",
         "file": "/home/interch/upload_images",
         "vfstype": "none",
         "mntops": "rw,bind",
         "freq": "0",
         "passno": "0"
      },{
         "spec": "/data3/design",
         "file": "/home/interch/htdocs/shared/design",
         "vfstype": "none",
         "mntops": "rw,bind",
         "freq": "0",
         "passno": "0"
      },{
         "spec": "/data3/design_temp",
         "file": "/home/interch/htdocs/shared/design_temp",
         "vfstype": "none",
         "mntops": "rw,bind",
         "freq": "0",
         "passno": "0"
      },{
         "spec": "/data3/reports/cat1",
         "file": "/home/interch/htdocs/cat-numero-uno/images/reports",
         "vfstype": "none",
         "mntops": "rw,bind",
         "freq": "0",
         "passno": "0"
      },{
         "spec": "/data3/reports/cat2",
         "file": "/home/interch/htdocs/cat-zahl-zwei/images/reports",
         "vfstype": "none",
         "mntops": "rw,bind",
         "freq": "0",
         "passno": "0"
      },{
         "spec": "/data3/reports/cat3",
         "file": "/home/interch/htdocs/cat-number-three/images/reports",
         "vfstype": "none",
         "mntops": "rw,bind",
         "freq": "0",
         "passno": "0"
      },{
         "spec": "/data3/reports/cat4",
         "file": "/home/interch/htdocs/cat-quatre/images/reports",
         "vfstype": "none",
         "mntops": "rw,bind",
         "freq": "0",
         "passno": "0"
      },{
         "spec": "/data3/reports/cat5",
         "file": "/home/interch/htdocs/cat-pět/images/reports",
         "vfstype": "none",
         "mntops": "rw,bind",
         "freq": "0",
         "passno": "0"
      },{
         "spec": "/data3/shared_var",
         "file": "/home/interch/catalogs/shared/var",
         "vfstype": "none",
         "mntops": "rw,bind",
         "freq": "0",
         "passno": "0"
      }
   ]
}
```

JSON takes a lot more room, and of course is not the format Linux expects for this particular file, but transforming tabular data to JSON format in other situations can be more readable for exchange across different systems since each field is labeled, and unused fields can be omitted. Plus JSON syntax is rigorously defined, nested data structures are possible, etc.

### Columnizing lists

All versions of `column` can also columnize lists, either horizontally (across) or vertically (down). Take this list of people's names:

```plain
Amy
Anna
Bob
Brenda
Cameron
Doug
Emily
Frank
Jane
Jill
Jim
Joe
John
Karen
Kate
Liz
Mary
Mike
Sarah
Steve
Victoria
```

Put that in file `/tmp/names` and `column` will format it in columns fitting the width of your terminal:

```plain
% column /tmp/names
Amy		Cameron		Jane		John		Mary		Victoria
Anna		Doug		Jill		Karen		Mike
Bob		Emily		Jim		Kate		Sarah
Brenda		Frank		Joe		Liz		Steve
```

It uses 2 or more tab characters to separate the columns, based on standard terminal 8-space tab stops, so the above doesn't look right here on the web.

What appears in my terminal looks like:

```plain
% column /tmp/names
Amy             Cameron         Jane            John            Mary            Victoria
Anna            Doug            Jill            Karen           Mike
Bob             Emily           Jim             Kate            Sarah
Brenda          Frank           Joe             Liz             Steve
```

Or you can use `column -t` that we discussed earlier to format the columns more compactly with spaces:

```plain
% column /tmp/names | column -t
Amy     Cameron  Jane  John   Mary   Victoria
Anna    Doug     Jill  Karen  Mike   
Bob     Emily    Jim   Kate   Sarah  
Brenda  Frank    Joe   Liz    Steve  
```

You can also ask for the list to be delivered horizontally, rather than vertically, with `column -x`:

```plain
% column -x /tmp/names | column -t
Amy    Anna   Bob       Brenda  Cameron  Doug
Emily  Frank  Jane      Jill    Jim      Joe
John   Karen  Kate      Liz     Mary     Mike
Sarah  Steve  Victoria                   
```

Note that it isn't doing anything to affect your ordering. You can order the lines in your original file however you want and it will preserve them. But other tools can help you here: Use `sort -u` to sort alphabetically and remove duplicates.

For more options and details see the `column` man page for the [util-linux column](https://man7.org/linux/man-pages/man1/column.1.html) version or [FreeBSD column](https://www.freebsd.org/cgi/man.cgi?query=column&apropos=0&sektion=0&manpath=FreeBSD+13.1-RELEASE+and+Ports&arch=default&format=html) version (same as macOS).

### A blast from 1974: pr

There is an even older Unix tool for columnizing lists in the same way. It is called `pr` and dates to First Edition Unix in 1971, but did not gain the options we are using here until Fifth Edition Unix in 1974 as seen in the [V6 pr man page](https://minnie.tuhs.org/cgi-bin/utree.pl?file=V6/usr/man/man1/pr.1).

We need to tell it how many columns to produce, so we will ask for 6 columns as `column` was doing above. Note that `pr` emits a curious mix of tabs and spaces, which `cat -t` reveals here as `^I` (since a tab is the same thing as Control+I):

```plain
% pr -t -6 /tmp/names | cat -t
Amy^I    Cameron^IJane^I    John^ILiz^I    Sarah
Anna^I    Doug^IJill^I    Karen^IMary^I    Steve
Bob^I    Emily^IJim^I    Kate^IMike^I    Victoria
Brenda^I    Frank^IJoe
```

But in a terminal it looks fine:

```plain
% pr -t -6 /tmp/names
Amy         Cameron     Jane        John        Liz         Sarah
Anna        Doug        Jill        Karen       Mary        Steve
Bob         Emily       Jim         Kate        Mike        Victoria
Brenda      Frank       Joe
```

See the many more options of pr in the [GNU coreutils pr man page](https://man7.org/linux/man-pages/man1/pr.1.html) and [FreeBSD pr man page](https://www.freebsd.org/cgi/man.cgi?query=pr&apropos=0&sektion=0&manpath=FreeBSD+13.1-RELEASE+and+Ports&arch=default&format=html) (same as macOS).

### A blast from 1979: expand

A useful tool for dealing with tabs is `expand`, which [first appeared in 3BSD](https://github.com/dank101/3BSD/blob/master/cmd/expand.c) in 1979. (Despite the FreeBSD and macOS man pages saying it appeared in 1BSD, I don't see it there or in 2BSD.)

We can use it to convert tabs to spaces just like a terminal would:

```plain
% pr -t -6 /tmp/names | expand | cat -t    
Amy         Cameron     Jane        John        Liz         Sarah
Anna        Doug        Jill        Karen       Mary        Steve
Bob         Emily       Jim         Kate        Mike        Victoria
Brenda      Frank       Joe
```

`expand` accepts the optional `-t` argument with a number to use as tabstop width instead of the default 8.

### And unexpand

I have used `expand` for years, but only recently learned of `unexpand` which goes the other way, converting runs of spaces into tabs:

```plain
% pr -t -6 /tmp/names | expand | unexpand -a         
Amy         Cameron     Jane        John        Liz         Sarah
Anna        Doug        Jill        Karen       Mary        Steve
Bob         Emily       Jim         Kate        Mike        Victoria
Brenda      Frank       Joe
```

It looks fine in the terminal, but let's see if it actually used tabs:

```plain
% pr -t -6 /tmp/names | expand | unexpand -a | cat -t
Amy^I    Cameron^IJane^I    John^ILiz^I    Sarah
Anna^I    Doug^IJill^I    Karen^IMary^I    Steve
Bob^I    Emily^IJim^I    Kate^IMike^I    Victoria
Brenda^I    Frank^IJoe
```

Interesting… For some reason `unexpand` doesn't actually convert all the spaces to tabs, but just one initial tab per gutter between columns. Running the output through `unexpand -a` again has no further effect. Strange.

The GNU coreutils version of `unexpand` that lives in most Linux systems is what I would call bug-compatible with the BSD version in this regard.

Oh, well. There's probably a reason.

Since it has handled turning the initial tabstop's varying number of spaces into a tab, we can easily remove the remaining fixed multiples of spaces on our own for a more compact list:

```plain
% pr -t -6 /tmp/names | expand | unexpand -a | sed 's/    //g'         
Amy     Cameron Jane    John    Liz     Sarah
Anna    Doug    Jill    Karen   Mary    Steve
Bob     Emily   Jim     Kate    Mike    Victoria
Brenda  Frank   Joe
```

### Ready at hand

`column`, `pr`, `expand`, and `unexpand` all come with most Linux and BSD systems, including macOS. It is amazing what great old tools are on many of our computers all the time, waiting to be used!

You can use these programs as filters inside your favorite text editor or IDE. For example, to achieve the same list columnization as above you can select a block of text and send it to external commands:

* In Vim, visually select text with `v` or `V` and then type `!column | expand` and press Enter.
* In VS Code you can install an extension called Filter Text (by yhirose). Once installed, type Control+K Control+F (⌘K ⌘F on macOS) and then `column | expand` and Enter.
* In IntelliJ IDEA you can install a plugin called Shell Filter (by Dennis Plöger). Once installed, select your text, then choose menu item Edit > Custom Shell Filter and then type `column -c 80 | expand` and Enter.
* Most other editors have a way to do this too. Search for "filter", "pipe", and/or "command".

Your selection will be replaced by the output.

### Unicode stumbling blocks

Note that these tools all presume one visual character takes one byte of input, so for any UTF-8 characters outside the limited classic ASCII character set that take more than 1 byte each, these tools will miscalculate the needed space between columns.

Perhaps you would like to take on the programming challenge and submit a patch to add a new `-u` option to take visual width of Unicode characters into account. 😊
