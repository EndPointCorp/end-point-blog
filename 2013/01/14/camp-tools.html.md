---
author: Jeff Boes
gh_issue_number: 749
tags: shell, camps
title: Camp tools
---

[Devcamps](http://www.devcamps.org/) are such a big part of my everyday work that I can’t imagine life without them. Over the years, I developed some short-cuts in navigating camps that I also can’t live without: I share them below.

```
function camp_top() {
  if [ -n "$1" ]
  then
      cd ~/camp${1}
  elif [[ $(pwd) =~ 'camp' ]]
  then
      until [[ $(basename $(pwd)) =~ '^camp[[:digit:]]+' ]]
      do
          if [[ $(pwd) =~ 'camp' ]]
          then
              cd ..
          else
              break
          fi
      done
  fi
}
alias ct='camp_top; pwd'

function cat_root() {
  camp_top $*
  cd catalogs/* >/dev/null
}
alias cr='cat_root; pwd'

function pages_root() {
  cat_root $*
  cd pages >/dev/null
}
alias pr='pages_root; pwd'

function what_camp() {
  c=$( camp_top $* 2> /dev/null; basename $( pwd ))
  echo $c
}
```

(“cat_root” and “pages_root” are very [Interchange](http://www.icdevgroup.org/i/dev)-specific; you may find other short-cuts more useful in your particular camp.)

There’s nothing terribly ground-breaking here, but if bash is not your native shell-tongue, then you might find these useful.

What I do is to stash these somewhere like “$HOME/.bash_camps”, then alter my .bashrc:

```
# Source campy definitions
if [ -f ~/.bash_camps ]; then
 . ~/.bash_camps
fi
```

That’s all it takes. Have you a camp-y shell script, function, or alias? Please share in the comments!
