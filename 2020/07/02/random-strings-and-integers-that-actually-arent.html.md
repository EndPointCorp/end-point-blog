---
author: "Josh Williams"
title: "Random Strings and Integers That Actually Aren’t"
tags: postgres, python, tips
gh_issue_number: 1650
---

![Rowntree’s Randoms sweets](/blog/2020/07/02/random-strings-and-integers-that-actually-arent/banner.jpg)

[Image](https://www.flickr.com/photos/fsse-info/3579540830/) from Flickr user fsse8info

Recently the topic of generating random-looking coupon codes and other strings came up on internal chat. My go-to for something like that is always [this solution](https://wiki.postgresql.org/wiki/Pseudo_encrypt) based on Feistel networks, which I didn’t think was terribly obscure. But I was surprised when nobody else seemed to recognize it, so maybe it is. In any case here’s a little illustration of the thing in action.

Feistel networks are the mathematical basis of the ciphers behind DES and other encryption algorithms. I won’t go into details (because that would suggest I fully understand it, and there are bits where I’m hazy) but ultimately it’s a somewhat simple and very fast mechanism that’s fairly effective for our uses here.

For string generation we have two parts. For the first part we take an integer, say the sequentially generated id primary key field in the database, and run it through a function that turns it into some other random-looking integer. Our implementation of the function has an interesting property: If you take that random-looking integer and run it back through the same function, we get the original integer back out. In other words…

```
cipher(cipher(n)) == n
```

…for any integer value of n. That one-to-one mapping essentially guarantees that the random-looking output is actually unique across the integer space. In other words, we can be sure there will be no collisions once we get to the string-making part.

The original function is based off the code [on the PostgreSQL wiki](https://wiki.postgresql.org/wiki/Pseudo_encrypt) with just a few alterations for clarity, and should work for any modern (or archaic) version of Postgres.

```sql
CREATE OR REPLACE FUNCTION public.feistel_crypt(value integer)
  RETURNS integer
  LANGUAGE plpgsql
  IMMUTABLE STRICT
AS $function$
DECLARE
    key numeric;
    l1 int;
    l2 int;
    r1 int;
    r2 int;
    i int:=0;
BEGIN
    l1:= (VALUE >> 16) & 65535;
    r1:= VALUE & 65535;
    WHILE i < 3 LOOP
        -- key can be any function that returns numeric between 0 and 1
        key := (((1366 * r1 + 150889) % 714025) / 714025.0);
        l2 := r1;
        r2 := l1 # (key * 32767)::int;
        l1 := l2;
        r1 := r2;
        i := i + 1;
    END LOOP;
    RETURN ((r1 << 16) + l1);
END;
$function$;

```

Swap what’s assigned to that `key` variable around a bit, just so you get a different output than what I’m illustrating. No good, after all, if someone can take this example verbatim and generate your coupon codes. Also once you start using the generated numbers, one way or another, you probably don’t want to change that key function as that would introduce the possibility of collisions with existing values generated with the previous key.

Anyway, with that in place, you can start generating some random integers, and make sure they map back:

```
totesrandom=# SELECT feistel_crypt(1), feistel_crypt(2), feistel_crypt(3), feistel_crypt(4);
 feistel_crypt | feistel_crypt | feistel_crypt | feistel_crypt
---------------+---------------+---------------+---------------
     561465857 |     436885871 |     576481439 |     483424269
(1 row)

totesrandom=# SELECT feistel_crypt(561465857), feistel_crypt(436885871), feistel_crypt(576481439), feistel_crypt(483424269);
 feistel_crypt | feistel_crypt | feistel_crypt | feistel_crypt
---------------+---------------+---------------+---------------
             1 |             2 |             3 |             4
(1 row)
```

In fact we can run a verification across, say, 10 million integers:

```sql
totesrandom=# SELECT COUNT(*) FROM generate_series (1,10000000) WHERE feistel_crypt(feistel_crypt(generate_series)) != generate_series;
 count
-------
     0
(1 row)

Time: 185151.416 ms (03:05.151)
```

### The cool part: string generation

Once we have that new value, the second part is even easier. We take the new integer and map that to a string, essentially creating a base-N representation of the number.

```sql
CREATE OR REPLACE FUNCTION public.int_to_string(n int)
  RETURNS text
  LANGUAGE plpgsql
  IMMUTABLE STRICT
AS $function$
DECLARE
    alphabet text:='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    base int:=length(alphabet);
    output text:='';
BEGIN
    LOOP
        output := output || substr(alphabet, 1+(n%base)::int, 1);
        n := n / base;
        EXIT WHEN n=0;
    END LOOP;
    RETURN output;
END $function$;
```

Voilà, short random-looking strings you can use for coupon codes, email confirmation tokens, whatever you need:

```sql
totesrandom=# SELECT int_to_string(feistel_crypt(1)), int_to_string(feistel_crypt(2)), int_to_string(feistel_crypt(3)), int_to_string(feistel_crypt(4));
 int_to_string | int_to_string | int_to_string | int_to_string
---------------+---------------+---------------+---------------
 5409L         | t8hJD         | Tj1aN         | NTySG
(1 row)

Time: 0.473 ms
```

You can tune that character set as needed, of course. Maybe jumble it up a bit if you’re super paranoid about someone reverse engineering it. Your character set could be anything you wanted. A purely emoji set could be fun, or perhaps set it to an array of words to concatenate together instead of individual letters. Or if there’s a chance someone could be reading one of these out loud, over a phone call for instance, you might want to go with a single case:

```sql
totesrandom=# -- alphabet in above function instead set to 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
totesrandom=# SELECT int_to_string(feistel_crypt(1)), int_to_string(feistel_crypt(2)), int_to_string(feistel_crypt(3)), int_to_string(feistel_crypt(4));
 int_to_string | int_to_string | int_to_string | int_to_string
---------------+---------------+---------------+---------------
 33FKKJ        | XK9DIH        | L79HTJ        | 7TQ39H
(1 row)

Time: 0.681 ms
```

It’s also certainly possible to reverse this part, too, and read the string back into the original integer. But I’d instead recommend stashing the resulting string into a database field, and doing a look-up on that directly.

### Bonus

At some point I ended up porting this to Python. It’s still super simple, and works just the same. But maybe seeing it in another form will help you port it to whatever other language you might need it for.

```python
def simple_feistel(value):
    # A simple self-inverse Feistel cipher for ID obfuscation
    l1 = (value >> 16) & 65535
    r1 = value & 65535

    for i in range(3):
        key = (((1366 * r1 + 150889) % 714025) / 714025.0)
        l2 = r1
        r2 = l1 ^ int(key * 32767)
        l1 = l2
        r1 = r2
    return (r1 << 16) + l1

def stringify_integer(value):
    # Take an integer and encode it as a base(len(alphabet)) string

    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    base = len(alphabet)
    output = ''

    while value > 0:
        output += alphabet[value%base]
        value //= base

    return output
```
