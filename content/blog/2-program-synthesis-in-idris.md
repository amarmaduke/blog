+++
title = "Program Synthesis in Idris 2"
date = 2023-08-02
draft = false

[taxonomies]
categories = ["Musings"]
tags = ["synthesis"]

[extra]
lang = "en"
toc = true
show_comment = false
math = true
mermaid = false
+++

Program synthesis enables a tool to automatically generate a program matching some specification.
In Idris 2 specifically this capability is espoused as a better method of interacting with the tool.
Indeed, the conjecture is that in dependent type theory we sometimes fully specify the function in the type anyway, so why bother writing it again?

<!-- more -->

# Abstract View of Program Synthesis

What is program synthesis?
Consider a functional program with the following type:
```haskell
add : Nat -> Nat -> Nat
```
Program synthesis is the problem of finding _any_ program that satisfies some constraints (in this case the type).
For example, the following synthesized program is a valid answer:
```haskell
add : Nat -> Nat -> Nat
add n m = 0
```
Of course, this isn't the kind of answer we expect, but it is an answer!
The problem:
1. the type of `add` is not specific enough to arrive at the function we expect
2. and the heuristics we use to determine which program to pick are badly tuned

Abstractly, program synthesis works over some syntax of programs and some set of edit actions and generates a graph of possible programs.
This graph can be _infinitely_ large if not at least exponentially large, depending entirely on the syntax and edit actions the synthesis is working over.
For this reason it is important to not only pick a small set of desirable edit actions but to prune/order the search space with heuristics.
Indeed, program synthesis is ultimately a traversal of the generated graph.

To sum it up precisely, program synthesis consists of the following:
1. A set of syntactic forms _with holes_ (usually represented as an inductive type), $\mathcal{S}$
2. A type representing available information at a given hole, $\mathcal{Ctx}$
2. A set of edit actions $e \in \mathcal{E}$ with type $e : \mathcal{Ctx} \to \mathcal{S}$
3. A (usually coinductive) traversal algorithm $\mathcal{T}$ with type $\mathcal{T} : \mathcal{S} \to \text{Stream}\ \mathcal{S}$

For example, suppose our syntax consists of all Haskell programs, and we have four edit actions:
1. Case split on a variable
2. Try a variable in context if the types match
3. Try a constructor if the types match
4. Try a recursive call if the types match

One path through the graph is: case split on the first input (generates two holes); try constructor 0 on first hole; recursive call on input (generates two holes); constant 1 on first hole; second variable on second hole.
This sequence is visualized below:
```haskell
-- starting node
add : Nat -> Nat -> Nat
add n m = ?0
-- 1st edit action
add 0 m = ?0
add (n + 1) m = ?1
-- 2nd edit action
add 0 m = 0
add (n + 1) m = ?1
-- 3rd edit action
add 0 m = 0
add (n + 1) m = add ?2 ?3
-- 4th edit action
add 0 m = 0
add (n + 1) m = add 1 ?3
-- 5th edit action
add 0 m = 0
add (n + 1) m = add 1 m
```
Of course, with this definition program synthesis could produce a goal with a hole.
This may or may not be desirable, but it is easy to throw away leaf nodes that have holes (i.e. programs with holes that somehow have no valid edit actions).

Note that the traversal algorithm produces a stream of possibilities because we want the user to be able to cycle through different synthesized programs, in case the first attempt is not desirable.

# Program Synthesis in Idris 2

