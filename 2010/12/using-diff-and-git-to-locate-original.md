---
author: David Christensen
title: Using “diff” and “git” to locate original revision/source of externally modified
  files
github_issue_number: 388
tags:
- development
- git
date: 2010-12-18
---

I recently ran into an issue where I had a source file of unknown version which had been substantially modified from its original form, and I wanted to find the version of the originating software that it had originally come from to compare the changes. This file could have come from any number of the 100 tagged releases in the repository, so obviously a hand-review approach was out of the question. While there were certainly clues in the source file (i.e., copyright dates to narrow down the range of commits to review) I thought up and used this technique:

Here are our considerations:

- We know that the number of changes to the original file is likely small compared to the size of the file overall.
- Since we’re trying to uncover a likely match for the purposes of reviewing, exactness is not required; i.e., if there are lines in common with future releases, we’re interested in the changes, so a revision with the fewest number of changes is preferred over finding the *exact* version of the file that this was originally based on.

The basic thought, then, is that we want to take the content of the unversioned file (i.e., the file that was changed) and find the revision of the corresponding file in the repository with the least number of changes, which we’ll measure as the count of the lines in the source code diff. This struck me as similar to the copy detection that git does, insofar as it can detect content that is similar to some source content with a certain amount of tolerance for changes from the base. The difference in this case is that we’re comparing content across a number of refs rather than across all of the blobs in a single ref. This recipe distilled down to the following bash command:

```bash
for ref in $(git tag);
do
    echo -n $ref;
    diff -w <(git show $ref:/path/to/versioned/file 2>/dev/null) modified_file | wc -l;
done | sort -k2 -n
```

The results of running this command is a list of the tags in the repository ordered by how similar they are to the target content (most similar first). A few comments:

- We iterate through all tags in the project; while there could indeed be changes to the relevant file in intermediate versions, due to the way the release worked it’s likely the original file was based on a released (aka tagged) version.
- We’re using diff’s -w option, as the content may have changed spaces to tabs or vice versa, depending on the editor/editing habits of the original user. This helps us ensure that the changes that we’re focusing on are the ones that change something substantial.
- We’re doing a numeric sort so the lines with the least number of changes show up at the top.
- For the specific case I used this technique with, there were a number of revisions that had the least number of changed lines. Upon reviewing this smaller set of revisions (using the git diff rev1 rev2 -- path/to/content syntax), it turns out that the file in question had remained unchanged in each of these revisions, so any one of them was useful for my purposes.
- The flexibility in the version detection works in this case because this was an isolated part of the system that did not have any changes or dependencies. If there had been important changes to the system as a whole independent of the changes to this file (but which had an affect on the operation of this specific part), we would need to have a more exact method of identifying the file.
