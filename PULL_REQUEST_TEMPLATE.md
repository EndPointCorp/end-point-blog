Before submitting a pull request, make sure to complete the following checklist:

- [ ] Include attribution for anything you don't own. This means images, but also code snippets or quotes you didn't write. Even if you do use your own image, please add an HTML comment with attribution so we know where it came from.
- [ ] Make sure you have the latest upstream changes: `git fetch upstream && git rebase upstream/main`
- [ ] Clean up your repo. Once you are done with all changes, including from reviewers, squash any commits you have into a single commit. Make sure you don't have any leftover commits from old blog posts. It saves time when the keepers of the blog don't need to rebase and squash your commits. If you need help with this, reach out to a keeper of the blog (who are listed in the End Point internal wiki under the page of that name).
- [ ] Push all changes from your local repo to your fork on GitHub.
- [ ] Create a pull request draft, then request review from your technical and style reviewers [on your pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/requesting-a-pull-request-review) (you should also message them on company chat, as not everyone checks their GitHub notifications regularly). If you have already had people review it, mention that in the pull request description. You can have your reviewers look at your post directly in GitHub, which will convert the Markdown nicely and even parse the frontmatter into a little table! See [this example](https://github.com/EndPointCorp/end-point-blog/pull/2010/files?short_path=3462db9#diff-3462db9870de2a809556b39c9a155c5daf52e2f182c7f68ea5802a8c5035c6af)
- Incorporate changes based on your reviewers' input.
    - [ ] Complete technical review
    - [ ] Complete style review
- [ ] When you are done incorporating feedback and making any other changes, contact a keeper of the blog for final review and publishing. You can message on company chat or in a comment on your pull request (make sure to tag Seth @sethjensen1).

Once your blog post has been published to the world, proofread it again. You often see mistakes after publishing that you didn't notice before, and it's not too late to fix them!
