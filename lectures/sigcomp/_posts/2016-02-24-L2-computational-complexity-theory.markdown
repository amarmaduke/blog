---
layout: post
title:  "Computational Complexity Theory and Heuristics"
date:   2014-02-24 11:15:00 -0500
permalink: /:categories/:title.html
---

- Introduction to Computational Complexity Theory
- The Pragmatic Hierarchy
- Determining Time Complexity
- Heuristics Using Problem Bounds
{:toc}

This post assumes you are familiar with it's predecessor, [Lecture One](L1-competitive-cpp-and-java.html).
We will be using shortcuts discussed in that post like `#include <bits/stdc++.h>` which may or may not work with your particular compiler.

## Introduction to Computational Complexity Theory
During a competitive programming contest, much like in the real world, there is often the question of "is this fast enough?"
Or, "does this scale?"
The creative process of finding a solution in its entirety might go something like this:

* Do I understand the problem?
* Can I demonstrate that the problem is solvable at all? In general?
* Can I find a solution?
* Is my solution practical enough (under realistic resource constraints)?
* Can I find a better solution?

In a contest this process is simplified somewhat.
First we clearly do need to understand what it is we're trying to solve, but we don't need to worry ourselves with whether or not it is solvable.
Indeed, in most practical real world cases it's fine to assume that the problem your working on is solvable.
If it's not solvable then it's likely a very well known problem (e.g. the Halting Problem) and you'll discover that fact rather quickly.
Finding a solution has some friction, it requires a certain amount of ingenuity and a large enough knowledge pool to draw from.
Yet, once you have a solution, any solution, the issue remains of whether or not it's practical.
A vague idea of _practical_ is if the solution produces the correct answer for the associated inputs in a sufficient amount of time and memory.
We could also consider code size in relation to maintaining the software in the future but for our purposes we're mostly interested in time, but we'll briefly discuss space and error practicality.

Consider this, (C++11)

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;

int solve(int n) {
   return n == 0 ? 1 : solve(max(n - 1, 0)) + solve(max(n - 2,0));
}

int main() {
   for (unsigned i = 0; i <= 45; ++i) {
      auto start = chrono::high_resolution_clock::now();
      int result = solve(i);
      auto end = chrono::high_resolution_clock::now();
      auto ms =
         chrono::duration_cast<chrono::microseconds>(end - start).count();
      auto s =
         chrono::duration_cast<chrono::seconds>(end - start).count();
      cout << i << ": " << result
         << " in " << ms << " ms, " << s << " s" << endl;
   }
}
{% endhighlight %}

This recursive solution for computing the Fibonacci sequence does a decent job.
In fact, if you only cared about the first twenty Fibonacci numbers this might just be fast enough.
Unfortunately, there are two very impractical things about this code.
Do you think you know?
They're both obvious if you execute the program and wait for it to terminate.
Figure it out?
It's too slow, and the datum used (a likely 32-bit integer) is too small so it overflows.
These problems can be thought of as a time constraint and an error constraint.
Although error constraints are usually thought of in terms of floating point arithmetic the idea is the same: "Is my machine representation of this mathematical value sufficient to produce the approximately correct output?"
In this case, the answer is a clear no, a Fibonacci number should never be negative.

Consider this altered version,

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;

typedef long long i64;
map<int, i64> memo;

i64 solve(i64 n) {
   if (n == 0LL or n == 1LL) return 1LL;
   i64 first = memo[n - 1] != 0LL ? memo[n - 1] : solve(n - 1LL);
   i64 second = memo[n - 2] != 0LL ? memo[n - 2] : solve(n - 2LL);
   memo[n] = first + second;
   return first + second;
}

int main() {
   for (int i = 0LL; i <= 92LL; ++i) {
      auto start = chrono::high_resolution_clock::now();
      i64 result = solve(i);
      auto end = chrono::high_resolution_clock::now();
      auto ms =
         chrono::duration_cast<chrono::microseconds>(end - start).count();
      auto s =
         chrono::duration_cast<chrono::seconds>(end - start).count();
      cout << i << ": " << result
         << " in " << ms << " ms, " << s << " s" << endl;
   }
}
{% endhighlight %}

