---
layout: post
title:  "Sprint: Parsing Virtual Machines and One Line Changes"
date:   2017-03-27 10:00:00 -0500
permalink: /:categories/:title.html
---


## Sprint Retrospective

Last Monday I committed to fixing a bug in my [Anki plugin](https://github.com/amarmaduke/ankideckffs).
The problem boiled down to a single line in the importer where I rename model fields.
If you've never looked at the internal code of [Anki](https://apps.ankiweb.net/), it's decently organized and not terribly complicated.
Basically, you have collections of "stuff", models and templates for notes and cards, and of course cards and notes themselves.
Yes, notes and cards are different things.
Anki decides when something requires a full sync by updating a kind of schema version number inside the SQLlite database.
Certain operations update this number while others don't.
It turns out I was renaming a model field name every single time and import occurred.
Even when the field names were the same!
And, as you can probably guess, the internal method from Anki I was using marked the schema as needing the version number bumped.
Queue full sync.

In order to fix this problem all I had to do was check to see if the new field name and the old field name were the same.
If they were, don't bother updating the model field name.
Simple code change, it took about two hours of work I would say.
It's a good thing too, because I put off working on this sprint until Sunday.
I probably shouldn't do that, but at the same time the whole point is to have achievable weekly goals right?

## PVM and the Long Game

PVM stands for Parsing Virtual Machine.
It's a [Rust crate](https://github.com/amarmaduke/pvm) I've been working on.
There are a lot of parsing crates in Rust's ecosystem to be honest, but I wanted a simple enough set of features that weren't represented.
I wanted a parsing library focused on programming languages (so it should probably use parsing expression grammars (PEG)) and one that supported left recursion.
Left recursion is a simple enough thing to explain: It's having a rule reference itself as the left-most thing, i.e. `rule { rule;"a" }`
The rule will match any string with any number of `a`'s in it.
It's basically just `a+`.
However, left recursion (really the whole gambit, direct (and indirect) left recursion, and mutual recursion) are not typically well supported in PEG libraries.
In my research it seemed to boil down to left recursion not being the most easily implementable thing combined with it being a relatively new feature to get figured out for PEGs.
All the same, I stumbled on some research that described a virtual machine that would execute a PEG grammar and recognize a particular string for that grammar.
The upshot being that additional work by the authors demonstrated it could be extended to support all kinds of recursion.
And more, it basically boiled down to a new stack frame and improved compilation.

Anyway, the long game is to have PVM working with a lot of the modern literature for recursion, error handling, and some context-sensitive bells and whistles.
The intent isn't to have the fastest parser in the west but instead the most convenient one (at least for programming languages).
I got pretty far with it before I got distracted by a programming competition contest.
Right now, it's in need of "finishing the loop".
What I mean is I have the "compiler" and the virtual machine, but I don't have an easy way to take the virtual machine output and construct the abstract syntax tree (AST) of your programming language.
That's what this sprint is about, **make PVM usable as a parsing library from start to finish**.
Then maybe next sprint I can focus on getting direct left recursion working, here's hoping.
