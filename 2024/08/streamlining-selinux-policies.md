---
title: "Streamlining SELinux Policies: From Policy Modules to Modules and Silent SELinux Denials"
author: Bharathi Ponnusamy
date: 2024-08-26
github_issue_number: 2072
featured:
  image_url: /blog/2024/08/streamlining-selinux-policies/banner.webp
description: Learn the differences between SELinux policy modules and modules, how to convert them from one to the other, and about SELinux denials and troubleshooting them.
tags: 
- selinux
- sysadmin
- security
---

![Cars drive across a road bridge over light blue water. Above are several large hotels, and white clouds against a light blue sky.](/blog/2024/08/streamlining-selinux-policies/banner.webp)

<!-- photo by Bharathi Ponnusamy -->

### Introduction

SELinux (Security-Enhanced Linux) provides a robust security layer that enforces security policies to control system access. When dealing with SELinux, you often encounter the terms "policy_module" and "module". Understanding the difference between these and knowing how to convert between them is crucial for efficient system administration.

### What is a policy_module?

A policy_module in SELinux is a type of module used to define additional policies. These modules encapsulate specific security rules that can be loaded into the SELinux policy to grant or restrict permissions. Policy modules are particularly useful for adding or modifying policies without changing the base SELinux policy.

```plain
policy_module(my_policy, 1.0)

require {
    type my_app_t;
}

#============= my_app_t ==============
allow my_app_t my_log_t:file read;
```

### What is a module?

A module in SELinux is a compiled version of a policy module. The compilation process translates the high-level policy rules into a binary format that SELinux can enforce. Modules are loaded into the SELinux policy store to extend or modify the active policy.

```plain
module my_module 1.0;

require {
    type my_app_t;
    class file { read write };
}

#============= my_app_t ===============
allow my_app_t my_log_t:file { read write };
```

### Converting policy_module to module

In many scenarios, it's necessary to convert a policy_module to a module. This conversion ensures compatibility and avoids the need for additional utilities such as selinux-polgenui.

Here’s how you can do it:

Create a `.te` file. This file contains the policy rules.

```plain
policy_module(my_policy, 1.0)

require {
    type my_app_t;
}

#============= my_app_t ==============
allow my_app_t my_log_t:file read;
```

Compile the policy module. Use the `checkmodule` and `semodule_package` tools to compile the policy module into a module.

```plain
checkmodule -M -m -o my_policy.mod my_policy.te
semodule_package -o my_policy.pp -m my_policy.mod
```

Load the module. Use `semodule` to load the compiled module into SELinux (using `-i` for "install").

```plain
semodule -i my_policy.pp
```


### The silent blocks of SELinux

Sometimes, SELinux can quietly block your software, leading to silent failures. This can be particularly tricky because SELinux usually logs issues in `/var/log/audit/auditd.log` or `/var/log/messages`. However, if a permission or property has the dontaudit setting applied, it won't be logged, making it harder to troubleshoot.

In many cases, system administrators expect SELinux to be vocal about problems. When SELinux doesn't log an issue due to dontaudit, it can quietly block your software without any visible errors.

### Troubleshooting silent blocks

To diagnose whether SELinux is causing a problem, you can temporarily set SELinux to "permissive" mode:

```plain
setenforce 0
```

If your script works in permissive mode and stops when you switch back to enforcing mode (with `setenforce 1`), SELinux is likely the culprit.

The next step is to temporarily disable dontaudit settings by building all policy modules with the `-D`/`--disable_dontaudit` option.

```plain
semodule -DB
```

This command will allow you to collect all the failing rules related to your problem. You can then use these logs to create a custom SELinux module.

After you've finished creating your module, re-enable the dontaudit silencing feature by rebuilding policy modules:

```plain
semodule -B
```

This prevents your logs from becoming cluttered with too many messages.