Now, instead of recomputing values we store the values we already computed in memory.
We can think about this as if the computer has _learned_ that input and so should be able to _recall_ it from memory.
This strategy is also called Dynamic Programming, where we prove to ourselves that we can break the problem into sub problems that appear in the main problem sufficiently often.
The trade off here is that we're using more memory than before, we have to store a 64-bit integer for every value of the Fibonacci sequence that we want.
The 64-bit integer does give us some additional ground when it comes to the count of Fibonacci numbers we can represent, but it fails at the ninety-second Fibonacci number, overflowing again.

Consider this final version,

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;

vector<bool> operator+(const vector<bool> &a, const vector<bool> &b) {
   size_t N = max(a.size(), b.size());
   size_t n = min(a.size(), b.size());
   vector<bool> result(N + 1, false);
   bool carry = false;
   for (size_t i = 0; i < n; ++i) {
      bool a_i = a[i], b_i = b[i];
      bool val = carry xor (a_i xor b_i);
      result[i] = val;
      if (not carry and (a_i and b_i)) carry = true;
      else if (carry and (a_i or b_i)) carry = true;
      else carry = false;
   }
   for (size_t i = n; i < N; ++i) {
      bool val;
      if (a.size() > b.size()) val = a[i]; else val = b[i];
      result[i] = carry xor val;
      carry = carry and val;
   }
   result[N] = carry;
   return result;
}

string strify(const vector<bool> &v) {
   string tmp = "";
   for (int i = 0; i < v.size(); ++i) {
      if (v[i]) tmp += "1"; else tmp += "0";
   }
   reverse(tmp.begin(), tmp.end());
   string result = "";
   bool leading = true;
   for (int i = 0; i < tmp.size(); ++i) {
      if (tmp[i] == '1') leading = false;
      if (not leading) result += tmp[i];
   }
   return result;
}

typedef vector<bool> integer;
map<int, integer> memo;

integer solve(int n) {
   if (n == 0 or n == 1) return integer(1, 1);
   integer first = memo.count(n - 1) != 0 ? memo[n - 1] : solve(n - 1);
   integer second = memo.count(n - 2) != 0 ? memo[n - 2] : solve(n - 2);
   memo[n] = first + second;
   return first + second;
}

int main() {
   for (int i = 0; i <= 1000; ++i) {
      auto start = chrono::high_resolution_clock::now();
      integer result = solve(i);
      auto end = chrono::high_resolution_clock::now();
      string output = strify(result);
      auto ms =
         chrono::duration_cast<chrono::microseconds>(end - start).count();
      auto s =
         chrono::duration_cast<chrono::seconds>(end - start).count();
      cout << i << ": " << output
         << " in " << ms << " ms, " << s << " s" << endl;
   }
}
{% endhighlight %}

In the real world you don't want to implement your own arbitrary size integers.
Even in a competitive programming contest you're better off switching to Java and using `BigInteger`, but we started with C++ so let's end with it.
This code shifts to an arbitrary sized integer using `vector<bool>` as a backing store.
It should be noted that `vector<bool>` has some special semantics and it's debatable whether you should even consider it a "container of bool", but we're not using it as a container just as a convenient method of abstracting a contiguous sequence of bits.
With that in mind, all we need is addition and a way to print it.
All of our error constraints are mostly satisfied.
The only possible problems are if we run out of memory, or if we want a Fibonacci number whose index doesn't fit in a 32-bit representation.
We've traded memory for speed and precision.
Although this implementation could be significantly optimized it still severely out performs the first implementation.
We can now print out the first thousand Fibonacci numbers with ease.

The question you might ask is how did we know what to improve?
How did we know the bottlenecks?
The answer lies in something called Computational Complexity Theory.
The idea is to obtain a measurement of how some resource an algorithm uses scales with respect to some variable.
This scaling helps us build an intuition of how fast something is, where we might need to direct our attention for improvement, and just how good our improvements really are.
We'll learn more than just how things perform at scale though, in competitive programming it is useful to know when you can get by with "just enough".
For that we need to learn a couple other tricks.

### Asymptotic Analysis

<div class="definition">
Given functions \(f : Params \to \mathbb{R}\) and \(g : Params \to \mathbb{R}\) with some shared parameter space \(Params\), then we say \(f\) is in the \(\textit{complexity class}\) \(\mathcal{O}(g)\), \(f \in \mathcal{O}(g)\), if there exists \(c : \mathbb{R}\) and parameters \(n_0, n_1, \cdots, n_k : Params\) for finite \(k\) such that for all \(m_i \geq n_i\) we have \(f(m_0, \cdots, m_k) \leq cg(m_0, \cdots, m_k)\).
</div>

