---
layout: post
title:  "Personal Sprints and Getting Stuff Done"
date:   2017-03-20 10:00:00 -0500
permalink: /:categories/:title.html
---


## What is a Sprint?

A sprint is a commitment to completing some amount of work within some period of time.
It is used sometimes in the software world to handle product management.
Whether or not it's useful in that setting is besides the point for me.
I want to use sprints, in particular one week sprints, to combat a particular problem I've noticed.
Perhaps you can relate, have you ever worked on a project only to be distracted by a different project?
The amount of time you think you have to commit to the project you're currently working on almost makes you worried you'll never get to the other project.
Thus, you have to stop what you're doing and do that project instead!
Queue infinite loop.
When I say "you" here I mean "me".

You might think to yourself that this is a perfectly fine state of affairs because you just context switch until the best project wins.
Except it doesn't work out that way, the grass is always greener, except it's not.
As I said, to combat this I want to commit to one week sprints with manageable goals for each sprint.


## Handling Failure

Sounds great, right?
But, what happens when you fail to meet your goal?
What if you're sick the entire weekend and busy with social events throughout the week?
As they say, shit happens.
If sprints are a way to silence the "But what if that project is better" voice by time limiting development time, then there needs to be something else to silence the "But why bother working on it at all, if you're just going to fail?"
The answer, I think, is to make failures real and exposed, but also blameless.
That is partly why this blog post exists.
Every Monday I plan to set a new goal and reflect on the past goal.
Nothing major, not a huge time commitment, just a fifteen minute recap on what happened and why.

Now, ultimately very few if any people will actually read these blog posts, but they're still there.
It's still public knowledge, interesting or not.
Worst case scenario people actually start to care, wouldn't that suck?
That's kind of the point, the mysterious void will bother me if I keep failing (even if it never talks back).
That should pressure me to make more reasonable goals.
At least, that's the plan.

## Goal Numero Uno

Briefly, let me describe Anki.
[Anki](https://apps.ankiweb.net/) is a tool for flashcards.
It has some interesting strategies about frequency in showing and reshowing your flashcards.
Basically, new information is shown more frequently than old information.
However, you still do end up seeing old information.
This kind of reinforcement is suppose to help you remember the information for longer and more clearly.
Whether or not it actually works is something you'll have to research for yourself, suffice to say I like it.

In fact, I like it so much I created a plugin for it called _ankideckffs_ (or Anki Deck From File System).
The plugin is fairly rough around the edges and I'd like to improve on something specific.
Namely, syncing between the desktop app and the android app causes a complete re-import every time you import a deck from the file system (using the plugin).
I primarily want to consume my decks via my phone so this is a big annoyance.
The goal is then clear:

**Make syncing between the android app and the desktop app work after imports from _ankideckffs_**

Here are some bonus objectives that I'll consider doing if I find the time:
* improve the readme,
* add integration tests.

And that's it! See you next week.
