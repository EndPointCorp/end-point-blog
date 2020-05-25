---
author: Jon Jensen
gh_issue_number: 192
tags: shell, perl, python, ruby
title: File test comparison table for shell, Perl, Ruby, and Python
---

A few days ago, my co-worker Richard asked how in Python you would do the -x Bourne shell and Perl file test that checks whether a file is executable. This is (for me, at least) a really commonly used function but one I hadn’t needed to do yet in Python, so I looked it up.

That wasn’t so hard to find, but then I wondered about the other shell and Perl file tests that I use all the time. Finding equivalents for those was harder than I expected. A web search didn’t turn much up aside from language holy wars and limited answers, but I didn’t find any exhaustive list.

So I made my own. Below is a table comparing file test operators in the original Bourne shell-compatibles bash, ksh, and zsh; Perl’s expanded set; Ruby’s which was derived first from Perl; and equivalent Python code.

There are still some blanks where I didn’t find a good equivalent. Of course I’m sure it’s possible with enough custom logic to achieve the same end, but I have tried to stick with relatively simple formulations using built-in functions for now. I’ll be happy to fill in the blanks if any readers make suggestions.

Performance notes on avoiding multiple stats of the same file:

- Starting with Perl 5.9.1, file tests can be “stacked” and will use a single stat for all tests, e.g. -f -x file. In older versions of Perl you can do -f file && -x _ instead.

- Ruby’s File::Stat class can be used to cache a stat for multiple tests.

- Python’s os.stat(file).st_mode can be stored and used for multiple tests.

Unless otherwise specified, these tests follow symbolic links and operate on the target of the link, rather than the link itself.

All tests return boolean true or false unless otherwise noted.

<style>
tr { background: #f1f1f1 !important; }
</style>
<div class="table-scroll">
<table>
<tr>
<th>Test</th>
<th>bash/ksh/zsh</th>
<th>Perl</th>
<th>Ruby</th>
<th>Python</th>
</tr>

<tbody>
<tr>
<td rowspan="2">File is readable by effective uid/gid</td>
<td rowspan="2"></td>
<td rowspan="2">-r 'file'</td>
<td>test ?r, 'file'</td>
<td rowspan="2">os.access('file', os.R_OK)</td>
</tr>

<tr>
<td>File.readable?('file')</td>
</tr>

<tr>
<td rowspan="2">File is writable by effective uid/gid</td>
<td rowspan="2"></td>
<td rowspan="2">-w 'file'</td>
<td>test ?w, 'file'</td>
<td rowspan="2">os.access('file', os.W_OK)</td>
</tr>

<tr>
<td>File.writable?('file')</td>
</tr>

<tr>
<td rowspan="2">File is executable by effective uid/gid</td>
<td rowspan="2"></td>
<td rowspan="2">-x 'file'</td>
<td>test ?x, 'file'</td>
<td rowspan="2">os.access('file', os.X_OK)</td>
</tr>

<tr>
<td>File.executable?('file')</td>
</tr>

<tr>
<td rowspan="2">File is owned by effective uid</td>
<td rowspan="2">-O file</td>
<td rowspan="2">-o 'file'</td>
<td>test ?o, 'file'</td>
<td rowspan="2">os.stat('file').st_uid == os.geteuid()</td>
</tr>

<tr>
<td>File.owned?('file')</td>
</tr>

<tr>
<td rowspan="2">File is owned by the effective gid</td>
<td rowspan="2">-G file</td>
<td rowspan="2">(stat('file'))[5] == $)</td>
<td>test ?G, 'file'</td>
<td rowspan="2">os.stat('file').st_gid == os.getegid()</td>
</tr>

<tr>
<td>File.grpowned?('file')</td>
</tr>

<tr>
<td rowspan="2">File is readable by real uid/gid</td>
<td rowspan="2">-r file</td>
<td rowspan="2">-R 'file'</td>
<td>test ?R, 'file'</td>
<td rowspan="2">os.access('file', os.R_OK)</td>
</tr>

<tr>
<td>File.readable_real?('file')</td>
</tr>

<tr>
<td rowspan="2">File is writable by real uid/gid</td>
<td rowspan="2">-w file</td>
<td rowspan="2">-W 'file'</td>
<td>test ?W, 'file'</td>
<td rowspan="2">os.access('file', os.W_OK)</td>
</tr>

<tr>
<td>File.writable_real?('file')</td>
</tr>

<tr>
<td rowspan="2">File is executable by real uid/gid</td>
<td rowspan="2">-x file</td>
<td rowspan="2">-X 'file'</td>
<td>test ?X, 'file'</td>
<td rowspan="2">os.access('file', os.X_OK)</td>
</tr>

<tr>
<td>File.executable_real?('file')</td>
</tr>

<tr>
<td>File is owned by real uid</td>
<td></td>
<td>-O 'file'</td>
<td>test ?O, 'file'</td>
<td>os.stat('file').st_uid == os.getuid()</td>
</tr>

<tr>
<td rowspan="2">File exists</td>
<td>-e file</td>
<td rowspan="2">-e 'file'</td>
<td>test ?e, 'file'</td>
<td rowspan="2">os.path.exists('file')</td>
</tr>

