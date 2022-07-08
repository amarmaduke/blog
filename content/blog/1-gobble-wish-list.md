+++
title = "A Programming Language Wishlist"
date = 2022-06-19
draft = false

[taxonomies]
categories = ["Musings"]
tags = ["concatenative", "design"]

[extra]
lang = "en"
toc = true
show_comment = false
math = true
mermaid = false
+++

I've been thinking about a programming language for a while that makes the trade-offs that I prefer.
The high-level overview is something like this:
- no bound variables;
- a type system with at least dependent function types and refinement types;
- a DSL (Domain Specific Language) system that is conducive to inspection and easy extension;
- and efficient execution.

<!-- more -->

Let's talk about each of these.

# No Bound Variables

Bound variables are the heart and soul of the $\lambda$-calculus.
Variables give you the ability to mark internal sharing and are pretty natural based on mathematical practice.
So why get rid of them?
The reason is three-fold.

First, when you are dealing with first-class higher-order functions the variables get in the way of efficient execution by demanding some garbage collection discipline.
One choice to recover efficiency is enforced linearity (i.e. a variable can only occur once in the body), but now you're placing a seemingly arbitrary restriction on what was standard practice.

Second, if you want easy quotable syntax the variables complicate things.
Now the users creating macros have to handle bound variables too, usually by hygienic patterns.
This is the path taken by many modern macro systems.

Third, if you do have a robust DSL system then you can add in bound variables without much issue.
To that point, why complicate the _core_ system with bound variables if it can be implemented as a library feature?

# Rich Type System

The lack of dependent types in most modern languages is caused by a few things.
Dependent types do not play nice with effects (e.g. non-termination, exceptions, I/O), they can complicate type checking, and your average programmer is scared of them.
For a crash course in dependent function types, consider the following type: `Vec Nat n` which represents a list with _exactly_ $n$ elements.
This is impossible to represent in a lot of languages but pretty trivial in a language with dependent types.
Together with the finite type: `Fin n` which represents a number in the range $[0, n)$ you have a safe, optimization friendly way to access arrays:

```rust
    let array : Vec Nat n = ...
    let index : Fin n = ...
    array[index] // no bounds checks necessary
```

Refinement types also seem like a pretty necessary feature, but they are more exotic.
Languages like [Agda](https://github.com/agda/agda) and [Coq](https://coq.inria.fr/) don't have refinement types in the sense I mean, but [F*](https://www.fstar-lang.org/) does.
A simple refinement type is the type of even numbers:

$$\texttt{Even} = \\{ n: \mathbb{N}\ |\ n = 0 \mod 2 \\}$$

Critically, there should be a trivial cast (i.e. an identity function) that forgets the refinements and produces a natural number.
This is not the same as wrapping up a natural number in a dependent pair where the second component is a proof the first is even.
You also likely want some definitional equalities, such as $2 : \texttt{Even} \equiv 2 : \mathbb{N}$.
These choices cause you to have an extrinsic type theory (i.e. a given term can have more than one type).

Another critical requirement is that the type system supports axioms.
In particular, recursive types with the added _axiom_ that they are well-founded.
This is in contrast to most systems which include syntactic requirements like strict positivity.
Although, in plenty of other systems, like [Idris](https://www.idris-lang.org/), a type-in-type discipline is used which allows general recursive types (and thus inconsistency).

The point here is that recursive types should be an _unsafe_ feature that demands some meta-obligations of the programmer, not unlike unsafe code in [Rust](https://www.rust-lang.org/), or "trust me" annotations on recursive functions in Agda or Idris.
However, these "trust me" annotations are not spelled out in the formal core theory.
They are tacked on, and the burden is shifted to the user to make sure they do things right.

Coq and Rust do the best job, in my opinion, of giving the user guidelines of when axioms or meta-obligations are allowed.
Coq has an entire [wiki-page](https://github.com/coq/coq/wiki/CoqAndAxioms) about axioms that you can expect to not break your development.
Rust has some [explicit rules](https://doc.rust-lang.org/book/ch19-01-unsafe-rust.html) about what expectations are in place for unsafe code.
However, it should also be noted how difficult it is to do [pointer cast in unsafe Rust correctly](https://gankra.github.io/blah/fix-rust-pointers/)!
In this scenario, the meta-obligations are too strong.

Regardless, the trade-off is a powerful and necessary one.
Give the user an escape hatch with a well documented set of meta-obligations so that they can express themselves in code to the fullest extent possible.
Moreover, deciding that a recursive function is well-founded is a daily occurrence for programmers and it is often trivially terminating from the perspective of the programmer (but often not trivially terminating from the perspective of syntactic criterion used in Coq or Agda!)

# Powerful DSL System

Let's be honest, there is only one game in town when it comes to reasonable DSLs and that is [Racket](https://racket-lang.org/).
I don't have much experience with Racket and think there is a lot to learn there.
Also, I fundamentally agree that allowing the user to construct DSLs is important if you want a language to help a user express domain knowledge.
Yet, macro systems are a complete disaster.
The greatest failure of Lisp is perhaps its macro system.
Macros in Lisp are so powerful that they make code written by a programmer completely incomprehensible.
Somehow, they are also too weak to express the kinds of syntactic constructs that are more natural on pen-and-paper.
This is likely why Racket is a thing at all, if Lisp solved DSLs at the onset there would be no Racket.

What is needed of a good DSL system?
I think the following things:
- easy inspection via the core syntax both with a debug representation and the actual representation;
- easy construction by well-known grammar definitions;
- and easy combination and interoperability between DSLs.

To inspect a DSL I propose the requirement that any span of a DSL can be independently transformed into core syntax.
For example, consider the following DSL code:

```rust
    fn quadratic(a: usize, b: usize, c: usize) -> usize {
        a*a + b*b + c
    }
```

In case you missed the implication, a language without bound variables basically ends up looking like a variation on [Forth](https://www.forth.com/forth/).
Here is how I imagine the above representation being encoded:

```rust
    [
        // stack starts as [c, b, a]
        dup *       // compute a^2
        swap dup *  // compute b^2
        + +         // compute a^2 + b^2 + c
    ]
    [quadratic]
    define
```

Where the syntax `[...]` is a _quote_ inspired by [Joy](https://en.wikipedia.org/wiki/Joy_(programming_language)).
Now, if a user selects the `b*b` span in the DSL, they should be able to see that it maps to `swap dup *` code in the core syntax.
It might not be the easiest to comprehend Forth-style (or really Joy-style) syntax for most programmers.
Indeed, it is likely better to describe it as a high-level assembler, but the benefits are that it does always make sense, even if it takes some effort to figure out what.
In contrast, someone's invented notation with no documentation may _never_ make sense.

# Efficient Execution

A concatenative programming language, which is ultimately what I am describing, yields to fairly obvious efficient execution by way of a linear type system.
The real issue only arises with quotes which are the replacement for higher-order functions.
For this, the proposed fix is to require that quotes are not data unless boxed or otherwise hidden behind a pointer.
Ultimately, this pushes the garbage collection duties to the user, they have to construct smart pointers like reference counting.

However, that is the main design principle behind all of this.
Keep the core language as simple as possible without sacrificing expressibility or power.
Push as much as possible into libraries.
As the design grows this core principle will remain.
