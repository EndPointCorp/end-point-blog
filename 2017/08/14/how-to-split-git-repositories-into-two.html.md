---
author: Wojtek Ziniewicz
gh_issue_number: 1321
tags: git
title: How to split Git repositories into two
---

Ever wondered how to split your Git repo into two repos?

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2017/08/14/how-to-split-git-repositories-into-two/image-0-big.png" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2017/08/14/how-to-split-git-repositories-into-two/image-0.png"/></a></div>

First you need to find out what files and directories you want to move to separate repos. In the above example we’re moving dir3, dir4, and dir7 to repo A, and dir1, dir2, dir5, and dir8 to repo B.

### Steps

What you need to do is to go through **each and every commit** in git history for every branch and filter out commits that modify directories that you dont care about in your new repo. The only flaw of this method is that it will leave those empty, filtered out commits in the history.

#### Track all branches

First we need to start tracking all branches locally:

```bash
for i in $(git branch -r | grep -vE "HEAD|master" | sed 's/^[ ]\+//');
  do git checkout --track $i
done
```

Then copy your original repo to two separate dirs: repo_a and repo_b.

```bash
cp -a source_repo repo_a
cp -a source_repo repo_b
```

#### Filter the history

Following command will delete all dirs that exclusively belong to repo B, thus we create repo A. Filtering is not limited to directories. You can provide relative paths to files, dirs etc.

```bash
cd repo_a
git filter-branch --index-filter 'git rm --cached -r dir8 dir2 || true' -- --all

cd repo_b
git filter-branch --index-filter 'git rm --cached -r dir3 dir4 dir7 || true' -- --all
```

Note that the `|| true` prevents git from failing to filter our dirs mentioned in the `rm` clause in early stages of the git history where the dirs did not yet exist.

Look at the list of branches once again (in both repos):

```bash
git branch -l
```

#### Set new origins and push

In every repo, we need to remove the old origin and set up new origin. After it’s done, we’re ready to push.

Remove old origin:

```bash
git remote rm origin
```

Add new origin:

```bash
git remote add origin git@github.com:YourOrg/repo_a.git
```

Push all tracked branches:

```bash
git push origin --all
```

That’s it!
