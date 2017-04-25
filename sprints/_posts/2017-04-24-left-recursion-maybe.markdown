---
layout: post
title:  "Sprint: Left Recursion! Maybe?"
date:   2017-04-24 10:00:00 -0500
permalink: /:categories/:title.html
---

## Bounded Recursion and Left Recursion

Recursion is a problem in a lot of situations when you want strong guarantees about correctness or consistency.
That whole problem about making sure programs halt actually ends up implying the incompleteness theorem of Gödel.
I'm not going to go on an exposition of those connections exactly partly because of time and partly because I'm not really qualified.
Suffice to say, recursion and in particular infinite recursion, is a problem.
The idea of bounded recursion is basically a greedy solution to infinite recursion.
Imagine for a moment that instead of allowing recursion to happen infinitely you allow it to happen only for a preset amount of times.
This could be thought of as a bounded recursion.
The question then becomes how many recurses do you need to determine if the recursion is going to be infinite or if you've processed the input sufficiently?
For instance the recursion might be periodic but there is a clear condition to stopping.
It shouldn't be too hard to see that _in general_ this is just the halting problem rephrased (that is, finding an appropriate bound).

Luckily for us, left recursion is not the general case and it is in fact a periodic recursion.
As you consume more of the finite input you will either consume more of the input or repeat one of the previous recursive uses for a given bound.
That means you can greedily increase the bound on the recursion until you reach an instance where you stop consuming more of the input.
This is not my argument it is one by Sérgio Medeiros (at least I assume it is his novel contribution but I have seen a similar idea in rewriting systems as well so it was familiar).
In his paper he describes this idea and supplies proof.
It is a general approach that should be implementation agnostic.
However, the machine transitions he gave in his paper for a parsing virtual machine are I believe incorrect.

Firstly, when Medeiros' implementation finds the bound that reduces the consumed input it backtracks the machine in such a way that you end up repeating the bounded recursion one too far.
Meaning you should have used the _previous_ bound because the machine still has instructions to consume that input (based on the instruction the implementation backtracks to).
There are two ways to fix this, either by having a "Fence" instruction for the left recursion that you jump to instead (so that you don't have to redo those instructions), or by tracking the last two bounded recursions (instead of just the last one).
I took the later approach as it was non-obvious where the "Fence" instruction should go based off of nested calls and nested choices.

Secondly, the failure states for the transitions ignore that a bounded recursion could fail while a later one could succeed.
A failure state shouldn't stop the bounded recursion unless the machine failed to consume more input.
I attempted to fix this problem by copying the transitions from the "Return" instruction that Medeiros supplied for the failure state with an additional check on if the input is fully consumed.

I'm not entirely sure if these fixes are actually, well, _fixes_.
I haven't proved them but I have tested them.
They seem to work.
I'm not sure why the transitions in the publication were incorrect, it might be implementation details that differ between what Medeiros was intending and what I have done.
I'd have to ask him.
I might do so once I'm more confident that my implementation is correct.
All in all, mission complete.

## NEXT!

I finally managed to get left recursion working, at least I think.
I really need to build my confidence on the implementation more I think.
In particular different precedence levels haven't really been explored as much as I like.
With that in mind I think the next goal is clear.
**Get PVM ready for a 0.1 release and have a calculator example using left recursion and precedence ready**.
