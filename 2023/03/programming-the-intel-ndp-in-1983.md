---
author: "Jeremy Freeman"
title: "Programming the Intel NDP in 1983"
date: 2023-03-12
tags:
- mathematics
- hardware
- programming
github_issue_number: 1941
featured:
  image_url: /blog/2023/03/programming-the-intel-ndp-in-1983/20230205-163937-sm.webp
---

![Photograph of brick building fronted by a metal staircase leading to the roof, gated by a full-size metal door that would be trivially easy to climb around](/blog/2023/03/programming-the-intel-ndp-in-1983/20230205-163937-sm.webp)

<!-- Photo by Jon Jensen -->

### The Beginning

I graduated from St. John’s College in Annapolis in 1980. It was an intensive four-year education in math, science, language, poetry, and philosophy. Two years later, I took four computer classes at a community college, and got my first IT job in 1983 at the beginning of the personal computer revolution.

There were two of us: Steve, the owner of the company, and I, working literally in his garage. I was just a fledgling, uncertain and doubtful of my own ability. The IBM PC had come out the summer before, a device IBM seemed to regard as little more than a toy. Steve was by profession a physicist.

Steve noticed the PC had an empty socket on the motherboard, next to the Intel 8088 CPU. He guessed it was for Intel’s 8087 Numeric Data Processor (NDP), also known as a math co-processor, that was designed as a companion to Intel’s 8088/86.

The CPU could operate perfectly well on its own, but if the NDP was installed, they would both read the same code stream. The CPU would ignore NDP instructions and let the NDP execute them. The NDP would ignore non-NDP instructions and let the CPU execute them. While the 8088/86 is running code, it can’t do anything else. With the NDP, true parallel processing is possible.

![Intel 8087 chip imprinted with part numbers and "© Intel '80 '81" alongside a U.S. 5¢ piece (nickel) for scale](/blog/2023/03/programming-the-intel-ndp-in-1983/8087_with_Nickel_003.webp)

### The Plan

IBM selected Microsoft to produce its systems software: operating system, compilers, linkers, libraries, macro assembler, etc. Microsoft not only ignored the 8087, it devised a floating-point format incompatible with it. Steve had signed a contract with Intel to be the exclusive distributor of the NDP for a period of years—Intel wasn’t selling any to speak of, so why not?

Steve’s business plan was to sell a package: an 8087 chip and modifications to IBM (Microsoft) systems software that builds programs (BASIC compiler, FORTRAN compiler, Pascal compiler, and Macro Assembler) so they can generate code for it, and libraries in which the math routines use the 8087 instead of complex, slow math routines in the CPU.

With the package we created, math-intensive applications would be sped up by anywhere from 2–3 times up to 40 times. The financial advantage to those who wrote their own applications in, say, BASIC, and used our package was compelling.

### The Platform

The computer I was given was a standard IBM PC of early 1983: an Intel 8088 microprocessor running at 4.77 MHz, two 360 KB 5¼-inch full-height floppy disks, 640 KB of RAM, a monochrome monitor, five expansion slots, and PC-DOS 1.1.

The 8088's 16-bit architecture internally was essentially the same as the 8086, with the difference that it used an 8-bit bus and was cheaper.

IBM designed an open architecture. In other words, it designed the PC to use all off-the-shelf equipment from other manufacturers, not IBM: chips from Intel, systems software from Microsoft, other chips from elsewhere. This was to be my saving grace, as we shall see below.

### Two Problems, Two Solutions, one Package

Our guiding design idea was that our users could develop programs in the way they were accustomed to. They could, for example, use the BASIC Interpreter that came as part of the PC ROM BIOS for an iterative, live mode of development. When satisfied, they could save the resulting text file, build it with our patched version of the BASIC compiler and link it with our libraries. They would have bought an 8087 from us, plugged it into the coprocessor slot, and then could launch their executable.

One customer, for example, was in Kansas. They were commodity traders who had an algorithm written in BASIC. It would take data from all commodity trades during the day and at the end of the day, run the data through their algorithm, and use the result to place trades first thing the next morning. It took 5–6 hours to run, and they got home to their families at 10 or 11 o'clock at night.

With our software modifications and the 8087, it took only about 2 hours to run, so they were home in time for dinner.

### Too Naive To Fail

When I first sat down at my PC to work, I didn't know how to turn it on.

To do my job I had to program in Intel 16-bit assembly language. I not only had never seen any assembly language, I had never seen any computer language before besides FORTRAN and PL/I.

I was somewhat like the bumblebee. Mathematics has proven that the bumblebee is aerodynamically unable to fly. The bee, however, does not know math, so it flies anyway.

I sat at my desk and grappled with the complexity before me. At the end of the first week, I felt so hopeless and lost that I thought I would speak to Steve and say, "Steve, when we interviewed I misled you. I pretended I am not an idiot. Let's say no more about it. I will slink away silently. You don't even have to pay me."

Then I thought, "Steve is a pretty smart man. I will leave it up to him. If he thinks I should leave, he can fire me. Meanwhile, I will stay here and give it everything I've got."

### My Tasks

The 8087 had a stack of eight ten-byte floating point registers. It could load and save either four-byte (single) or eight-byte (double) floating point. Steve had written a disassembler using the BASIC interpreter, so I had a printout of the code in the BASIC library. It did not show the source code, but it did show labels of routines and variables.

Steve had a list of the names of all the math routines in the library. I had to edit each math routine so that it would perform the same functionality as the original, but using the 8087.