<tr>
<td>-a file</td>
<td>File.exist?('file')</td>
</tr>

<tr>
<td rowspan="2">File has zero size (is empty)</td>
<td rowspan="2">-f file -a ! -s file</td>
<td rowspan="2">-z 'file'</td>
<td>test ?z, 'file'</td>
<td>os.path.getsize('file') == 0</td>
</tr>

<tr>
<td>File.zero?('file')</td>
<td>os.stat('file').st_size == 0</td>
</tr>

<tr>
<td rowspan="2">File exists and has size greater than zero</td>
<td rowspan="2">-s file</td>
<td rowspan="2">-s 'file' <em>(boolean and returns size in bytes)</em></td>
<td>test ?s, 'file' <em>(boolean: returns nil if doesn't exist or has zero size, size of the file otherwise)</em></td>
<td>os.path.getsize('file') > 0</td>
</tr>

<tr>
<td>File.size?('file') <em>(same)</em><br/>
</td><td>os.stat('file').st_size > 0</td>
</tr>

<tr>
<td rowspan="2">File exists, return size in bytes</td>
<td rowspan="2"></td>
<td rowspan="2">-s 'file'</td>
<td rowspan="2">File.size('file')</td>
<td>os.path.getsize('file')</td>
</tr>

<tr>
<td>os.stat('file').st_size</td>
</tr>

<tr>
<td rowspan="2">File is a plain file</td>
<td rowspan="2">-f file</td>
<td rowspan="2">-f 'file'</td>
<td>test ?f, 'file'</td>
<td>os.path.isfile('file')</td>
</tr>

<tr>
<td>File.file?('file')</td>
<td>stat.S_ISREG(os.stat('file').st_mode)</td>
</tr>

<tr>
<td rowspan="2">File is a directory</td>
<td rowspan="2">-d file</td>
<td rowspan="2">-d 'file'</td>
<td>test ?d, 'file'</td>
<td>os.path.isdir('file')</td>
</tr>

<tr>
<td>File.directory?('file')</td>
<td>stat.S_ISDIR(os.stat('file').st_mode)</td>
</tr>

<tr>
<td rowspan="2">File is a symbolic link</td>
<td>-h file</td>
<td rowspan="2">-l 'file'</td>
<td>test ?l, 'file'</td>
<td>os.path.islink('file')</td>
</tr>

<tr>
<td>-L file</td>
<td>File.symlink?('file')</td>
<td>stat.S_ISLNK(os.lstat('file').st_mode)</td>
</tr>

<tr>
<td rowspan="2">File is a named pipe (FIFO)</td>
<td rowspan="2">-p file</td>
<td rowspan="2">-p 'file' <em>(can also be used on a filehandle)</em></td>
<td>test ?p, 'file'</td>
<td rowspan="2">stat.S_ISFIFO(os.stat('file').st_mode)</td>
</tr>

<tr>
<td>File.pipe?('file')</td>
</tr>

<tr>
<td rowspan="2">File is a socket</td>
<td rowspan="2">-S file</td>
<td rowspan="2">-S 'file'</td>
<td>test ?S, 'file'</td>
<td rowspan="2">stat.S_ISSOCK(os.stat('file').st_mode)</td>
</tr>

<tr>
<td>File.socket?('file')</td>
</tr>

<tr>
<td rowspan="2">File is a block special file</td>
<td rowspan="2">-b file</td>
<td rowspan="2">-b 'file'</td>
<td>test ?b, 'file'</td>
<td rowspan="2">stat.S_ISBLK(os.stat('file').st_mode)</td>
</tr>

<tr>
<td>File.blockdev?('file')</td>
</tr>

<tr>
<td rowspan="2">File is a character special file</td>
<td rowspan="2">-c file</td>
<td rowspan="2">-c 'file'</td>
<td>test ?c, 'file'</td>
<td rowspan="2">stat.S_ISCHR(os.stat('file').st_mode)</td>
</tr>

<tr>
<td>File.chardev?('file')</td>
</tr>

<tr>
<td>File type (returns string 'file', 'directory', 'characterSpecial', 'blockSpecial', 'fifo', 'link', 'socket', or 'unknown'</td>
<td></td>
<td></td>
<td>File.ftype('file')</td>
<td></td>
</tr>

<tr>
<td rowspan="2">Filehandle or descriptor is opened to a tty</td>
<td rowspan="2">-t fd</td>
<td rowspan="2">-t $fh</td>
<td>fd.isatty</td>
<td rowspan="2">os.isatty(fd)</td>
</tr>

<tr>
<td>fd.tty?</td>
</tr>

<tr>
<td rowspan="2">File has setuid bit set</td>
<td rowspan="2">-u file</td>
<td rowspan="2">-u 'file'</td>
<td>test ?u, 'file'</td>
<td rowspan="2">os.stat('file').st_mode & stat.S_ISGID</td>
</tr>

<tr>
<td>File.setuid?('file')</td>
</tr>

<tr>
<td rowspan="2">File has setgid bit set</td>
<td rowspan="2">-g file</td>
<td rowspan="2">-g 'file'</td>
<td>test ?g, 'file'</td>
<td rowspan="2">os.stat('file').st_mode & stat.S_ISUID</td>
</tr>

<tr>
<td>File.setgid?('file')</td>
</tr>

<tr>
<td rowspan="2">File has sticky bit set</td>
<td rowspan="2">-k file</td>
<td rowspan="2">-k 'file'</td>
<td>test ?k, 'file'</td>
<td rowspan="2">os.stat('file').st_mode & stat.S_ISVTX</td>
</tr>

<tr>
<td>File.sticky?('file')</td>
</tr>

<tr>
<td>File is an ASCII text file (heuristic guess)</td>
<td></td>
<td>-T 'file'</td>
<td></td>
<td></td>
</tr>

<tr>
<td>File is a "binary" file (opposite of -T)</td>
<td></td>
<td>-B 'file'</td>
<td></td>
<td></td>
</tr>

<tr>
<td rowspan="2">File modification time</td>
<td rowspan="2"></td>
<td>(stat('file'))[9]</td>
<td>test ?M, 'file' <em>(returns Time object)</em></td>
<td rowspan="2">os.stat('file').st_mtime</td>
</tr>

<tr>
<td>-M 'file' <em>(script start time minus file modification time, in days)</em></td>
<td>File.mtime('file') <em>(same)</em></td>
</tr>

<tr>
<td rowspan="2">File access time</td>
<td rowspan="2"></td>
<td>(stat('file'))[8]</td>
<td>test ?A, 'file' <em>(returns Time object)</em></td>
<td rowspan="2">os.stat('file').st_atime</td>
</tr>

<tr>
<td>-A 'file' <em>(script start time minus file access time, in days)</em></td>
<td>File.atime('file') <em>(same)</em></td>
</tr>

<tr>
<td rowspan="2">Inode change time (Unix)</td>
<td rowspan="2"></td>
<td>(stat('file'))[10]</td>
<td>test ?C, 'file' <em>(returns Time object)</em></td>
<td rowspan="2">os.stat('file').st_ctime</td>
</tr>

<tr>
<td>-C 'file' <em>(script start time minus inode change time, in days)</em></td>
<td>File.ctime('file') <em>(same)</em></td>
</tr>

<tr>
<td>File has been modified since it was last read</td>
<td>-N file</td>
<td></td>
<td></td>
<td></td>
</tr>

<tr>
<td>file1 is newer (according to modification date) than file2, or if file1 exists and file2 does not</td>
<td>file1 -nt file2</td>
<td>(stat('file1'))[9] > (stat('file2'))[9]</td>
<td>test ?>, 'file1', 'file2'</td>
<td>os.path.exists('file1') and (not os.path.exists('file2') or os.stat('file1').st_mtime > os.stat('file2').st_mtime)</td>
</tr>

<tr>
<td>file1 is older than file2, or if file2 exists and file1 does not</td>
<td>file1 -ot file2</td>
<td>(stat('file1'))[9] < (stat('file2'))[9]</td>
<td>test ?<, 'file1', 'file2'</td>
<td>os.path.exists('file2') and (not os.path.exists('file1') or os.stat('file1').st_mtime < os.stat('file2').st_mtime)</td>
</tr>

<tr>
<td>file1 and file2 refer to the same device and inode numbers</td>
<td>file1 -ef file2</td>
<td>join(':', (stat('file1'))[0,1]) eq join(':', (stat('file2'))[0,1])</td>
<td>test ?-, 'file1', 'file2'</td>
<td>os.path.samefile('file1', 'file2')</td>
</tr>

<tr>
<td>file1 and file2 have the same modification times</td>
<td></td>
<td>(stat('file1'))[9] == (stat('file2'))[9]</td>
<td>test ?=, 'file1', 'file2'</td>
<td>os.stat('file1').st_mtime == os.stat('file2').st_mtime</td>
</tr>

</tbody></table></div>

Complete details are in the manuals for each language:

- bash: [`man bash`](https://linux.die.net/man/1/bash) and search for “CONDITIONAL EXPRESSIONS”
- ksh: [`man pdksh`](https://linux.die.net/man/1/pdksh) and search for “test expression”
- zsh: [`man zshmisc`](https://linux.die.net/man/1/zshmisc) and search for “CONDITIONAL EXPRESSIONS”
- Perl: [`perldoc -f -f`](https://perldoc.perl.org/functions/-X.html), [filetest pragma](https://perldoc.perl.org/filetest.html)
- Ruby: [File class](https://ruby-doc.org/core-2.5.1/File.html) ([summary version](https://www.tutorialspoint.com/ruby/ruby_file_methods.htm)) and [test() built-in](https://ruby-doc.org/core-1.8.7/Kernel.html#M001085), [IO class](https://ruby-doc.org/core-2.5.1/IO.html) docs
- Python: [os.access](https://docs.python.org/3/library/os.html#os.access), [os.stat](https://docs.python.org/3/library/os.html#os.stat), [stat() results](https://docs.python.org/3/library/stat.html), [os.path](https://docs.python.org/3/library/os.path.html#module-os.path)