This definition is trying to convey a simple idea.
If we have two functions that measure how much time it takes for a program to do something then if one of those measurements is always smaller than a constant times the other after some fixed parameter input then that smaller measurement is in the $$\textit{complexity class}$$ of the larger measurement.

Consider the following two functions, $$f(n) = 2n^2$$ and $$g(n) = n^2$$, with one parameter $$n$$ the size of the input.
It might seem strange at first but we can show $$f \in \mathcal{O}(n^2)$$.
This is easy enough to prove, select $$c = 3, n_0 = 0$$ and it's trivial.
Why would we want to do this?
Because we only want to remember a select few complexity classes.
The point of this analysis is to convey a lot of information about the scaling of our algorithm very quickly.
To that effect we want to ignore lower order terms and constant factors.

What is meant by lower order terms?
A lower order term is any part of the function, separated by addition, whose contribution is dominated by some other term.
Consider $$f(n) = n^2 + n + 1$$.
If you're keen enough, you should be able to prove $$f \in \mathcal{O}(n^2)$$.
This is very useful, we can ignore parts of the computation that don't play a role at scale.
We have a quick and effective method of determining the practicality of our algorithm.

This kind of notation to express complexity classes is called Big-O notation.

Here are some properties of Big-O:

$$ \begin{gather}
\mathcal{O}(cf) = \mathcal{O}(f),~\forall c : \mathbb{R} \\

\mathcal{O}(n^k + n^{k-1} + \cdots + n + 1) = \mathcal{O}(n^k),~\forall~ \mbox{finite}~k \\

f \in \mathcal{O}(g) \implies \mathcal{O}(g + cf) = \mathcal{O}(g),~\forall c : \mathbb{R}
\end{gather} $$


### The Constant Matters

There is one lie I've told that I should make clear.
For any algorithm there is always a constant factor on its largest contributing term.
Even if this constant is just one, there is always some constant.
Big-O notation hides away this constant because it shouldn't matter at scale, but in practice it matters.
Because we're taking a pragmatic approach we sometimes need to figure out that constant and use it to aid us in determining if our algorithm is good enough.

More often than not the constant really doesn't matter.
Your algorithm is plenty fast enough and the constant is probably less than or equal to five or some small value.
However, there are some algorithms were the constant is so large that the parameters would have to, in turn, be so large to see a benefit that the algorithm is impractical.
For that reason you should at least keep in mind that the constant can, and does, matter.

## The Pragmatic Hierarchy

If you'd like to learn more about the background and theory involved with Big-O notation, Computation Complexity Theory, and Complexity Theory then I encourage you to pick up and read {% cite Sisper2006 %} and {% cite Arora2009 %}.
Both texts will also discuss the Complexity Hierarchy and you'll learn plenty about $$P \stackrel{?}{=} NP$$ and other hard questions.
However, we're going to discuss a different kind of hierarchy.

Here is a list of complexity classes, in order of fastest to slowest:

$$
\mathcal{O}(1) \in
\mathcal{O}(\log(n)) \in
\mathcal{O}(n) \in
\mathcal{O}(n\log(n)) \in
\mathcal{O}(n^2) \in
\mathcal{O}(n^3) \in
\mathcal{O}(2^n) \in
\mathcal{O}(n!)$$

Each faster (or "smaller") complexity class can be said to be "in" any of the slower (or "larger") ones.
This is an absorption property of complexity classes, but the utility comes in determining the smallest such complexity class that your algorithm is "in".
With the smallest appropriate complexity class chosen you can compare it to other possible ones.
If your algorithm is $$\mathcal{O}(n^2)$$ but your partners is $$\mathcal{O}(n)$$, then after some vetting of correctness you should go with your partners approach.
Knowing this hierarchy gives you the freedom of easily choosing between potential algorithms to know which one is going to be fast enough.
Take a look at the plot below to get a better understanding of how these complexity classes scale.

![plots](/img/lectures/sigcomp/bigoplots.svg)

## Determining Time Complexity

Knowing the theory is important in order to apply it, but you also have know how to apply it.
Time complexity is the most important measurement because it is the most heavily constrained resource.
In the real world, especially on embedded systems, things like space complexity could become a much more important factor, but our target is the competitive programming scene.
Error complexity is incredibly important (almost more so than time complexity) in numerical computation.
Who cares how fast your algorithm is if it isn't approximately correct to some error tolerance?
These kinds of problems do show up in contests but we can usually rest easy just by using `double`, `long double`, and worst case by implementing our own ratio class.