A second requirement had to do with the floating-point format of constants in the source code. The Microsoft compilers generated them in MS-Binary floating point, in the structure *exponent + sign bit + mantissa* (or significand). The 8087 used IEEE floating-point, which was structured *sign bit + exponent + mantissa*. We patched the compilers so that at the place they would generate floating-point constants, they would generate IEEE-format constants instead.

### My Advantages

IBM shipped each PC with two ring binders. One explained the BASIC language as implemented in the ROM BIOS. The other was a handbook for the PC, which told everything a person could possibly want to know about the machine, including a printout of the ROM BIOS assembly language source code at the end of the manual: page after page of working code in Intel 8088/86 assembly language.

I also had an Intel product manual on the 8088/86, including a section on the 8087. That was some of the most dense specifications on the planet, but it contained all the operations and registers, both for the CPU and the NDP.

Another advantage I had was the debugger, `DEBUG.COM`. I would edit a math routine to replace the operations in the CPU with a few simple opcodes for the NDP, since it did all its operations internally, allowing the programmer to use a few NDP instructions to carry out the functionality. I would then use the librarian to replace the given routine in the library with my routine, write a test program in BASIC and build it. Then I would load the executable in the debugger and step through the code. That had two big advantages: One, I got to see the assembly language in action, learning more than a book could ever teach me. Two, I verified that the code actually did what I thought it did. The code we shipped rarely had a bug in it and those were usually minor. Except one.

### Whoops!

There was one major bug: error handling. I became aware of it when a customer called in about the failure of our code to catch a division by zero. Some research showed that the first 1024 bytes of RAM contained the Interrupt Vector Table (IVT), 256 four-byte entries containing the segment (two bytes) and offset (two bytes) of the Interrupt Service Routine (ISR). Interrupt INT 0 contained the address of the CPU divide by zero ISR.

Our software, since it did not use the CPU for division, did not catch a division by zero. This error would generate an IRQ (interrupt request) 13 which Intel had reserved for the math coprocessor. In Intel's product spec, they marked IRQ 13 as Reserved. The IBM engineers, however, had always seen the word "Reserved" used for things reserved by IBM, so they used IRQ 13 for something else. So I had to write an ISR that would take over the IRQ 13 entry in the IVT, check to see if there was an error in the NDP, and if so, handle it. Otherwise, pass control onto the original ISR.

Eventually there was a DOS routine to create a chain of ISRs, each of which would determine if the interrupt was something it should handle or else pass it on to the next ISR in the chain. Good cyber-citizens would play nice, and use the DOS routine to get their place in the chain.

### They Think They Didn't Get the Right Test

The company expanded, leaving the garage far behind and moving into a brick-and-mortar building, one of many at a defunct rope-factory. It employed by this time 40–50 people.

Intel had marched forward, producing the 80286 (with its companion 80287) and the 80386 (with its companion 80387).

Steve asked me to write a test for the math chips. I wrote it in C and Intel 16-bit Assembler. The test performed the four standard arithmetic operations—add, subtract, multiply, divide—and also special operations the NDP was capable of, like exponents, logarithms, square roots, trigonometric functions, etc.

The code tested whether the answers calculated by the chip came out within a narrow range, since it is not possible to test for an exact result with floating-point numbers that can be "right" but differ in the least significant bits of the mantissa. I named it 87TEST.EXE. It shipped with every NDP we sold: 8087, 80287, 80387.

We began getting calls from customers who had bought an 80287 or 80387, complaining that they had received the wrong test. Someone would have to explain that the same executable with the same code tested all variants of the NDP. These calls were costing the company money to reassure the customers, so I wrote a new version of the test which determined which CPU and which NDP it was running on.

The OS was MS-DOS, a character-based system. I used the advanced ROM-BIOS character set to "draw" images representing both chips, each casting a "shadow" to seem three-dimensional, and each labeled with the number of the chip. For example, one "image" could be labeled 80286 and the other 80287.

In order to gain customer confidence these had to be accurate. Later models of these chips had instructions whereby you could ask the chip, "What are you?" and it would return its version number. Earlier variants did not have these instructions, but for the most part I found characteristics I could test for to determine the version.

With the 8088 and 8086, however, they both used exactly the same instruction set. I racked my brain to find a difference and could not. I turned to my dog-eared copy of the 8088/86 Intel product manual and pored through it. Finally, I found a difference: the 8088 had a four-byte prefetch queue and the 8086 had a six-byte one.

I solved the problem by writing self-modifying code, which was a huge no-no according to Intel. It used 6 bytes in the code segment, with a constant defined in the 6th byte. I cleared the prefetch queue by doing a jump to the lead instruction. Thus, the prefetch queue would contain four bytes and the sixth byte would still be in memory (8088) or all six bytes would be in the pre-fetch queue (8086). The first instruction moved a different constant into the 6th byte. In an 8088, the 6th byte in memory would be changed and in the 8086 the 6th byte would be modified in the prefetch queue and remain untouched in memory. Then I would test that 6th byte: changed = 8088 and unchanged = 8086.

At last my search to correctly identify the CPU and its companion NDP was over. The test program was complete.

### Summary

I had to make do with the Intel product manual, the IBM PC manual, the IBM debugger, and tools my own company had created. Google did not exist, and for that matter, the Internet as we know it today did not exist. There was no plethora of instructional videos, as are widely available today.

Success required above all persistence and resourcefulness. I do not deny that native ability and education are important, but problem-solving in the IT world succeeds when we accept a challenge and strive to achieve what we never thought possible.

We adapt, we improvise, we overcome. Failure is not an option!

### References

* [IBM PC](https://en.wikipedia.org/wiki/IBM_Personal_Computer)
* [PC Hardware](http://philipstorr.id.au/pcbook/book2/irq.htm)
