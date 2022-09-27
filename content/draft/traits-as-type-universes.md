+++
title = "Traits as Type Universes"
date = 2022-09-26
draft = false

[taxonomies]
categories = ["Musings"]
tags = ["design"]

[extra]
lang = "en"
toc = true
show_comment = false
math = true
mermaid = false
+++

What is the domain of a quantification?
Is it everything that is?
Everything that can be?
Where do we draw the line on what is quantified over?

<!-- more -->

In type theory land, or at least the modern hegemony quantification of types is solved by postulating an infinite tower of larger and larger types.
This was done to solve size issues by some famous people, like Bertrand Russell.
Personally, I think it's a hack.

It originates from the problem of well-founded recursion.
We want our logics to be consistent because we want to trust our results, but if we allow certain kinds of quantification then we can write non-terminating functions.
Really the situation is worse then that, we can write _any_ function at _any_ type.
This happens, famously, if you postulate that `Type : Type`, i.e. that the type of the universe of types is itself a type.

So we fix it by postulating an even bigger type, `Type₁ : Type₂`, but now we ask the question, what is the type of _that_ type?
Never fear, we postulate an even bigger type, and so on, and so forth.
Tools like Agda will take this extremes, postulating an infinite oridinal index for the types.

What if, instead, the question of typehood was not also at the type level at all?
What if, it was at the trait (i.e. typeclass) level?
If types are viewed as descriptions of data, the ways certain elements are put together, then a type gives a domain of quantification for the data.
A trait, in turn, would give a domain of quantification for _types_.

Let us push this analogy further.
I think the proper way of thinking about types is that they are an analytic tool for understanding the world.
The describe data and allow the construction of data.
Types are the tools for building interesting lego projects.

However, a trait is better understood as part of the synthetic world.
A trait postulates that a certain kind of behavior is available that may have some type itself, but not exactly what it does.
Quantification over a trait allows any type that satisfies the behavior.
Quantification over a type allows any of the constrained data.

For example, let's suppose we have types with functions, disjoint sums, products.

` t ::= t | t x t | t + t | t -> t`

For traits, we have records that specify required functions, but we can also take a nod from Scala and include intersections and unions (that are only well-founded if the traits have disjoint labels).

` c ::= (l:t) | c ∪ c | c ∩ c`

Now, like in any programming language that features typeclasses or traits, the universe of types described by a trait is open.
We have some method of postulating that a type satisfies the trait by giving definitions to its labels that satisfy the associated type.
Expanding our language with quantification, we now have dependent functions and ad hoc polymorphic functions.

What is a polymorphic function? Like the identity function?
Normally, we give it type $\forall T : \texttt{Type}. T \to T$.
That means we need a trait, Type, that asserts when something _is_ a type.
Taking a nod from semantic definitions of a type, we could demand that the implementation of an object is a type when we know its inhabitants and their equalities.
With this information encoding the trait, it is easy to piece together generic inclusions for the type formers.
Given two things, `a` and `b`, which are Type, we build an instance of Type for `a x b`, `a + b`, and `a -> b` in the usual way.

Interestingly, this does not give us an impredicative universe of types, at least not immediately.
We would need to describe an instance of Type for any quantification over things of Type to make it impredicative.
The way things are setup in this fashion the control over quantification seems much more fine grained without necessarily losing any universes you had before.