The question remains, how do we determine complexity?

Consider the following three algorithms:

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;

int main() {
   int n = 1000;

   int acc1 = 0, acc2 = 0, acc3 = 0;
   for (int i = 0; i < n; ++i)
      for (int j = 0; j < n; ++j)
         ++acc1;

   for (int i = 0; i < n; ++i)
      for (int j = 0; j < n - i; ++j)
         ++acc2;

   for (int i = 0; i < n; ++i)
      for (int j = 0; j < floor(log(n)); ++j)
         ++acc3;

   cout << acc1 << " " << acc2 << " " << acc3 << endl;
}
{% endhighlight %}

There are three separate sections with two for-loops, one nested in the other.
What is the time complexity of each of these sections?
Play the graphic below to gain some insight:

<svg id="fig1" width="800" height="200"></svg>

The leftmost grid is doing $$n \times n$$ steps, the middle is doing about half as many steps as the leftmost, and the rightmost is doing $$n \times \log(n)$$ steps.
To represent the time complexity we would say the algorithms are $$\mathcal{O}(n^2)$$, $$\mathcal{O}(n^2)$$, and $$\mathcal{O}(n\log(n))$$ respectively.
It's true that the middle grid is taking a constant factor less steps, but remember that Big-O notation does not capture that constant multiplier.

