---
author: Mark Johnson
gh_issue_number: 515
tags: interchange, jobs, testing
title: Global Variables in Interchange Jobs
---



Those familiar with writing global code in Interchange are certainly familiar with the number of duplicate references of certain global variables in different namespaces. For example, the Values reference is found in both the main namespace ($::Values) as well as in Vend::Interpolate ($Values usually from within usertags). One can also access the Values reference through the Session reference, which itself can be found in main ($::Session), Vend ($Vend::Session), and Vend::Interpolate ($Session usually from within usertags) namespaces with, e.g., $::Session->{values}. Most times, as long as context allows, any of those access points are interchangeable, and there's a good mix you see from developers using all of them.

In recent work for a client, I had developed an actionmap that incorporated access to the session for some of its coding--certainly not an uncommon occurrence. When I work in global space, I tend to use the main namespace references since they are available in all contexts within Interchange (or so I thought). The actionmap was constructed, tested, and put into production, where it worked as expected.

After a short period of operation, the client came to us and noted that in their actual operating procedure, the actionmap must process many more data points than we had it operate on in testing, causing it to take much more time. Thus, for their usual workload, they found the process was timing out and Interchange housekeeping reaping the process.

After a brief discussion, we decided the expedient course of action was to convert the work from a browser-initiated actionmap into an Interchange job. The code was easily exposed as a usertag as well, so in very short order we had the same functionality available as a job, where the job was now triggered by the browser access previously running the actionmap.

The change resolved the immediate problem, so now all work was completing, but the client brought a new issue to our attention. The reporting from the job was not as it was supposed to be. None of the code had been modified in the changeover, and the code when run as an actionmap produced the proper reporting.

The problem tracked down eventually to that session access. When the code was run in the context of the job, the Session reference was not copied into the main (or, as it turns out, Vend::Interpolate) namespace. Without the assumed session values in place, it was causing the report to produce invalid output.

To demonstrate, I constructed a simple usertag to dump the reference addresses of the 5 mentioned global variables:

```perl
UserTag  ic-globals  Routine &lt;&lt;EOR
sub {
    return &lt;&lt;EOP;
.     \$Session: $Session
\$Vend::Session: $Vend::Session
    \$::Session: $::Session

       \$Values: $Values
     \$::Values: $::Values
EOP
}
EOR
```

I then created both a test page and an IC job that only called [ic-globals]. Running them both demonstrates the problem quite clearly.

From test page:

```nohighlight
      $Session: HASH(0xb0e1898)
$Vend::Session: HASH(0xb0e1898)
    $::Session: HASH(0xb0e1898)

       $Values: HASH(0xb0e1dd8)
     $::Values: HASH(0xb0e1dd8)
```

Output from job:

```nohighlight
      $Session:
$Vend::Session: HASH(0xb221fa0)
    $::Session:

       $Values: HASH(0x926ddd8)
     $::Values: HASH(0x926ddd8)
```

Interchange jobs provide yet a new context where you must consider your global variable usage. In particular, if you find code executed in the context of a job produces inconsistencies with the same code in other contexts, review your global variable usage and confirm those variables are what you assume they are.


