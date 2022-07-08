+++
title = "What is Semantics?"
date = 2022-07-07
draft = false

[taxonomies]
categories = ["Musings"]
tags = ["philosophy", "semantics"]

[extra]
lang = "en"
toc = true
show_comment = false
math = true
mermaid = false
+++

Semantics is a surprisingly controversial subject.
Dana Scott, known for many things not the least of which is Domain Theory, is recorded as having said that operational semantics is _not_ semantics.
Giorgi Japaridze, known for cirquents and Computability Logic, will tell you that Game Theory _is_ semantics, or at least a generalization of classical semantics (and that classical semantics _is_ semantics).
Indeed, in his mind linear and intuitionistic logic are _syntactically_ motivated and have no satisfactory semantics!
Moreover, I have personally had people decide to not engage in a discussion with me, because of my own stance on semantics.
There in lies the point of this discussion, to spell out exactly what I think semantics really is.

<!-- more -->


# Compiling Interpreted Compilers

Imagine you had a compiler, $K$, whose job it was to compile platform independent bytecode to machine code.
This machine code, is of course interpreted by program $I$.
Moreover, let us focus on a particular bytecode program, a compiler for the C programming language.
My question is this, where is the semantics?
Is it in the informal description of C?
Or what about how that code is interpreted by $I$?
Maybe it is in how that code is compiled by $K$?
Finally, could it be how the CPU executes the machine code?

The purpose of semantics is to give _meaning_ to otherwise meaningless syntactic constructs.
The word "apple" is a string of characters, meaningless until a human interprets it and gives it meaning as a reference to an edible object.
This is the core of what I think semantics really is, it is the subjective interpretation of a thing _in terms of physical objects_.
With this definition, Game Theory falls short, as the object of study is the theoretical game, a mathematical construct.
Moreover, Category Theory fails, Set Theory fails, _any_ mathematical theory whose objects of study are imaginary idealized objects fails.
Scott is now as upset with me as Japaridze is.
Who am I kidding, Scott would just roll his eyes and continue to believe imaginary continuous functions really give any meaning to symbols on a piece of paper.

No, reality is where semantics lies, but not _just_ reality, because an interpreter is always necessary.
Things only have meaning in the eye of a beholder, in you.
Why then, can't we say that semantics consists of imaginary bits, if it is all subjective?
Semantics can be _idealized_ in terms of imaginary bits, but ultimately you are a flesh machine computing with physical bits and pieces.
You are not capable of escaping the substrate by which you exist.
There is a philosophical commitment here, that the physical world really is, and that it is regardless of any observer to it.
I have no interest in defending this philosophical position as I think any other is utter nonsense, but it is important to state the assumption.

Thus, the physical world grounds all interactions you have with it, even if your hardware can misinterpret stimulus or malfunction.
Reality merely is and semantics is the interpretation of our thoughts, our ideas, our language, in the terms of our very substrate.
Moreover, this is why you are able to communicate meaning at all.
Imagine for a second that two people lived inside virtual realities that were completely different from birth.
Then, pulled from their personal heavens, they are forced to interact with one another.
The only shared experience they would have is that they _can_ experience and that they are both experiencing something _new_.
How would these two people communicate what an object in their respective reality is to another?
Maybe with time, they could develop language, but it would all be based on shared experience in their new reality.

Yes, semantics may be the subjective interpretation of language in terms of physical objects, but its _purpose_ is to communicate meaning between observers.
Even between your past self and your future self.
As a programmer, it is easy to sympathize with returning to a codebase after a long vacation and not really remembering what all of it does.
The shared semantics is what lets you get back into the swing of things, between your past self and your current self.

# Presuppositions and Logic

There is a bit of potential circularity going on here, I am giving meaning to semantics, a semantics of semantics?
Under what rules am I allowed to assign meaning to anything?
The easiest answer is _any_ rules, I am unrestricted in how I give meaning to things.
Of course, I am actually restricted, I am restricted by the physical world.
The restriction by the physical world prevents any circularity, as is I have already committed to _it_ existing, reality is the axiomatic starting point.