The following description is synthesized from these resources:
1. [Secrets of type driven program synthesis - Edwin Brady | Lambda Days 2021](https://www.youtube.com/watch?v=E7uSsL8r_mU) (the slides are available [here](https://www.lambdadays.org/static/upload/media/1613990474814809idrissynthesisedwinbrady.pdf))
2. [Dependent Type Driven Program Synthesis](https://www.youtube.com/watch?v=s9PAb9c6J44)
3. [Idris 2 source code for expression search](https://github.com/idris-lang/Idris2/blob/main/src/TTImp/Interactive/ExprSearch.idr)

The syntax of Idris 2 is a dependent type theory with a Haskell-style, not unlike the syntax of Agda.
The main difference is that Idris 2 has _quantities_ in its function types.

For Idris' program synthesis it consists of three "major" edit actions:
1. Initialize
2. Case split on an input variable (heuristic: limited to depth of 1, no nested case splitting)
3. Expression search

Expression search consist of a list of "minor" edit actions:
1. Try a variable in context when the type of the hole can be unified (heuristic: also try pair projections `fst` and `snd`)
2. Try a lambda if the type of the hole is a function type
3. Try a constructor for the type of the hole when the resulting types can be unified, then expression search on the holes for the constructor arguments
4. Try a recursive call with a descending argument to the function being defined (heuristic: also try let-abstracting this recursive call)

The traversal algorithm will initialize a function, and then try expression search followed by case splitting (left-to-right).
Expression search will try all its minor edit actions in order.
Moreover, the traversal algorithm will generate a batch of candidates (of a small size, ~16) and orders that batch by number of inputs used.
The idea is that a program _probably_ wanted to use all inputs, so those synthesized programs should be presented first.

The "Initialize" action simply sets up the function with input variables and a hole for the body:
```haskell
add : Nat -> Nat -> Nat
-- initialize edit
add : Nat -> Nat -> Nat
add n m = ?0
```
The "Case Split" action will case split only to depth of 1 and left-to-right, below is an example of it being applied three times:
```haskell
add : Nat -> Nat -> Nat
-- initialize edit
add : Nat -> Nat -> Nat
add n m = ?0
-- 1st case split
add : Nat -> Nat -> Nat
add 0 m = ?0
add (n + 1) m = ?1
-- 2nd case split
add : Nat -> Nat -> Nat
add 0 0 = ?0
add 0 (m + 1) = ?2
add (n + 1) 0 = ?1
add (n + 1) (m + 1) = ?3
-- 3rd case split
-- fails
```

For expression search, many edits only work if the synthesized expressions type unifies with the holes type.
Unification is needed in the case of Idris because types may be dependent and may have implicit arguments.
For example:
```haskell
f : Vec A n -> Vec A (n + 1)
f v = ?0
-- edit try v
-- fails, Vec A n != Vec A (n + 1)
```
The implementation has a method of unifying types already as that is required for type checking.
In the above case, there is no way to unify the type of the variable `v` and the type of the hole `?0` so the try-variable edit action fails.
Unification is not strictly needed to accomplish this kind of goal, it depends on the language.
Indeed, convertibility of types will also work, but it might miss programs that unification would be able to unify.

This unification check is also important when trying constructors because the type might refute a particular constructor as possible.
For example:
```haskell
f : A -> Vec A n -> Vec A (n + 1)
f a v = ?0
-- edit try constructor vnil
-- fails Vec A (n + 1) != Vec A 0
```
When synthesis tries the `vnil` constructor for a vector that we know _must_ have at least one element, unification is unable to unify the type of `vnil` with the type of the hole `?0`.
Thus, the `vnil` constructor is rejected and the `vcons` constructor is tried instead:
```haskell
f : A -> Vec A n -> Vec A (n + 1)
f a v = ?0
-- edit try constructor vcons
f a v = vcons ?1 ?2
-- edit try variable
f a v = vcons a ?2
-- edit try variable
f a v = vcons a v
```
Of course, synthesis could have tried the variable `v` in hole `?1` but again the types would not unify, as the type of `?1` is `A`.
Unification in this way is _pruning_ search paths in the graph.
When unification succeeds it also tends to prune the search space by forcing the definition of holes that show up in implicit arguments of types.

# Manually Worked Examples

Below we work some examples following the Idris 2 traversal algorithm.

## Addition of Naturals with No Specification
```haskell
add : Nat -> Nat -> Nat
-- initialize
add n m = ?0
-- expression search on ?0
-- try variable n in context, Nat = Nat
add n m = n -- done (1)
-- try variable m in context, Nat = Nat
add n m = m -- done (2)
-- try constructor 0
add n m = 0 -- done (3), Nat = Nat
-- try constructor S
add n m = S ?1
-- try variable n in context, Nat = Nat
add n m = S n -- done (4)
```
The order of the batch would list (1), (2), and (4) arbitrarily followed by (3)

## Addition of Naturals with Specification
```haskell
data AddSpec : Nat -> Nat -> Type where
    Zero : {m : Nat} -> AddSpec 0 m
    Succ : {n m : Nat} -> AddSpec n m -> AddSpec (S n) m

add : (n m : Nat) -> AddSpec n m
-- initialize
add n m = ?0
-- expression search on ?0
-- try variable n in context, Nat != AddSpec n m
-- try variable m in context, Nat != AddSpec n m
-- try constructor Zero,
    -- AddSpec 0 ?1 != AddSpec n m
    -- (because 0 != n, but we can unify ?1 = m)
-- try constructor Succ,
    -- AddSpec (S ?1) ?2 = AddSpec n m
    -- cannot unify S ?1 and n
-- try a recursive call, but no input is descending
-- case split on n
add 0 m = ?0
add (S n) m = ?1
-- ?0: try variable m in context, fails
-- ?0: try constructor Zero,
    -- AddSpec 0 ?2 = AddSpec 0 m
    -- unification forces ?2 = m
add 0 m = Zero
add (S n) m = ?1
-- try variable n in context, fails
-- try variable m in context, fails
-- try constructor Zero, fails
-- try constructor Succ,
    -- AddSpec (S ?3) ?4 = AddSpec (S n) m
    -- unification forces ?3 = n and ?4 = m
    -- now ?5 : AddSpec n m
add (S n) m = Succ ?5
-- try variable n in context, fails
-- try variable m in context, fails
-- try constructor Zero, fails
-- try constructor Succ, fails
-- try recursive call on descending argument (n and m)
    -- add n m : AddSpec n m which unifies
    -- note the traversal could have tried (n and n)
    -- but this would not unify AddSpec n n != AddSpec n m
    -- so the only valid recursive call is `add n m`
add (S n) m = Succ (add n m) -- done
-- by design there is only one valid program to generate
```

Note that as of July 2023 Idris 2 will find this definition.

## Addition of Naturals with Partial Specification
```haskell
data AddSpec : Nat -> Type where
    Zero : AddSpec 0
    Succ : {n : Nat} -> AddSpec n -> AddSpec (S n)

add : (n m : Nat) -> AddSpec n
-- initialize
add n m = ?0
-- expression search on ?0
-- try variable n in context, Nat != AddSpec n
-- try variable m in context, Nat != AddSpec n
-- try constructor Zero,
    -- AddSpec 0 != AddSpec n
-- try constructor Succ,
    -- AddSpec (S ?1) = AddSpec n
    -- cannot unify (S ?1) and n
-- try a recursive call, but no input is descending
-- case split on n
add 0 m = ?0
add (S n) m = ?1
-- ?0: try variable m in context, fails
-- ?0: try constructor Zero,
    -- AddSpec 0 = AddSpec 0
add 0 m = Zero
add (S n) m = ?1
-- try variable n in context, fails
-- try variable m in context, fails
-- try constructor Zero, fails
-- try constructor Succ,
    -- AddSpec (S ?2) = AddSpec (S n)
    -- unification forces ?2 = n
    -- now ?3 : AddSpec n
add (S n) m = Succ ?3
-- try variable n in context, fails
-- try variable m in context, fails
-- try constructor Zero, fails
-- try constructor Succ, fails
-- try recursive call on descending argument (n and m)
    -- add n m : AddSpec n m which unifies
add (S n) m = Succ (add n m) -- done (1)
-- but now there are more options!
add (S n) m = Succ ?3
-- case split on m
add (S n) 0 = Succ ?3
add (S n) (S m) = Succ ?4
-- ?3: try variable n, fails
-- ?3: try constructor Zero, fails
-- ?3: try constructor Succ, fails
-- ?3: try recursive call on descending arguments (n and n)
add (S n) 0 = Succ (add n n)
add (S n) (S m) = Succ ?4
-- try variable n, fails
-- try variable m, fails
-- try constructor Zero, fails
-- try constructor Succ, fails
-- try recursive call on descending arguments (n and m)
add (S n) 0 = Succ (add n n)
add (S n) (S m) = Succ (add n m) -- done (2)
-- try recursive call on descending arguments (n and n)
add (S n) 0 = Succ (add n n)
add (S n) (S m) = Succ (add n n) -- done (3)
```

Note that as of July 2023 Idris will return the 2nd definition as its first synthesis:
```haskell
add (S n) 0 = Succ (add n n)
add (S n) (S m) = Succ (add n m)
```
Thus, the manually worked example is missing some details of the complete algorithm, most likely to do with how Idris 2 picks descending arguments or how the batch ordering interacts with case splitting.
