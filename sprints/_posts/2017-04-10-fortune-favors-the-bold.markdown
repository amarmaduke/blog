---
layout: post
title:  "Sprint: Fortune Favors the Bold"
date:   2017-04-10 10:00:00 -0500
permalink: /:categories/:title.html
---

## Not Again!
I have some unfortunate news.
I did not hit my sprint goal as stated.
However, I did work on the parser for at least a couple of hours every day that made sense to.
Now, I could have worked harder over the weekend but I'm doing this in my free time so cut me _some_ slack.
The parser is more or less fleshed out with unit tests against it.
What held me back was a couple of bugs that I had to work through.
There are still at least two bugs that I know of in the parser.
Parenthesis is not handled correctly (the closing parenthesis is getting consumed too early) and lookahead is too greedy (it takes everything to the right of it as argument).
Lookahead should "bind" more tightly.
Perhaps it's hard to explain without getting technical but as an analogy it should bind like exponentiation.
You're not raising everything to the left to some power just the "closest expression."

Overall I'm happy with the progress I made.
It really wasn't too terribly far away from the sprint goal, and I don't think missing a sprint goal should be the ultimate decider of success.
What it should mean is that I was either too ambitious or just bad at estimating work.
Frankly I don't value estimation (in terms of planning poker) very much but as I've probably said I think having an actionable goal to shoot for is useful.
Not hitting the goal but having measurable progress?
That sounds good enough to me.

## So Let's be Bold
I have been enjoying working on the parser.
There is still a lot to be done.
I stubbed out all the possible ways the parser could fail but right now in every failure scenario it returns the same error code, zero.
There is a lot to be done on the usability front.
I think the better goal though is to iron on the bugs in the parser, complete the dog-food, and go straight for left-recursion support.
Left-recursion is the ultimate goal of this, it's kind of the reason I'm writing my own parser library.
Thus, it seems reasonable to push harder towards that.
So let's be bold, our goal for this week is to **get left-recursion working**.
