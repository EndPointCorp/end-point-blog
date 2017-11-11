---
author: Selvakumar Arumugam
gh_issue_number: 977
tags: ruby, rails, testing
title: Convert Line Endings of Mac and Windows to Unix in Rails and Test with RSpec
---

Line endings or newline is a special character(s) to define the end of a line. The line endings special character(s) vary across the operating systems. Let's take an example, we are developing a Rails feedback application which will be used by a wide range of users. The users might submit the feedback from different operating systems which has different kind of line end character(s). The content should have formatted for standard line endings before storing into backend.

Mostly two special characters used to define the line endings in most of the operating systems.

1. Line Feed (LF) - \n

2. Carriage Return (CR) - \r

The usage of these two special characters for Unix, Mac and Windows are

<table border="1" style="border-collapse: collapse; border: 1px solid white;"><tbody>
<tr> <td style="padding: 5px;">OS</td> <td style="padding: 5px;">Characters</td> <td style="padding: 5px;">Name</td> </tr>
<tr> <td style="padding: 5px;">Unix</td> <td style="padding: 5px;">\n</td> <td style="padding: 5px;">LF</td> </tr>
<tr> <td style="padding: 5px;">Mac</td> <td style="padding: 5px;">\r</td> <td style="padding: 5px;">CR</td> </tr>
<tr> <td style="padding: 5px;">Windows</td> <td style="padding: 5px;">\r\n</td> <td style="padding: 5px;">CRLF</td> </tr>
</tbody></table>

Note:- \r is the newline character up to Mac OS version 9, after that Mac uses Unix line endings.

It is a developer's job to convert all kinds of line endings to Unix line ending format to maintain the standard. We can achieve this by a regex pattern replace. The regex pattern should convert \r(Mac) or \r\n(Windows) to \n(Unix).

```ruby
standard_content = non_standard_content.gsub(/\r\n?/,"\n")
```
We can see the conversion of line endings to Unix from Mac and Windows using irb (Interactive Ruby) shell.

***1. Mac***

```ruby
irb(main):001:0&gt; mac ="Hello \r Mac"
=&gt; "Hello \r Mac"
irb(main):002:0&gt; mac.gsub(/\r\n?/,"\n")
=&gt; "Hello \n Mac"
```
***2. Windows***

```ruby
irb(main):001:0&gt; windows="Hello \r\n Windows"
=&gt; "Hello \r\n Windows"
irb(main):002:0&gt; windows.gsub(/\r\n?/,"\n")
=&gt; "Hello \n Windows"
```

**RSpec Tests**

After the implementation of line endings conversion, it should covered with test cases for the best practices of development. Here is the bunch of Rspec code to test both Mac and Windows line endings conversion.

```ruby
  describe "POST feedback requests" do
    it "validates Mac line endings converted to Unix" do     
      _params = { :content =&gt; "Hello \r Mac", :user =&gt; "myuser"}
      post '/feedback.json', _params
      response.status.should == 200
      result = JSON.parse(response.body)
      result['content'].should_not include("\r")
    end

    it "validates Windows line endings converted to Unix" do
      _params = { :content =&gt; "Hello \r\n Windows", :user =&gt; "myuser"}
      post '/feedback.json', _params
      response.status.should == 200
      result = JSON.parse(response.body)
      result['content'].should_not include("\r\n") 
    end
  end
```
The line endings conversion plays a crucial role in standardising the content. It is recommended to convert line endings to Unix style when providing web service features. 


