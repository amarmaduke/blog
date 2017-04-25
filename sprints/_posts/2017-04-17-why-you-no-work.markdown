---
layout: post
title:  "Sprint: But the Transitions are Right Here!"
date:   2017-04-17 10:00:00 -0500
permalink: /:categories/:title.html
---

## Sometimes Four Lines is Complicated

I wasn't able to get left-recursion working by the sprint end unfortunately.
Not for lack of trying.
I honestly don't quite know what's wrong.
The implementation is based off of something called "Bounded Left-Recursion".
As you might be able to imagine, you allow limited number of left recurses until some condition.
The particular observation is that the length of the matched input should grow until a critical number of recurses.
At this critical number the length matched should either decrease or be equal.
That's when you stop the infinite recursion.

There is a paper that describes all this in detail by Sérgio Medeiros.
To be fair I skimmed the parts I thought didn't matter and got right into the grit of the virtual machine implementation.
Translating the transitions from machine state to machine state into my code was easy.
The problem is that it didn't bloody work.
I think the problem might have to do with a difference in how the paper describes a match of input and how I'm doing it.
The paper talks about the entire suffix or prefix of an input.
Theoretically you should be able to do this with just a pointer that splits the input but at this point I'm willing to question anything.

Another issue is that different positions of the stack frame that encodes the memo table might have different semantic meaning.
Two entries which at a glance mean a point in the input might actually be the prefix _and then_ the suffix.
I don't know.
The resolution is to understand the paper in depth, front to back.
I was hoping to avoid that because, well, it's a time consuming thing to really understand the quirks of whatever notation the author decided to use.
I was also hoping that LPEG, the implementation by the author, had this left-recursion implemented but I couldn't find a hint of it in the source.
Moreover the paper suggests they have an experimental implementation of it, so I wonder if they just never incorporated it into the actual code.
It's also possible I just didn't spend enough time looking for it.

## But I want it!

Although it has been a bit of a struggle the way forward seems clear.
I need to understand the paper in depth so that I can reproduce the algorithm on my own instead of letting the transition equations babysit me.
There _is_ an implementation of bounded left-recursion that works in IronMeta, it's just not a virtual machine.
All the same, it's possible, even if the paper happens to have errors in the transition equations for the machine states (which I honestly doubt).
The code effort really isn't much at all, so I'll just double down on the same goal: **get left-recursion working.**
