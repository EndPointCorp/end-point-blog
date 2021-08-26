---
author: Mike Farmer
title: Testing Anti-Patterns
github_issue_number: 782
tags:
- conference
- ruby
date: 2013-04-04
---

Testing is always a popular subject at MountainWest RubyConf. Now that many developers are embracing test driven development, there is a big need for guidence. [Aja Hammerly](http://www.thagomizer.com/blog/2013/04/04/a-testing-anti-pattern-safari.html) is talking about testing anti-patterns. Tests should be trustworthy. You should be able to depend on them. If they fail, your system is broken. If they pass your system works. Tests should be simple. Simple to read, simple to write, simple to run.

Here are some anti-patterns that Aja addressed:

### Pointless Tests

- No tests! Solution: Write tests.
- Not Running Tests. Solution: Use Continuous Integration so you have to run your tests.
- Listen to your failing tests. Fix team culture that ignores a red CI.
- That test that fails sometimes. Fix it!

### Wasted Time / Effort

- Testing Other Peoples Code (OPC). Solution: Test only what you provide and use third-party code that has good coverage.
- assert_nothing_raised or in other words, don’t assert that a block runs without an exception only. If an error is raised, it will just raise an exception, which is a failure.

### False Positives and Negatives

- Time sensitive tests. For example, using Time.now. Solution: stub Time.now().
- Hard-coded dates in tests. Use relative dates instead.
- Order dependent tests. Make sure your tests clean up after themselves. Randomizing your tests helps detect these problems.
- Tests that can’t fail. This can happen when we heavily stub or mock. You can also detect these errors by ensuring you always see your tests go red, then green.

### Inefficient Tests

- Requiring External Resources such as networking requests or other IO not checked into your source control. Solution: Mock/stub external resources. You can use WebMock for this, but it’s better to write your own Stub.
- Complicated Setup: Solution is to refactor your implementation. See Working Effectively with Legacy Code by Michael Feathers.

### Messy Tests:

- Repeated code
- Copy paste tweak
- disorganized tests
- literals everywhere

Solution:

- DRY your tests
- Group by method under test
- Use descriptive names
- Put literals in variables

Many of the reasons we don’t have adequate tests in our apps is because they are slow. Applying the solutions for these anti-patterns can solve the majority of these issues.
