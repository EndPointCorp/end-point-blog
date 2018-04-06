---
author: Mike Farmer
gh_issue_number: 821
tags: rails, ruby, shell
title: Making use of a Unix Pipe
---

Developing in a Unix-based environment has many wonderful advantages. Thanks to [Gary Bernhardt of DestroyAllSoftware Screencasts](https://www.destroyallsoftware.com/screencasts/catalog/running-tests-asynchronously), I’ve recently discovered a new use for the Unix pipe. A pipe in Unix does exactly what you might think it would do by its name. Send something in one side and watch it come out the other. If you’ve done much in the shell, you’ve probably used pipes before where you’ve probably piped some output from one command to another. Here’s an example:

```nohighlight
$ cat foo.txt | grep bar
```

This command simply says take the output of cat and sends it to the input of grep. Pipes used in this way can yield very powerful commands in the shell.

There is another pipe in Unix and this is a [named pipe](https://en.wikipedia.org/wiki/Named_pipe). A named pipe, or a [FIFO](https://linux.die.net/man/1/mkfifo) ([First In, First Out](https://en.wikipedia.org/wiki/FIFO)), works similarly to command line pipe. You put stuff in one end and it comes out the other. To create a named pipe, you use the mkfifo command.

```nohighlight
$ mkfifo my_fifo
$ ls -l
...
prw-rw-r--  1 mikefarmer mikefarmer      0 Jun  5 21:22 my_fifo
```

Notice the “p” at the beginning of the file list. The “p” designates this file as a named pipe to the system. To try out our pipe, we will, in one terminal, listen for anything coming out of the pipe. Then in another terminal we will send some text to the pipe. To listen to the pipe we will be using cat to just display whatever comes into the pipe.

```nohighlight
$ cat my_fifo
```

Notice that when this runs, it blocks while it waits for something to come through the pipe. Now let’s push some text through the pipe. In another terminal window, I’ll just echo some text to the pipe.

```nohighlight
$ echo "hello world" > my_fifo
```

As soon as I press enter on this command, I see that the other terminal outputs “hello world” and then exits.

Now that we have a basic understanding of how the pipe works, we can set it up to run some commands. I’m going to throw my listener into a shell script that will create our pipe and start listening to and executing anything that comes out of it.

```bash
  # setup_listener.sh
  if [ ! -p commands ]; then
    mkfifo commands
  fi

  while true; do
    sh -c "clear && $(cat commands)"
  done
```

The first three lines create the pipe. The last three lines setup the listener. Remember how the process ended after the first command was sent? Well, putting this into a loop allows us to call cat repeatedly. I also added a clear call to clear my screen between each command. Now to test it out:

```nohighlight
$ sh ./setup_listener.rb
```

In another terminal:

```nohighlight
$ echo 'ls -l' > commands
```

You’ll notice that the command clears the screen in the other terminal and displays the output of the command ls -l. Nice!

Now let’s put this to some practical use. I have a Rails application that has some [Minitest](https://www.rubydoc.info/gems/minitest/5.0.4/frames) tests and a small script that I’ve put together to run all the tests. Here’s the content of of my test runner:

```ruby
# run_all_tests.rb

#!/usr/bin/env ruby
$:<<'test'

files = Dir.glob('test/**/*_test.rb')
files.each{|file| require file.sub(/^test\/|.rb$/,'')}
```

The script is a simple Ruby script that adds the test directory to the LOAD_PATH and then just requires all the files in the test directory that start with “test”. I make this script executable using a chmod +x command. Then to run it, I just call

```nohighlight
$ ./run_all_tests.rb
```

Simple. To run individual tests, I just run:

```nohighlight
$ minitest test/test_foo.rb
```

With these two commands in mind, I can now put together everything I need for my pipe. First I’m going to vertically split my screen (You can use tmux, or whatever tool you’d like. I like iTerm’s simple split screen for this.) In my terminal on the right, I’m going to startup my listener just like I did above. In the terminal on the right, I’m going to start up vim and bring up my test file. To execute my test, I’ll just use vim’s :! command to execute the test command in the shell using the % as a placeholder for the current file name in my active buffer.

```nohighlight
:!echo "minitest %" > commands
```

If I’ve done everything right, my test will run on the terminal on the right and then wait for my next command. W00T! Now I’m going to run all my tests:

```nohighlight
:!echo "./run_all_tests.rb" > commands
```

Immediately upon pressing enter, all my tests are running on the right pane! Hooray!

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/06/13/making-use-of-unix-pipe/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/06/13/making-use-of-unix-pipe/image-0.png"/></a></div>

To make things a little easier in vim, I setup some key mappings for running the tests.

```nohighlight
:nmap <leader>g :w\|:silent !echo "minitest %" > commands<cr>
:nmap <leader>G :w\|:silent !echo "./run_all_tests.rb" > commands<cr>
```

Now I don’t necessarily want these shortcuts all the time so I’m going to add these shortcuts to a file called setup_test_shortcuts.vim. Then to activate them I just run :source setup_test_shortcuts.vim. Now I have a simple shortcut in vim for running my tests!

If you are using [zeus](https://github.com/burke/zeus) then you will need to modify your shortcuts to look like this:

```nohighlight
nmap <leader>g :w\|:silent !echo "zeus test %" > commands<cr>
nmap <leader>G :w\|:silent !echo "zeus test ./run_all_tests.rb" > commands<cr>
```

Using Unix to help me in my workflow always brings a big smile to my face as I see the gains in productivity. Simple Unix concepts continue to blow my mind at their practicality and underlying simplicity.