A good rule for determining complexity is just counting nested loops.
If you have three nested loops that go from 0 to some variable(s) (let's say $$n$$, $$m$$, and $$q$$) then a safe first guess is $$\mathcal{O}(nmq)$$.
If $$n = \max(n, m, q)$$ then you could also express this as $$\mathcal{O}(n^3)$$.
While that kind of simplification to the largest growing variable might be helpful to convey intent in some cases, it can hurt you in others.

Consider the problem of finding the maximum element in an array of length $$n$$ for $$q$$ queries that define a sub-array.
Assuming the queries define a set of indices one approach is to scan from the leftmost to rightmost index and track the maximum value along the way.
Suppose the size of the array can be very large, but the number of queries (perhaps per second) is relatively small.
If we only need to do ten queries a second then a $$\mathcal{O}(nq)$$ approach might be perfectly fine.
However, an oversimplification to $$\mathcal{O}(n^2)$$ could trick us into thinking our algorithm isn't good enough when it might clearly be.

### Counting Principles
<div class="definition">
A \(\textit{permutation}\) of a sequence \(S\) is a reordering of its elements.
</div>

<div class="definition">
A \(\textit{permutation with repetition}\) or \(word\) of some alphabet is a ordered selection of \(n\) elements from a sequence or alphabet \(S\) where the same element may be selected arbitrarily many times to form a new sequence \(S'\).
</div>

<div class="definition">
A \(\textit{combination}\) is a selection of \(k\) distinct elements from a set \(S\) which form a subset of \(S\).
</div>

<div class="definition">
A \(\textit{combination with repetition}\) is a selection of \(k\) elements from a set \(S\) which form a multiset \(M\).
</div>

These are the four useful methods of counting that can be categorized easily and applied effectively to determine computational complexities.

|                 ||Ordered           ||Unordered
|                 ++------------------++-------------------
|**Repetition**   ||permutation w/ rep||combination w/ rep
|**No Repetition**||permutation       ||combination


If you encounter a counting problem that you can determine requires an ordering of the elements without repetition, then you know it's a permutation.

So how do we compute these?

A permutation of a sequence of length $$n$$ is $$n!$$ or $$n(n-1)(n-2)\cdots(2)(1)$$.
This can be seen by imagining we have $$n$$ empty spots in a queue.
The first spot can be selected from any of the available members of the original sequence.
Once selected, though, the second spot in the queue can only choose from $$n-1$$ members.
This process continues until there is one spot left, with only one member left.

A permutation of a sequence of length $$n$$ where you only wish to permute to a subsequence of length $$k$$, $$k \leq n$$ is $$\frac{n!}{(n-k)!}$$.
This can be called a $$\textit{k-permutation of n}$$.
A similar analogy works to motivate the formula, the divisor will remove the extra empty spaces that you are no longer considering.

A permutation with repetition of a sequence of length $$n$$ with $$k$$ distinct elements is $$k^n$$.
To understand this we can use the same visual analogy.
Imagine the line, except now when we select a member for the first spot, that member is still available for the second spot.
This means that every spot in our empty queue has $$k$$ potential members, giving the formula.

A combination of a set with $$n$$ elements of which $$k$$ are to be selected is $$\left(n \atop k\right) = \frac{n!}{k!(n-k)!}$$.
Generally when we speak about combinations we say *n choose k* and write it $$\left( n \atop k \right)$$.
This formula can be understood by using permutations as a way to construct unordered choice.
First, we must select a permutation of length $$k$$ from a sequence of length $$n$$.
Second, we must remove (or discount) any orderings of this sequence of length $$k$$.
Because a permutation of length $$k$$ has $$k!$$ orderings, we get our extra divisor.

A combination with repetition of a set with $$n$$ elements of which $$k$$ are to be selected is $$\left(\left( n \atop k \right)\right) = \left( {n + k - 1} \atop k\right)$$.
To motivate this formula, consider that we have $$k$$ indistinguishable balls.
We also have $$n-1$$ separators.
We are allowed to place each separator wherever we like in the sequence of balls.
We could place them all on the right, enclosing none of the balls, or intersperse them.
Once placed, we can few the enclosed balls between separators as the choice of what values those balls now map to.
There are $$n + k - 1$$ different positions (of separators and balls), of which we choose $$k$$ balls into various different positions and use the separators to fill in the rest.

Sometimes a problem will be glaringly obvious that it wants you to work with permutations of say a string.
Sometimes, you can just generate all the permutations via `next_permutation` in the C++ Standard Template Library and perform a complete search in $$\mathcal{O}(n!)$$.
However, that is for us to be considered just about the *worst* you could do.
If it works, it works, but that problem could also be conveying that you need a clever solution and a complete search of the permutations isn't going to cut it.

### Examples

Let's return to computing the Fibonacci sequence.
In the first code sample provided on this topic we used a recursive function to search down until we bottomed out at $$n = 0$$ or $$1$$ which returned $$1$$ and then unraveled the recursion back up.
For a given index of the Fibonacci sequence $$n$$, what is the time complexity of computing the nth Fibonacci number using this method?

There are two methods to go about this, one is a heuristic approach, the other is from a generating function.
Consider writing out a tree of execution.
First, you'll have $$Fib(n)$$ (assuming $$Fib$$ is our recursive function).
Then, one depth lower, you'll have $$Fib(n-1)$$ and $$Fib(n-2)$$.
Following that, you'll have $$Fib(n-2)$$, $$Fib(n-3)$$, $$Fib(n-3)$$, and $$Fib(n-4)$$.
There are two necessary observations to get at a heuristic time complexity.
The first observation is that the width of the tree is doubling at each successive depth.
The second observation is that the height of the tree is $$n$$.
This can be seen by the fact that the always-left recursive path is rooted at $$Fib(n)$$ and will recurse one step at a time from $$Fib(n)$$ to $$Fib(n-1)$$ to $$\cdots Fib(1)$$.
With these observations the number of nodes (and thus computations) is $$\mathcal{O}(2^n)$$.

There are a couple of lies though in the above approach.
The first lie is that the tree is complete.
If the tree is complete, then it is indeed the case that you have $$2^n - 1$$ nodes and thus the correct time complexity, but in our case there is no reason to believe that it is.
This gets back to a concept we discussed before, Big-O notation is about upper bounds, *but* we want to make those upper bounds as *sharp* as possible.
A *sharp* upper bound is also called the *least* upper bound, it is the complexity class that precisely describes the worst case performance where no other complexity class could still be an upper bound but be absorbed by it.
That is to say, if $$\mathcal{O}(f)$$ is a sharp upper bound, and $$\mathcal{O}(g)$$ is any other upper bound, then either $$\mathcal{O}(f) = \mathcal{O}(g)$$ or $$\mathcal{O}(f) \in \mathcal{O}(g)$$.

This heuristic reason is good enough in a contest setting most of the time, but as a matter of exposition, how can we do better?
Consider $$T(n)$$ to be a function that computes the time taken to compute $$Fib(n)$$.
Then, $$T(n) = T(n-1) + T(n-2) + O(1)$$.
The constant factor can be ignored, and we have a linear recurrence relation:
$$T_n = T_{n-1} + T_{n-2}$$.
Here is the trick.
A linear recurrence relation takes the following form: $$a_n = c_{n-1}a_{n-1} + c_{n-2}a_{n-2} + \cdots + c_{1}a_{1}$$ with $$c_i : \mathbb{R}$$ for $$0 < i < n$$.
Any linear recurrence relation can be solved by taking the following assumption: $$a_n = \alpha^n$$.
Where $$\alpha^n$$ is called a *generation function*, or sometimes an *ansatz*.
Plug in the generation function into the recurrence relation, simplify to a polynomial, solve for the roots, and then the answer is the sum of those $$\alpha$$ values (to the $$n$$th power) times constant multipliers (in general).
Quickly, here it is for the Fibonacci recurrence relation (which just so happens to be the $$T_n$$ recurrence relation as well):

$$T_n = T_{n-1} + T_{n-2}$$

$$\alpha^n = \alpha^{n-1} + \alpha^{n-2}$$

$$\alpha^2 = \alpha + 1$$

$$\alpha^2 - \alpha - 1 = 0$$

$$\alpha = \frac{1 + \sqrt{5}}{2}, \frac{1 - \sqrt{5}}{2}$$

$$T_n = c_1(\frac{1 + \sqrt{5}}{2})^n + c_2(\frac{1 - \sqrt{5}}{2})^n$$

From there, you can use the initial conditions $$T_0 = T_1 = 1$$ to determine the constant values.
However, Big-O notation doesn't care about constant factors so we can compute the time complexity using just this information, which is approximately $$\mathcal{O}(1.6^n)$$.
That's a lot of extra work just to confirm that the time complexity is exponential, but you learned something.
As an interesting aside, this approach works for linear ordinary differential equations, they just use a different generating function, $$e^{nx}$$.

Needless to say an exponential time complexity is horrible.
As you also know, we can do a lot better, what exactly happens in the second code sample?
As it turns out, you end up recomputing a lot of Fibonacci numbers in the recursive approach.
If we can have the machine "learn" or "remember" those values, then the time complexity to "recall" the values would be $$\mathcal{O}(1)$$.
If you imagine taking the always-left recursive path down the binary tree discussed before, but then memorize results on the way up, then you never end up taking any other path except the first node to realize you memorized it.
That means our time complexity is $$\mathcal{O}(n)$$ for the second code sample.
An incredible improvement, and with the aid of Big-O notation you can see precisely why.

As a next example let's use a problem from [Codeforces](http://codeforces.com).
The problem will be [Lucky Numbers](http://codeforces.com/problemset/problem/630/C).
Here is a brief description:

A new office has its doors numbered with lucky numbers.
A lucky number is a number with only 7 or 8 as a digit.
A doorplate on an office door can only hold $$n$$ digits.
What is the maximum number of office doors, assuming they are all lucky numbers, that the new office can have?
The input is one number, $$n$$ ($$1 \leq n \leq 55$$), the output should be one number, the maximum number of offices.
The problem must be solved in less than half a second with less than 64 megabytes of space used.

A first naive approach could be the following:
Generate all the lucky numbers in lexicographical order until you reach a number whose digit length is greater than $$n$$, output the total count.

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
typedef long long i64;

i64 gen(int n) {
   i64 result = 0;
   for (int i = 0; i <= n; ++i) {
      vector<int> v(n, 7);
      for (int j = 0, k = v.size() - 1; j < i; ++j, --k) {
         v[k] = 8;
      }
      do ++result;
      while (next_permutation(v.begin(), v.end()));
   }
   return result;
}

int main() {
   i64 n, result = 0;
   cin >> n;
   for (int i = 1; i <= n; ++i) {
      result += gen(i);
   }
   cout << result << endl;
}
{% endhighlight %}

You may have had trouble coming up with the actual implementation for the solution yourself.
That's fine, we're more interested in time complexity, but take a good look at the above solution if you want to really grasp what it's doing.
It turns out you're computing all the permutations of length $$1, \cdots, n$$ with repeated entries.
That means we're dealing with a permutation with repetitions.
If you try to run the above code on anything above 30 you'll notice that it takes much longer than half a second.
If we use our counting principles then we can quickly see that the time complexity for this algorithm is $$\mathcal{O}(2^n)$$, exponential.

That's no good, how can we do better?
Well, as it turns out the problem is only interested in *counting* the number of permutations with repetition.
When we computed the time complexity, we were doing just that (with some hand waving of lower order terms).
It turns out that for a word of length $$n$$ with two possible letters the number of permutations is $$2^n$$, and for a word of length $$n-1$$ it's $$2^{n-1}$$, and so on.
With this observation, we can come up with a new solution that solves the problem in $$\mathcal{O}(n)$$ instead:

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
typedef long long i64;

int main() {
   i64 n, result = 0;
   cin >> n;
   for (i64 i = 1, pow2 = 2; i <= n; ++i, pow2 = pow2 << 1) {
      result += pow2;
   }
   cout << result << endl;
}
{% endhighlight %}

We just add powers of two to the result until we hit the length of the string.

## Heuristics Using Problem Bounds
Big-O notation offers us a powerful way to determine time complexity at scale, and with the constant factor we can do decently well at lower values as well.
However, in a competitive setting, there is additional information which is crucial in determining if your solution will work.
Almost every problem will incorporate some kind of variable bound.
Whether it's on the size of an array, the number of vertices, or some other variable described in the problem.

Consider the following problem:
Compute the sum from $$1$$ to $$n$$ and output that sum modulo $$2^{19} - 1$$ in less than one second, where $$2 \leq n \leq 10^{10}$$.

Let's try a naive solution:
{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
unsigned long long modulo = (1 << 19) - 1LL;
int main() {
   unsigned long long n;
   cin >> n;
   unsigned long long result = 0LL;
   for (unsigned long long i = 1LL; i <= n; ++i) {
     result = (result + i) % modulo;
   }
   cout << result << endl;
}
{% endhighlight %}

A single for loop, a cool $$\mathcal{O}(n)$$ solution!
Except it's way too slow.
We can see this by using the highest bound on $$n$$, $$10^{10}$$.
We use the upper bound as a heuristic for how many operations will be executed.
A general rule is that we can get away with two to three million operations.
Any more operations and you're pushing your luck.
Of course, this is a broad generalization of the reality, and if your constant factor is reducing an eight million operation count worst case down to two million, then things just might work out.

We can improve our algorithm by using an $$\mathcal{O}(1)$$ algorithm below, take a look and see if it makes sense.

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
unsigned long long modulo = (1 << 19) - 1LL;
int main() {
   unsigned long long n;
   cin >> n;
   unsigned long long left = n, right = n + 1LL;
   if (left % 2LL == 0) left /= 2LL; else right /= 2LL;
   unsigned long long result = ((left % modulo) * (right % modulo)) % modulo;
   cout << result << endl;
}
{% endhighlight %}

Here is another example.
For $$q$$ queries, print the $$k$$th permutation of a given ordered string of length $$n$$ in less than two seconds, where $$1 \leq q \leq 1000$$, $$1 \leq n \leq 9$$.

One solution is to generate all the permutations, store them in memory, and then print them out for each query.
Hold on, though, that approach would be $$\mathcal{O}(n! + q)$$, the worst time complexity we know of!
The unfortunate competitor might immediately dismiss the naive solution and move on to trying to figure something else out.
In reality, the naive solution is perfectly acceptable.
Using the worst bound, $$n = 9$$, we have $$9! = 362880$$, well under a million.
It should be noted that recomputing the permutation for every query is $$\mathcal{O}(qn!)$$, or $$1000(9!) = 362880000$$, about three hundred million.

Try the below solution out for yourself, the input is assumed to be two numbers $$n$$ then $$q$$, a lexicographically ordered string, and then $$q$$ numbers that are smaller than $$n$$.

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;

map<int, string> memo;
int main() {
   int n, q, k = 0;
   cin >> n >> q;
   string s;
   cin >> s;
   memo[k] = s;
   while (next_permutation(s.begin(), s.end())) {
      memo[++k] = s;
   }
   for (int i = 0; i < q; ++i) {
      int qk;
      cin >> qk;
      cout << memo[qk] << endl;
   }
}
{% endhighlight %}

## Final Remarks

Hopefully after this you can agree that Big-O notation is a valuable tool in understanding the cost of a particular algorithm.
We didn't discuss space complexity but all of the same principles apply, you just measure space instead of time.
Remember that finding a solution at all is always the first step, don't throw something out immediately because you're quick on the trigger to know it's too slow.
Slow solutions can still solve a problem within the time and space constraints.
However, also remember that once you have that slow solution, you can use these tools and techniques to know that it *is* too slow before wasting time and getting a `Time Limit Exceeded`.
Ultimately that is the point, being able to make quick and powerful judgments about potential solutions so that you can make better use of your development time, as well as your computation time.


## References

{% bibliography %}

<script>
var paper = Snap("#fig1");

var fbx = 660; var fby = 80;
var bbx = 600; var bby = 80;
var sbx = 610; var sby = 80;
var forward_pressed = 0; var backward_pressed = 0;
var forward_button = paper.polygon([fbx, fby, fbx, fby + 40, fbx + 25, fby + 20])
var backward_button = paper.polygon([bbx, bby, bbx - 25, bby + 20, bbx, bby + 40])
var stop_button = paper.polygon(
   [sbx, sby, sbx + 40, sby, sbx + 40, sby + 40, sbx, sby + 40])
var set = Snap([]);

var data = [];
var n = 8;
var speed = 250;
var idx = 0;

paper.text(25, 50 + 60, "n");
paper.text(240 - 25, 50 + 60, "n");
paper.text(430 - 25, 50 + 60, "n");
paper.text(100, 35, "n");
paper.text(240 + 40, 35, "n - i");
paper.text(430 + 35 , 35, "log(n)");

for (i = 0; i < n; ++i)
   for (j = 0; j < n; ++j)
      set.push(paper.circle(50 + 15*j, 50 + 15*i, 5));
for (i = 0; i < n; ++i)
   for (j = 0; j < n; ++ j)
      set.push(paper.circle(240 + 15*j, 50 + 15*i, 5));
for (i = 0; i < n; ++i)
   for (j = 0; j < n; ++ j)
      set.push(paper.circle(430 + 15*j, 50 + 15*i, 5));

var tmp_frame = [];
for (k = 0; k < 3; ++k) {
   for (i = 0; i < n; ++i) {
      for (j = 0; j < n; ++j) {
         tmp_frame.push([{fill: '#000000'}, speed]);
      }
   }
}
tmp_frame[tmp_frame.length - 1].push(function() { loop(); });
data.push(tmp_frame);

for (i = 0; i < n; ++i) {
   for (j = 0; j < n; ++j) {
      var frame = [];
      var k = i*n + j;

      var tmp = 0;
      for (u = 0; u < n; ++u) {
         for (v = 0; v < n; ++v) {
            if (tmp > k)
               frame.push([{fill: '#000000'}, speed]);
            else
               frame.push([{fill: '#bada55'}, speed]);
            ++tmp;
         }
      }

      tmp = 0;
      for (u = 0; u < n; ++u) {
         for (v = 0; v < n - u; ++v) {
            if (tmp > k)
               frame.push([{fill: '#000000'}, speed]);
            else
               frame.push([{fill: '#bada55'}, speed]);
            ++tmp;
         }
         for (v = n - u; v < n; ++v) {
            frame.push([{fill: '#000000'}, speed]);
         }
      }

      tmp = 0;
      for (u = 0; u < n; ++u) {
         var ln = Math.floor(Math.log(n));
         for (v = 0; v < ln; ++v) {
            if (tmp > k)
               frame.push([{fill: '#000000'}, speed]);
            else
               frame.push([{fill: '#bada55'}, speed]);
            ++tmp;
         }
         for (v = ln; v < n; ++v) {
            frame.push([{fill: '#000000'}, speed]);
         }
      }

      frame[frame.length - 1].push(function() { loop(); });
      data.push(frame);
   }
}

var loop = function() {
   if (forward_pressed != 0 && idx < n*n)
      set.animate.apply(set, data[++idx]);
   else if (backward_pressed != 0 && idx > 0)
      set.animate.apply(set, data[--idx]);
};

forward_button.click(function(event) {
      if ((idx == 0 || backward_pressed == 0) && forward_pressed == 0)
         set.animate.apply(set, data[idx]);
      forward_pressed = 1;
      backward_pressed = 0;
   })

backward_button.click(function(event) {
      if ((idx == n*n || forward_pressed == 0) && backward_pressed == 0)
         set.animate.apply(set, data[idx]);
      forward_pressed = 0;
      backward_pressed = 1;
   })

stop_button.click(function(event) {
      backward_pressed = 0;
      forward_pressed = 0;
   })


</script>
