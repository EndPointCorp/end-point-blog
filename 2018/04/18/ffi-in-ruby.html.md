---
author: Kamil Ciemniewski
title: "Using FFI in Ruby"
tags: ruby, ffi, c
---

`Ruby` for many years has been proving to be an amazing language. It's one of the most popular for creating web applications but also DevOps / systems administration tools. 

It seems that languages are naturally finding their own "niches". For `Ruby` it's what I listed above, while `Python` seems to work well for Computer Vision and Machine Learning.

For performance reasons, some code should never be coded in either one. Topic boundaries are being crossed typically though. You might be working on the web app that does some high performance math in the background. To marry the two worlds, people were successful with creating compiled "extensions". These extensions are typically coded in `C`. Both languages along with their interpreters are able to use those using native-to-language constructs.

One good example of this is the great `numpy` package. It brings high performance linear algebra constructs that would be impossible to code in pure `Python` with the same performance.
In the `Ruby` land, a similar example is the `nokogiri` gem. It allows very fast `XML` / `HTML` processing thanks to the core of its functionality being coded in `C`.

You might also be working on a `Ruby` app having a need for a functionality that has already been written as a library with `C` interface available. One way to use it would be to create an extension that would operate on those external `C` functions. This involves quite a number of prep-work though. The [RubyGems guides](http://guides.rubygems.org/gems-with-extensions/) describe the process in detail.

There is one more option and I'm about to show you what it is.

## Referencing external functions directly

`FFI` stands for "Foreign Function Interface". Most languages have a way to operate with external code (written in another language). The interface for doing so is what's called `FFI`. Examples:

* Docs on `FFI` in `Rust`: [https://doc.rust-lang.org/book/ffi.html](https://doc.rust-lang.org/book/ffi.html)
* Docs on `FFI` in `Python` via the `cffi` package: [https://cffi.readthedocs.io/en/latest/](https://cffi.readthedocs.io/en/latest/)
* Docs on `FFI` in `Haskell`: [https://wiki.haskell.org/FFI_Introduction](https://wiki.haskell.org/FFI_Introduction)

In this article, we're interested in using `FFI` in `Ruby`: [https://github.com/ffi/ffi/wiki](https://github.com/ffi/ffi/wiki)

No matter what the host language, the usage pattern is always the same:

* Define what external library you want to link with
* Define functions you want to make use of and how their arguments and return values map to your host language data types
* (Optionally) Define the calling convention
* Use those functions as if they were "native" to your host language

Let's see how it looks like in `Ruby`. The first step is to define a module you want to "attach" external functions to. This very often looks similar to the following:

```ruby
module SomeLibrary
  extend FFI::Library
  # (...)
end
```

The `FFI::Library` module brings in useful methods for defining  the linkage with the target, external library. We still need to "tell" `Ruby` the external library we want to work with. Here's an example of working with `fribidi`, which contains lots of very useful functions for working with the bidirectional Unicode text:

```ruby
module Bidi
  extend FFI::Library
  ffi_lib ['libfribidi']
  # (...)
end
```

Let's say that we want to use a very helpful `fribidi_log2vis` function. We'll want it to give us a logical position index for each visual position index of the text, given a directionality of it.

Disclaimer:
If the language you speak uses latin based script in writing, you might be scratching your head now. For most languages the logical positions of characters are the same as the "visual" ones (where those characters end up visually in the word / token). This is not always the case. Counterexamples include Arabic, Hebrew and Syriac (among others). A line of text could also contain words / tokens written using different scripts (like e. g. names of places written in the Latin script, inside a RTL paragraph). Sometimes also e. g. the punctuation might appear in one place logically in the string, while visually somewhere else.

The signature of the function reads as follows:

```C
fribidi_boolean fribidi_log2vis(
    /* input */
    FriBidiChar     *str,
    FriBidiStrIndex len,
    FriBidiCharType *pbase_dir,
    /* output */
    FriBidiChar     *visual_str,
    FriBidiStrIndex *position_L_to_V_list,
    FriBidiStrIndex *position_V_to_L_list,
    FriBidiLevel    *embedding_level_list
)
```

In order to use this function from `Ruby`, we need to tell it what those types mean in terms of types available in `Ruby` and the `ffi` gem:

```ruby
module Bidi
  extend FFI::Library
  ffi_lib ['libfribidi']
  
  attach_function :fribidi_log2vis, [ :pointer, :int32, :pointer, :pointer, :pointer, :pointer, :pointer ], :bool
end
```

The full documentation on the types mappings can be found here: [https://github.com/ffi/ffi/wiki/Types](https://github.com/ffi/ffi/wiki/Types)

We're now ready to wrap our newly attached external function around a convenient `Ruby` code. We'll create a `to_visual_indices` method on the `Bidi` module that will take a string and a symbol representing the directionality. The directionality will expect `:rtl` for the RTL direction. Here's the listing of how it looks like:

```ruby
module Bidi
  extend FFI::Library
  ffi_lib ['libfribidi']
  
  attach_function :fribidi_log2vis, [ :pointer, :int32, :pointer, :pointer, :pointer, :pointer, :pointer ], :bool
  
  def self.to_visual_indices(text, direction)
    null = FFI::Pointer::NULL

    t = FFI::MemoryPointer.new(:uint32, text.codepoints.count)
    t.put_array_of_uint32(0, text.codepoints)

    pos = FFI::MemoryPointer.new(:int, text.codepoints.count)

    dir_spec = FFI::MemoryPointer.new(:long)
    dir_spec.write_long( direction == :rtl ? 273 : 272)

    success = Lib.fribidi_log2vis(t, text.codepoints.count, dir_spec, null, null, pos, null)

    if success
      return pos.read_array_of_int(text.codepoints.count)
    else
      raise StandardError, "Failed to infer the visual ordering of the text"
    end
  end
end
```

You could now use your new module along with the new method that uses an external library:

```ruby
>> Bidi.to_visual_indices "Friendship الصداقة", :rtl
=> [17, 16, 15, 14, 13, 12, 11, 10, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

Using `FFI` in `Ruby` is a great way to bring in existing external functionality without the need to write an extension in `C`. It also spares you from the need to compile it, which in the case of `Rails` is very, very convenient.
