---
layout: post
title:  "Sprint: Bad Estimates and Procrastination"
date:   2017-04-03 10:00:00 -0500
permalink: /:categories/:title.html
---

## Estimation, is it Hard?

The jig is up!
I failed to hit a goal that I set for a sprint.
I should just quit now, clearly I'm a failure and there is no point in continuing.
Or, we could talk openly and honestly about what happened and press on.
Let's do that.

The bigger problem (I think) that happened this sprint is that I misjudged the scope of my goal.
I thought that I basically needed to define a new interface for functionality that was already there and maybe implement some simple helper infrastructure.
What _really_ needed to be done was implementing a parser for the grammar language.
Strictly speaking to make the goal I set technically "achieved" all I needed was four lines of code change to add an additional 32 bits of information on the parsing machines output (assuming no parser was needed).
The virtual machine (VM) outputs a vector of 32-bit (okay technically the bit size of the integers is whatever the default register size is) integer triples.
The first integer tells you what rule this range matched, the next two integers define the range.
Originally there were only two integers making it hard to map your rules to an abstract syntax tree (AST).
Four lines of change later and we have the additional third integer.

You don't really strictly need an interface to help you turn that output into an AST, the library is still usable without that convenience.
You know what makes it not usable?
Not being able to build a machine from your grammar at all.
That's where needing a parser comes into play.
The parser fell behind because half of me wanted to bootstrap the process too early (when the project was originally started).
What I mean by that is I wanted the VM to parse the grammar specifications itself and produce the needed AST to then be compiled for your specific grammar.
That turns out to not really be practical, it's simpler to just write the parser and not worry about this self-referential stuff so early on.
So I started to do that, but writing a parser wasn't something I really incorporated into the estimate of time commitment.

## Things get Worse with Procrastination

Unfortunately, I also procrastinated.
To be honest, getting work done on the sprint Tuesday and Thursday is hard to do.
Not because of procrastination or laziness, but because of prior commitments.
Friday is also nigh impossible because of coaching commitments.
That leaves Monday (the day I write this blog, which to be fair only eats up about thirty minutes to an hour), Wednesday and the weekend.
This past Saturday I attended a programming contest which didn't go terribly well.
Contests are pretty draining events for me, with four hours of total driving and stressing out over my teams performance (me being the coach, not the participant).
I don't really blame myself for comatosing on Saturday.

However, here is the rub.
This past Friday was _open_.
I could have had at least two hours of quality time to work and I wasted it.
I did a very minor amount of work on Saturday during the contest, but on Sunday I only really spent a couple of hours working on the parser.
It could have been a much more fruitful day than that.
Personally, I don't count social gatherings as being lazy or procrastinating, you should take things in balance.
There wasn't any of that going on this past sprint though.
So, the upshot is that, yeah, I procrastinated.
I should stop doing that.

## Moving Forward

Working on my parser library was fun, even though I procrastinated.
Because of that, I want to double down on it.
The goal is still the same, the library should be developed to be in a _usable_ state.
Let's make the goal explicit: **The library should be able to parse its own grammar specification and produce its own AST**.
By library here, I mean the VMs themselves not hand rolled code, but there will be a hand rolled parser to get the ball rolling.

You might be asking, "isn't this still too much for a week sprint?"
My answer to that is no, my weekend is more open, and I'm more aware of what will be needed in terms of time (so procrastinating will be less justifiable to me).
Even if I fail (again), it's important to keep trying.
