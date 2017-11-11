---
author: Szymon Lipiński
gh_issue_number: 1233
tags: shell, python
title: Adding Bash Completion To a Python Script
---

Bash has quite a nice feature, you can write a command in a console, and then press <TAB> twice. This should should you possible options you can write for this command.

I will show how to integrate this mechanism into a custom python script with two types of arguments. What's more, I want this to be totally generic. I don't want to change it when I will change the options, or change config files.

This script accepts two types of arguments. One type contains mainly flags beginning with '--', the other type is a host name taken from a bunch of chef scripts.

Let's name this script show.py - it will show some information about the host. This way I can use it with:

```bash
show.py szymon
```

The szymon part is the name of my special host, and it is taken from one of our chef node definition files.

This script also takes huge number of arguments like:

```bash
show.py --cpu --memory --format=json
```

So we have two kinds of arguments: one is a simple string, one begins with --.

To implement the bash completion on double <TAB>, first I wrote a simple python script, which is prints a huge list of all the node names:

```python
#!/usr/bin/env python

from sys import argv
import os
import json

if __name__ == "__main__":
    pattern = ""
    if len(argv) == 2:
        pattern = argv[1]

    chef_dir = os.environ.get('CHEF_DIR', None)
    if not chef_dir:
        exit(0)
    node_dirs = [os.path.join(chef_dir, "nodes"),
                 os.path.join(chef_dir, "dev_nodes")]
    node_names = []

    for nodes_dir in node_dirs:
        for root, dirs, files in os.walk(nodes_dir):
            for f in files:
                try:
                    with open(os.path.join(root, f), 'r') as nf:
                        data = json.load(nf)
                        node_names.append(data['normal']['support_name'])
                except:
                    pass

    for name in node_names:
        print name
```

Another thing was to get a list of all the program options. We used the below one liner. It uses the help information shown by the script. So each time the script changed its options, and it is shown when used show.py --help, the tab completion will have show these new options.

```bash
$CHEF_DIR/repo_scripts/show.py --help | grep '  --' | awk '{print $1}'
```

The last step to make all this work was making a simple bash script, which uses the above python script, and the one liner. I placed this script in a file $CHEF_DIR/repo_scripts/show.bash-completion.

```bash
_show_complete()
{
    local cur prev opts node_names
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts=`$CHEF_DIR/repo_scripts/show.py --help | grep '  --' | awk '{print $1}'`
    node_names=`python $CHEF_DIR/repo_scripts/node_names.py`

    if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi

    COMPREPLY=( $(compgen -W "${node_names}" -- ${cur}) )
}

complete -F _show_complete show.py
```

The last thing was to source this file, so I've added the below line in my ~/.bashrc.

```bash
source $CHEF_DIR/repo_scripts/show.bash-completion
```

And now pressing the <TAB> twice in a console shows quite nice completion options:

```bash
$ show.py <tab><tab>
Display all 42 possibilities? (y or n)
... and here go all 42 node names ...
</tab></tab>
```

```bash
$ show.py h<tab><tab>
... and here go all node names beginning with 'h' ...
</tab></tab>
```

```bash
$ show.py --<tab><tab>
.. and here go all the options beginning with -- ...
</tab></tab>
```
