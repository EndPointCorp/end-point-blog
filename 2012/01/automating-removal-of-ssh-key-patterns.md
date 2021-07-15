---
author: Brian Buchalter
title: Automating removal of SSH key patterns
github_issue_number: 536
tags:
- hosting
- tools
date: 2012-01-03
---

Every now and again, it becomes necessary to remove a user’s SSH key from a system. At End Point, we’ll often allow multiple developers into multiple user accounts, so cleaning up these keys can be cumbersome. I decided to write a shell script to brush up on those skills, make sure I completed my task comprehensively, and automate future work.

### Initial Design and Dependencies

My plan for this script is to accept a single argument which would be used to search the system’s authorized_keys files. If the pattern was found, it would offer you the opportunity to delete the line of the file on which the pattern was found.

I’ve always found mlocate to be very helpful; it makes finding files extremely fast and its usage is trivial. For this script, we’ll use the output from locate to find all authorized_keys files in the system. Of course, we’ll want to make sure that the mlocate.db has recently been updated. So let’s show the user when the database was last updated and offer them a chance to update it.

```bash
mlocate_path="/var/lib/mlocate/mlocate.db"
if [ -r $mlocate_path ]
then
    echo -n "mlocate database last updated: "
    stat -c %y $mlocate_path
    echo -n "Do you want to update the locate database this script depends on? [y/n]: "
    read update_locate
    if [ "$update_locate" = "y" ]
    then
        echo "Updating locate database.  This may take a few minutes..."
        updatedb
        echo "Update complete."
    fi
else
    echo "Cannot read the mlocate db path: $mlocate_path"
    exit 2
fi
```

First we define the path where we can find the mlocate database. Then we check to see if we can read that file. If we can’t read the file, we let the user know and exit. If we can read the file, print the date and time it was last modified and offer the user a chance to update the database. While this is functional, it’s pretty brittle. Let’s make things a bit more flexible by letting locate tell us where its database is.

```bash
if
    mlocate_path=`locate -S`
then
    # locate -S command will output database path in following format:
    # Database /full/path/to/db: (more output)...
    mlocate_path=${mlocate_path%:*} #remove content after colon
    mlocate_path=${mlocate_path#'Database '*} #remove 'Database '
else
    echo "Couldn't run locate command.  Is mlocate installed?"
    exit 5
fi
```

Instead of hard-coding the path to the database, we collect the locate database details using the -S parameter. By using some [string manipulation functions](http://tldp.org/LDP/abs/html/string-manipulation.html) we can tease out the file path from the output.

Because we are going to offer to update the location database (as well as eventually manipulate authorized_keys files), it makes sense to check that we are root before proceeding. Additionally, let’s check to see that we get a pattern from our user, and provide some usage guidance.

```bash
if [ ! `whoami` = "root" ]
then
    echo "Please run as root."
    exit 4
fi

if [ -z $1 ]
then
    echo "Usage: check_authorized_keys PATTERN"
    exit 3
fi
```

### Checking and modifying authorized_keys for a pattern

With some prerequisites in place, we’re finally ready to scan the system’s authorized_keys files. Let’s just start with the syntax for that loop.

```bash
for key_file in `locate authorized_keys`; do
    echo "Searching $key_file..."
done
```

We do not specify a dollar sign ($) in front of key_file when defining the loop, but once inside our loop we use the regular syntax. We use [command substitution](http://pubs.opengroup.org/onlinepubs/009695399/utilities/xcu_chap02.html#tag_02_06_03) by placing a command around back quotes (`) around the output of the command we want to use. We’re now scanning each file, but how do we find matching entries?

```bash
IFS=$'\n'
for matching_entry in `grep "$1" $key_file`; do
    IFS=' '
    echo "Found an entry in $key_file:"
    echo $matching_entry
done
```

For each $key_file, we now grep our user’s pattern ($1) and store it in $matching_entry. We have to change the [Input Field Seperator (IFS)](http://pubs.opengroup.org/onlinepubs/009695399/utilities/xcu_chap02.html#tag_02_05_03) to a new line, instead of the default space, in order to capture each grepped line in its entriety. (Thanks to Brian Miller for that one!)

With a matching entry found in a key file, it’s time to finally offer the user a chance to remove the entry.

```bash
echo "Found an entry in $key_file:"
echo $matching_entry
echo -n "Remove entry? [y/n]: "
read remove_entry
if [ "$remove_entry" = "y" ]
then
    if [ ! -w $key_file ]
    then
        echo "Cannot write to $key_file."
        exit 1
    else
        sed -i "/$matching_entry/d" $key_file
        echo "Deleted."
    fi
else
    echo "Not deleted."
fi
```

We prompt the user if they want to delete the shown entry, verify we can write to the $key_file, and then delete the $matching entry. By using the -i option to the sed command, we are able to make modifications in place.

### The Final Product

I’m sure there is a lot of room for improvement on this script and I’d welcome pull requests on the [GitHub repo](https://github.com/bbuchalter/clean_authorized_keys/blob/master/clean_authorized_keys) I setup for this little block of code. As always, be **very** careful when running automated scripts as root. Please test this script out on a non-production system before use.

```bash
#!/bin/bash

if [ ! `whoami` = "root" ]
then
    echo "Please run as root."
    exit 4
fi

if [ -z $1 ]
then
    echo "Usage: check_authorized_keys PATTERN"
    exit 3
fi

if
    mlocate_path=`locate -S`
then
    # locate -S command will output database path in following format:
    # Database /full/path/to/db: (more output)...
    mlocate_path=${mlocate_path%:*} #remove content after colon
    mlocate_path=${mlocate_path#'Database '*} #remove 'Database '
else
    echo "Couldn't run locate command.  Is mlocate installed?"
    exit 5
fi

if [ -r $mlocate_path ]
then
    echo -n "mlocate database last updated: "
    stat -c %y $mlocate_path
    echo -n "Do you want to update the locate database this script depends on? [y/n]: "
    read update_locate
    if [ "$update_locate" = "y" ]
    then
        echo "Updating locate database.  This may take a few minutes..."
        updatedb
        echo "Update complete."
        echo ""
    fi
else
    echo "Cannot read from $mlocate_path"
    exit 2
fi

for key_file in `locate authorized_keys`; do
    echo "Searching $key_file..."
    IFS=$'\n'
    for matching_entry in `grep "$1" $key_file`; do
    IFS=' '
        echo "Found an entry in $key_file:"
        echo $matching_entry
        echo -n "Remove entry? [y/n]: "
        read remove_entry
        if [ "$remove_entry" = "y" ]
        then
            if [ ! -w $key_file ]
            then
                echo "Cannot write to $key_file."
                exit 1
            else
                sed -i "/$matching_entry/d" $key_file
                echo "Deleted."
            fi
        else
            echo "Not deleted."
        fi
    done
done

echo "Search complete."
```
