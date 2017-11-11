---
author: Joshua Tolley
gh_issue_number: 303
tags: postgres
title: Using PostgreSQL Hooks
---

PostgreSQL is well known for its extensibility; users can build new functions, operators, data types, and procedural languages, among others, without having to modify the core PostgreSQL code. Less well known is PostgreSQL's extensive set of "hooks", available to the more persistent coder. These hooks allow users to interrupt and modify behavior in all kinds of places without having to rebuild PostgreSQL.

Few if any of these hooks appear in the documentation, mostly because the code documents them quite well, and anyone wanting to use them is assumed already to be sufficiently familiar with the code to find the information they'd need to use one. For those interested in getting started using hooks, though, an example can be useful. Fortunately, the contrib source provides one, in the form of [passwordcheck](http://www.postgresql.org/docs/9.0/static/passwordcheck.html), a simple contrib module that checks users' passwords for sufficient strength. These checks include having a length greater than 8 characters, being distinct from the username, and containing both alphabetic and non-alphabetic characters. It can also use [CrackLib](http://sourceforge.net/projects/cracklib/) for more intense password testing, if built against the CrackLib code.

In general, these hooks consist of global function pointers of a specific type, which are initially set to NULL. Whenever PostgreSQL wants actually to use a hook, it checks the function pointer, and if it's not NULL, calls the function it points to. When someone implements a hook, they write a function of the proper type and an initialization function to set the function pointer variable. They then package the functions in a library, and tell PostgreSQL to load the result, often using [shared_preload_libraries](http://www.postgresql.org/docs/9.0/static/runtime-config-resource.html#GUC-SHARED-PRELOAD-LIBRARIES).

For our example, the important pieces of the PostgreSQL code are in src/backend/commands/user.c and src/include/commands/user.h. First, we need a function pointer type, which in this case is called check_password_hook_type:

```cpp
typedef void (*check_password_hook_type)
   (const char *username, const char *password,
   int password_type, Datum validuntil_time,
   bool validuntil_null);

extern PGDLLIMPORT check_password_hook_type check_password_hook;
```

This says the check_password_hook will take arguments for user name, password, password type, and validity information (for passwords valid until certain dates). It also provides an extern declaration of the actual function pointer, called "check_password_hook".

The next important pieces of code are in src/backend/commands/user.c, as follows:

```cpp
/* Hook to check passwords in CreateRole() and AlterRole() */
check_password_hook_type check_password_hook = NULL;
```

...which defines the function hook variable, and this:

```cpp
if (check_password_hook &amp;&amp; password)
  (*check_password_hook) (stmt-&gt;role, password,
      isMD5(password) ? PASSWORD_TYPE_MD5 : PASSWORD_TYPE_PLAINTEXT,
    validUntil_datum,
    validUntil_null);
```

...which actually uses the hook. Actually the hook is used twice, with identical code, once in CreateRole() and once in AlterRole(), so as to provide password checking in both places. (Insert D.R.Y. rant here).

In order to take advantage of this hook, the passwordcheck module needs to implement the hook function, and set the check_password_hook variable to point to that function. First, passwordcheck.c needs to include a few things, including "commands/user.h" to ge the definitions of check_password_hook and check_password_hook_type, and call the PG_MODULE_MAGIC macro every PostgreSQL shared library needs. Then, it implements the password checking logic in a function called check_password():

```cpp
static void
check_password(const char *username,
      const char *password,
      int password_type,
      Datum validuntil_time,
      bool validuntil_null)
{
/* Actual password checking logic goes here */
}
```

Note that this declaration matches the arguments described in the check_password_hook_type, above.

Now to ensure the check_password_hook variable points to this new check_password() function. When loading a shared library, PostgreSQL looks for a function defined in that library called _PG_init(), and runs it if it exists. In passwordcheck, the _PG_init() function is as simple as this:

```cpp
void
_PG_init(void)
{
 /* activate password checks when the module is loaded */
 check_password_hook = check_password;
}
```

Other modules using hooks often check the hook variable for NULL **before** setting it, in case something else is already using the hook. For instance, the [auto_explain](http://www.postgresql.org/docs/9.0/static/auto-explain.html) contrib module does this in _PG_init() (note that auto_explain uses three different hooks):

```cpp
prev_ExecutorStart = ExecutorStart_hook;
 ExecutorStart_hook = explain_ExecutorStart;
 prev_ExecutorRun = ExecutorRun_hook;
 ExecutorRun_hook = explain_ExecutorRun;
 prev_ExecutorEnd = ExecutorEnd_hook;
 ExecutorEnd_hook = explain_ExecutorEnd;
```

auto_explain also resets the hook variables in its _PG_fini() function. Since unloading modules isn't yet supported and thus, _PG_fini() never gets called, this is perhaps unimportant, but is good for the sake of being thorough.

Back to passwordcheck. Having set the hook variable, all that remains is to get PostgreSQL to load this library. The easiest way to do that is to set shared_preload_libraries in postgresql.conf:

```nohighlight
josh@eddie:~/devel/pgsrc/pg-eggyknap/contrib/passwordcheck$ psql
psql (9.0devel)
Type "help" for help.

5432 josh@josh# show shared_preload_libraries ;
 shared_preload_libraries
--------------------------
 passwordcheck
(1 row)
```

Restarting PostgreSQL loads the library, proven as follows:

```nohighlight
5432 josh@josh# create user badpass with password 'bad';
ERROR:  password is too short
```

There are hooks like this all over the PostgreSQL code base. Simply search for "_hook_type", to find such possibilities as these:

<table><tbody><tr><td><b>Name</b></td><td><b>Description</b></td></tr>
<tr><td>shmem_startup_hook</td><td>Called when PostgreSQL initializes its shared memory segment</td></tr>
<tr><td>explain_get_index_name_hook</td><td>Called when explain finds indexes' names.</td></tr>
<tr><td>planner_hook</td><td>Runs when the planner begins, so plugins can monitor or even modify the planner's behavior</td></tr>
<tr><td>get_relation_info_hook</td><td>Allows modification of expansion of the information PostgreSQL gets from the catalogs for a particular relation, including adding fake indexes</td></tr>
</tbody></table>