This leads to another question, though, what other axioms are there?
In the usual philosophy of classical logic we entertain many logic axioms _a priori_.
That is, we assume them to be inherently true.
I reject this, because _logic_ is, in my opinion, a subjective discipline.
It is a way of assigning semantics to statements.
Take propositional logic as an example, we have the propositional variables, $A, B, C, \ldots$, and the connectives: $\wedge, \vee, \neg$.
Immediately, a logician will begin to tell you what statements generated from these symbols _mean_.
Semantics comes before logic.

For classical logic, the boolean semantics is often sufficient, atoms are interpreted as boolean-valued statements with $\wedge$ meaning logical and, $\vee$ meaning logical or, and $\neg$ meaning logical negation.
This is a simple semantics of boolean constants, variables, and operators.
It originates from our subjective experience of physical objects with two states or with yes-or-no questions.
Is the door closed or open?
Are you coming to the party or not?
It fails in situations where more fidelity is needed, such as questions about how tall someone is, the quantity of apples needed for the apple pie, or the amount of tolerable risk.
It _fails_ because the language is not powerful enough to express those situations and the semantics only strong enough to give meaning to the language.

The only presuppositions that I take (as previously stated) is that physical reality _exists_ where existence means some aspect of reality is able to observe itself.
However, logic yields an interesting case study when cast in the veins of Computer Science.

# Operational Semantics is Semantics

What is operational semantics?
It is the description of a set of states that a system can take and a transition relation between those states.
For simplicity, we can think of operational semantics as giving meaning to a language in terms of a machine.
Critically, any machine description we come up with should have a physical realization, but if we restrict ourselves from having infinite states or infinite transitions this is easily accomplished.
Potential infinities are easily added by having a zero state, and a successor transition from zero to itself.
Given infinite time, the machine can now execute infinitely, but this situation is only theoretically possible.

Any interpretation of a language in terms of physical reality admits at the very least an approximation by way of a machine.
Indeed, as far as we can tell all physical motion is machine-like.
Moreover, I would happily retroactively define operational semantics to mean _any_ physical machine that is realizable, though this is not how the term is typically used.
With this setup, it is my opinion that a language is only a logic when it has an operational semantics.

How then, are we able to talk about any mathematical object?
The answer is that mathematical objects are all idealizations of real objects.
Take an orange, forget any surface structure, forget an entire dimension of its structure, smooth the curve defining it, and you have a circle.
Mathematical objects are obtained by _forgetting_ information about physical objects.
A language already approximates the physical world so forgetting information is baked into the definition of a logic.
Thus, a logic is a language expressing a finite set of idealized machines and execution traces of those machines.
The only real difference between mathematics and logic is that, culturally, logic does not include any language to describe its objects of study, whereas mathematics does.
Logic only has variables or individuals to mark idealized objects, but mathematics constructs wildly interesting ones.

However, there is a final comment about transitivity of semantics.
If Category Theory is a language with semantics (as described above) then is it not the case that any other language _modelled_ by Category Theory has a semantics?
My answer to this is, of course, yes.
Just as with our compiled interpreted compiler, once a language has a semantics it can be used as a semantics for another language.
However, I would always prefer to call this instead a _model_ of the language in terms of some other language, but the point stands that if a semantics is what one is after then producing a model is already enough.

As a final thought, it is important to note that most semantics we construct are idealized because constructing true physical machines is a difficult task.
For example, a Turing machine is an idealized machine since it has an infinite tape, yet it is still very close to physical reality.
However, this very idealization leads us to silly situations once we start feeding our infinite tapes of Turing machines into others.
It is my opinion that when researchers make sense of these silly situations what they are really doing is constructing a _different_ operational semantics that symbolically evaluates the Turing machines with their infinite tapes.
Indeed, our intended semantics can accidentally become the object of study when we touch the parts of it not grounded in reality.
