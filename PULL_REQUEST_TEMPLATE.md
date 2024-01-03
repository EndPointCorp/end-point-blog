Before submitting a pull request, make sure to complete the following checklist:

- [ ] Have your technical and style reviewers look at your draft directly in GitHub, which will nicely convert the Markdown for display in your fork, even parsing the frontmatter into a little table! See [this example](https://github.com/EndPointCorp/end-point-blog/blob/main/2017/11/from-zero-to-https-in-an-afternoon.md).
    - Alternatively, you can create a pull request first, then on the PR, request them as reviewers. If you do, just follow the instructions below, but skip the review until after your pull request is created.
- Incorporate changes based on your reviewers' input.
    - [ ] Complete echnical review
    - [ ] Complete style review
- [ ] Include attribution for anything you don't own. This means images, but also code snippets or quotes you didn't write. Even if you do use your own image, please add an HTML comment with attribution so we know where it came from.
- [ ] Make sure you have the latest upstream changes: `git fetch upstream && git rebase upstream/main`
- [ ] Clean up your repo. Once you are done with all changes, including from reviewers, squash any commits you have into a single commit. Make sure you don't have any commits from old blog posts. It saves time when the keepers of the blog don't need to rebase and squash your commits. If you need help with this, reach out to a keeper of the blog (who are listed in the End Point internal wiki under the page of that name).
- [ ] Push all changes from your local repo to your fork on GitHub and submit a pull request. In the pull request, please mention who has reviewed the post so far.

Once your blog post has been published to the world, proofread it again. You often see mistakes after publishing that you didn't notice before, and it's not too late to fix them!