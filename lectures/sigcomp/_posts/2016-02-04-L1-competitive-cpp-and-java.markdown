---
layout: post
title:  "Using C++ and Java for Competitive Programming"
date:   2016-02-04 02:20:00 -0500
permalink: /:categories/:title.html
---

- C++ Standard Template Library Data Structures
- C++ Standard Template Library Algorithms
- Understanding Iterators and Using the STL
- C++11
- General C++ Style
- IO Performance
- Java
- Final Tips
{:toc}

## C++ Standard Template Library Data Structures

There are several useful data structures to know and understand from the Standard Template Library (STL).
To name a few: `pair`, `tuple` (C++11), `vector`, `set`, `map`, `priority_queue`, and `unordered_map` (C++11).

### Pairs and Tuples

`pair` and `tuple` (C++11) can be used to join two or more heterogeneous types together.
Each value inside the structure can be accessed by member variables, or with `get<unsigned int>(tuple<...> t)` (C++11).
It is more or less a style choice to use `pair` and `tuple` over custom structs.

Example (C++11):

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
int main() {
   pair<int, int> a = make_pair(1, 2);
   int x, y;
   tie(x, y) = a;
   assert(a.first == x);
   assert(a.second == y);

   tuple<pair<int, int>, int> t = make_tuple(a, 2);
   assert(a.first == get<0>(get<0>(t)));
   assert(a.second == get<1>(get<0>(t)));
}
{% endhighlight %}

The `tuple` type is only available with C++11, so if C++11 is not allowed you'll have to emulate tuples with your own struct:

{% highlight c++ %}
template<typename First, typename Second, typename Third>
struct triple {
   First first;
   Second second;
   Third third;
}
{% endhighlight %}

A small amount of template programming can go a long way in a contest setting, but if you over do it you'll pay a hefty price in the compile log.
The above code snippet will work perfect assuming `First`, `Second`, and `Third` are Plain ol' Data (POD) or value types like `int`, `long long`, etc.
In a competitive setting we're usually working with value types anyway, but if you need to work with more complicated types, just make a dedicated struct.

### Containers

STL containers are useful for their properties and in a setting where you want to dynamically grow a data structure.
Static data is better off as a static array because of the bound information available in the problem.
However, it is still good to know the STL data structures when you inevitably encounter a problem that has you remove data or shrink and grow the data dynamically.

#### Vector

A `vector` should be considered the dynamic array. You should never bother using a pointer, allocating space yourself, and then worrying about deleting it.
Repeat after me, if you don't know what to use to store data, use a `vector`.

A `vector` can be thought of as a contiguous collection of data in memory.
That means if you add data to a vector which then requires more space than its originally allocated size then it has to copy all of its data to a newly allocated array in memory.
This sounds slow, but in practice we know about how much data the vector is going to contain, and it is clever about how much additional space it is going to take if it has to regrow to prevent excessive copies or moves.

Thus, we can think of a `vector` as having $$\mathcal{O}(1)$$ insertion and index time complexity.
Deleting from a `vector` is more complicated.
If you are consistently deleting elements, a `vector` might start to be a poor choice.

Example:

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
int main() {
   vector<int> v; // Empty vector
   v.push_back(1);
   v.push_back(2);
   vector<int> w(2); // Two uninitialized elements
   w[0] = 1;
   w[1] = 2;
   assert(equal(v.begin(), v.end(), w.begin()));
}
{% endhighlight %}

#### Set

A `set` is designed to emulate a mathematical set, or a collection of unique values.
Under the hood a set is really a tree and a useful benefit is that an iterator over a set will be a sorted collection.

We should choose a `set` either when the data conceptually matches our idea of a mathematical set or we want to keep a dynamically changing collection of sorted values.
Because of the nature of a `set` the insertion, search, and deletion time complexities are all $$\mathcal{O}(\log(n))$$.

Example (C++11):

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
int main() {
   set<int> s;
   vector<int> v = {1, 1, 2, 3, 4, 5, 5, 6}; // C++11 Initializer List
   for (int i : v)
      s.insert(i);
   for (int i : v)
      assert(s.count(i) == 1); // Can only have one unique element
}
{% endhighlight %}

#### Map

If you need a collection of key-value pairs for two heterogeneous types `Key` and `Value` then you want a `map`.
Under the hood a `map` is most likely a balanced tree (not unlike a `set`).
This means insertion, deletion, and search are going to have a similar time complexity of $$\mathcal{O}(\log(n))$$.
One benefit of an STL `map` is the overloaded index operator:

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
int main() {
   map<string, string> dictionary;
   string definition = "Name usually given to a boy or powerful wizard.";
   dictionary["Albus"] = definition;
   assert(
      equal(definition.begin(), definition.end(), dictionary["Albus"].begin())
   );
}
{% endhighlight %}

Having an index operator leads to more intuitive and often easier to read code, especially if your mapping is mostly from value type to value type.
A trick with `map` is using them as dynamically growing grids or spaces.
It's rare, but there may be a problem were initializing a grid statically would eat too much memory but there is a significantly smaller amount of cells you care about.

Consider this (C++11):

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
int main() {
   // The first template argument is the key, the second is the value.
   // Thus we have a map from ints to another map from ints to ints.
   // This forms an "empty" grid which can be filled in dynamically.
   map<int, map<int, int> > grid;
   grid[0][1] = 6;
   grid[1002][6] = 2;
   typedef map<int, map<int, int> >::iterator iter;
   typedef map<int, int>::iterator subiter;
   for (iter it = grid.begin(); it != grid.end(); ++it)
      for (subiter jt = it->second.begin(); jt != it->second.end(); ++jt)
         cout << it->first << " " << jt->first << " " << jt->second << endl;

   // Or with C++11
   for (auto sp : grid)
      for (auto p : sp.second)
         cout << sp.first << " " << p.first << " " << p.second << endl;
}
{% endhighlight %}

If you're more comfortable with using a `map` instead of a static array then go for it.
Most of the time you can get away with it.
However, if you want the most performant code in a competitive setting, you should use static or cache-friendly data structures whenever possible.

#### Priority Queue

A `priority_queue` gives the largest element by the default order relation of the template argument.
This order relation can be changed by giving a different comparison function in the template arguments or in the constructor.
The benefit of a `priority_queue` is $$\mathcal{O}(1)$$ search for the largest element with respect to the order relation.
However, insertion and extraction (of all elements, including the largest) from the queue is still $$\mathcal{O}(log(n))$$ time complexity.
With a `priority_queue` you can only extract the largest element (in the STL implementation), and you can't iterate over the elements.
All the same, if you're using a `priority_queue` you shouldn't want to extract anything but the largest element.
The idea is to process the largest element in the queue, perhaps while additional elements are being added, until some condition is meant.
A classic use case for a `priority_queue` is implementing Dijkstras were you want to greedily take the lowest cost path available to you.
To switch `priority_queue` from a largest element to lowest element is easy (C++11):

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
int main() {
   // Template arguemnts are: value type, container type, order relation
   priority_queue<int, vector<int>, greater<int> > q;

   vector<int> values = {5, 4, 3, 2, 1};
   for (int x : values) q.push(x);
   vector<int> answer = {1, 2, 3, 4, 5};
   vector<int> a;
   while (not q.empty()) a.push_back(q.top()), q.pop();

   assert(equal(a.begin(), a.end(), answer.begin()));
}
{% endhighlight %}

#### Unordered Map

An `unordered_map` is much like a normal `map` except its elements are not guaranteed to be ordered on traversal.
In reality, under the hood a `map` is most likely a balanced tree, an `unodered_map` is most likely some kind of hash map.
With a hash map, `unordered_map` gives us on average constant time complexity for search, insertion, and deletion of elements.
You can do all the same things with `unordered_map` that you could with `map` but if you don't care much for sorted elements, you think using `map` itself is your bottleneck, and you have access to C++11, then try `unordered_map`.
It will probably be a very rare occurrence to both need and have it be available.

## C++ Standard Template Library Algorithms

Data structures are the ways in which we represent and store collections of data.
A lot of data structures have member functions for access, search, insertion, and deletion of this data.
The STL also provides a very useful algorithm library for manipulation, transformation, comparison, and other operations on iterator ranges.
Just quickly, an iterator range is something almost all STL data structures implement (`priority_queue` proper being an exception, but you can use it's underlying container if you want).
To interface with many algorithms you have to use the data structure `.begin()` and `.end()` member functions which define two iterators that form a range over the data structure.
We'll get more into the specifics of ranges defined by two iterators later.

### Fill and Copy

Two simple algorithms that you might find yourself using on occasion are `fill` and `copy`.
They do precisely what you might expect: `fill` sets every value in a range to the supplied value, and `copy` copies one range to another.

Example:

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
const int N = 100001;
int dp[N];
int main() {
   vector<int> x(N);
   fill(dp, dp + N, 0);
   fill(x.begin(), x.end(), 2);
   copy(x.begin(), x.end(), dp);
   assert(equal(x.begin(), x.end(), dp));
}
{% endhighlight %}

`fill` in particular is a good substitute for writing the boilerplate of a for loop to set all the elements in a range.
If you think writing a for loop is quicker or easier than a `fill` or `copy` call then go for it, it probably wont matter performance wise.
However, you should take note that `fill` and `copy` can be optimized under the hood to be faster than your hand written for loop.
For instance, fill could be specialized on `char` to just `memset` instead of iterating over the range.

### Reverse

Another short and sweet algorithm is `reverse`.
It's not terribly common to need to reverse a range, but when it does come up that you have to reverse a string and you can't just call `.reverse()` a certain kind of anger boils inside.

Enter `reverse`, a simple algorithm that will work on _any_ range, not just your strings:

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
int main() {
   string x = "This is a string.";
   string answer = ".gnirts a si sihT";
   string rx(x.size(), ' ');
   reverse_copy(x.begin(), x.end(), rx.begin()); // copy variant
   reverse(x.begin(), x.end());
   assert(equal(x.begin(), x.end(), answer.begin()));
   assert(equal(rx.begin(), rx.end(), answer.begin()));
}
{% endhighlight %}

### Sort and Stable Sort

Sorting is a very common problem, so much so that you probably know seven different sorting algorithms and yet the reality is that whenever you actually need to sort something you should never write the algorithm yourself.
Instead, use `sort` or `stable_sort`.
If you do know those seven different kinds of sorting algorithms then you can think of `sort` as your quick sort (hence the missing stable_ prefix), and `stable_sort` as your merge sort.
The actual sorts that implement these algorithms are irrelevant, as they're almost definitely faster than a sorting algorithm you're going to implement (with the exception of a $$\mathcal{O}(n)$$ radix sort or similar).
If you don't know a lot of sorting algorithms, you do know what it means to sort something, so the only detail left is what is the difference between stable and not?
A stable sort will preserve the relative position of equal elements.
If I want to sort `{1, 2(1), 3, 2(2)}` (with parentheses added for clarification), a unstable sort could give me `{1, 2(2), 2(1), 3}` but a stable sort will always give me `{1, 2(1), 2(2), 3}`.
Note that this has nothing to do with extra information about both of the twos in the above example, it's only preserving it's relative position in the unsorted array.
Not knowing when to use a `stable_sort` in a contest setting can be the difference between never getting that easy sorting problem and solving it instantly.
If relative position matters (e.g. with `pair`s sorting on the first element only) then *use* `stable_sort`.

Example (C++11):

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
int main() {
   vector<int> v = {2, 3, 1, 6, 5, 4};
   vector<int> answer = {1, 2, 3, 4, 5, 6};
   sort(v.begin(), v.end());
   assert(equal(v.begin(), v.end(), answer.begin()));
}
{% endhighlight %}

Sorting an array is always relative to some order relation.
If you're only sorting value types than this is fine, worst case scenario you `reverse` the range once to get the ordering you want.
However, you might need to sort something that doesn't already have an order relation.
`sort` allows you to give it a comparison function to handle these cases (C++11):

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
struct cmp {
   bool operator() (const pair<int, int> a, const pair<int, int> b) {
      return a.first < b.first;
   }
} cmp;

int main() {
   vector<pair<int, int>> v = { {1, 2}, {4, 2}, {4, 1}, {2, 3}, {1, 8} };
   vector<pair<int, int>> answer = { {1, 2}, {1, 8}, {2, 3}, {4, 2}, {4, 1} };

   stable_sort(v.begin(), v.end(), cmp);
   assert(equal(v.begin(), v.end(), answer.begin()));
}
{% endhighlight %}

### Max and Min Element

Finding a maximum and minimum element are fairly common problems in a competitive setting.
Like `fill`, `max_element` and `min_element` aren't going to win any awards with how complicated they are and yes you could just write the for loop yourself.
The same motivation applies though, they're quick, clean, and probably faster.

Example (C++11):

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
int main() {
   vector<int> v = { 2, 3, 1, 100, 2, 1000, 6, 10000, 2, 5};
   int answer1 = 10000, answer2 = 1;
   typedef vector<int>::iterator iter;
   iter M = max_element(v.begin(), v.end());
   iter m = min_element(v.begin(), v.end());
   // I don't use the dereference operator here because it breaks my markdown
   // highlighting.
   assert(answer1 == M[0] && answer2 == m[0]);
}
{% endhighlight %}

### Permutations

Iterating through a collection of permutations is not something most of learn how to do.
Not that it is particularly complicated, but when a problem requires you to iterate through all the permutations of a string you might waste more time deriving how to do that in lexicographical order than solving the problem.
Enter `next_permutation` and `prev_permutation`.
Permutations, like sorts, require an order relation to make sense.
Without getting into the weeds about lattices, partial orders, well orders, and the like, suffice to say we'll be permuting strings most of the time, so lexicographical will work just fine.

Example:

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
int main() {
   string s = "abcdefg";
   int pause, count = 1;
   do {
      cout << s << endl;
      if (count % 10 == 0)
      {
         cout << "continue?" << endl;
         cin >> pause;
      }
      ++count;
   } while (next_permutation(s.begin(), s.end()));
}
{% endhighlight %}

Notice that we ask for permutations until, well, there aren't any.
`next_permutation` returns a boolean telling us if there is in fact a next permutation.
Also note that we started with an ordered string, had we not started ordered we would not have seen every permutation.
`next_permutation` does not wrap around, it goes from the current state to the next lexicographical state.

## Understanding Iterators and Using the STL

An iterator in C++ for simplicity can be thought of as any object that supports increment (`++it`), dereference to a reference type (`decltype(*it) == it::reference`), and other miscellaneous construction, destruction, and swappable requirements.
For a competitive purpose the only thing we need to know and understand is that an iterator will give us the "next iterator" as well as a reference to the information it stores.
This reference information need not be a direct reference to what we perceive is the value type, as an example for `map<int, int>` we have `map<int, int>::iterator::reference == &pair<int, int>`.
This is because the iterator is returning all the information relative to it, i.e. the key-value pair stored in a map.
Although from the perspective of `map`, this *is* its value type.
Iterators in C++ are what in the future we'll just call a "Concept."
A C++ iterator is not an interface, an object inheriting from a class iterator, or anything of the sort.
It is merely a construct that meets the pre and post conditions which define the concept "Iterator."

Because of this distinction a useful realization is that pointers are iterators.
That means, the only thing we need to do to iterate over a contiguous range of memory is supply a pointer to the first memory address and the pointer to one past the last memory address.
"One past the last," is a common design choice in all of the STL.
Whenever you want to give a range to something in terms of two iterators (a begin and an end), you're always doing it in a half-closed range.
That means, if I have a range defined by $$a$$ and $$b$$, then the actual range that my algorithms should be working over is $$[a, b)$$.
Closed on the left, open on the right.

Example:

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
const int N = 101;
int values[N];

struct gen {
   int val;
   gen() : val(0) { }
   int operator() () { return ++val; }
} generator;

template<typename T>
struct display {
   void operator() (const T& x) { cout << x << " "; }
};

display<int> displayer;

int main() {
   generate(values, values + N, generator);
   for_each(values, values + N, displayer);
   cout << endl;
}
{% endhighlight %}


## C++11

In a contest setting it has, at least in the past, been rare to have C++11 support.
However, I imagine the times are changing and C++11 is going to become more and more available in contest settings (especially with the advent of python being available).
C++11 offers a couple of nice language features that can ease the pain of boilerplate, especially around iterators.
A competitor needs to keep his wits about him though and not rely on these features as a crutch, otherwise he might find himself without C++11 and needing to know how to write out the type of that `map<string, map<string, int> >` iterator and sub-iterator, as well as what they return and why.

### `auto` Keyword and New For Loop

One of the more useful language benefits is the `auto` keyword.
If you've ever worked in C#, `auto` is more or less your `var`.
It is type deduction at compile time, where the compiler will figure out (if it can) exactly what type is required for a certain expression without you having to write it out.

The new for loop expression is a "for each" loop.
It works particularly well in conjunction with the `auto` keyword.
The syntax is simple enough, instead of the boilerplate of defining your own iterator range, when it ought to stop, and how much to increment it, you tell the compiler you want to touch all the items in a container: `for (auto x : container) { ... }`.

To use the above example (C++11):

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
int main() {
   map<string, int> a1 = { {"b", 2}, {"c", 3} };
   map<string, int> a2 = { {"b", 4}, {"c", 5} };
   map<string, map<string, int>> m = { {"a", a1}, {"d", a2} };
   // pre C++11
   typedef map<string, map<string, int> >::iterator iter;
   typedef map<string, int>::iterator subiter;
   for (iter it = m.begin(); it != m.end(); ++it)
   {
      for (subiter sit = it->second.begin(); sit != it->second.end(); ++sit)
      {
         cout << it->first << " " << sit->first << " " << sit->second << endl;
      }
   }
   // post C++11
   for (auto v : m)
      for (auto x : v.second)
         cout << v.first << " " << x.first << " " << x.second << endl;
}
{% endhighlight %}

As a general rule `auto` should be used to save you time, not because you don't know what type you want.
However, if you *don't know* and auto helps you tease out what it is, or helps you get the solve, then no one is going to complain during the contest.
You'll get teased afterwards.

### Initializer Lists

An initializer list is that funny syntax you've seen me use in several prior examples.
It's the bracket notion with literals, e.g. `{1, 2, 3}`.
An initializer list is a convenient way to work with complicated shapes or just pairs of values.
Although a `make_pair(...)` isn't terribly difficult to do, you can also just `{...}` and throw it in.

Example (C++11):

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
int main() {
   map<int, int> m;
   map<int, int> answer = { {1, 2}, {3, 4}, {5, 6} };
   m.insert({1, 2});
   int x = 3, y = 4, z = 5;
   m.insert({x, y});
   m.insert({z, 6});
   assert(equal(m.begin(), m.end(), answer.begin()));
}
{% endhighlight %}

Initializer lists are hit or miss.
In the instances where they can be used they're often quite nice, but they're not always supported out of the box and have certain pitfalls.
You can think of an initializer list as just a range of items that a function call (which accepts an initializer list) will iterate over and attempt to use.
Because of the generality of these algorithms you might run into problems were the compiler complains about requiring explicit construction from the sub-lists in say a `vector<tuple<...>>`.
In a contest setting it's a double edged sword which could lead to grieve with long compiler errors, but it can also speed up certain scenarios from needing `make_pair()` everywhere.
My advice is to try it out in a test program if you're not certain how it's going to behave.

### Lambdas

Lambdas are an addition to C++11 that should probably rarely be used in a contest setting.
However, there are times when you need a function to pass into a STL algorithm, like `generate` or `sort` that we've seen before, and whipping it up in a lambda can be faster than implementing a struct, overloading the call operator, and then going from there (basically a boilerplate lambda).

A lambda expression takes this full form: `[ *capture-list* ] ( *params* ) mutable *exception attribute* -> *return type* { *body* }`.
However, the entire *params* portion is optional, the `mutable` keyword with *exception attribute* is optional, and the *return type* with it's arrow `->` are also optional.
These parts aren't independently optional, but the only bits you need to worry about is `mutable` and *return type*.
If you want to mutate, you need to have a parameter list and return.
If you want to return, you need to have a parameter list.

The capture list in the lambda expression is to capture variables in the parent scope of the expression that aren't going to be passed in as parameters.
You could just not capture anything and pass all needed values as parameters, but that would be a bother.
The capture list can capture by value or by reference, e.g. `[a, &b]` capturing `a` by value and `b` by reference.
You can automatically capture every variable available to you by reference or by value with `[&]` and `[=]` respectively.
Asides from that, it's like writing any other kind of function, although you need to end the expression with a semicolon.

Example (C++11):

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
int main() {
   vector<int> v(100);
   int val = 0;
   auto generator = [&val] () -> int { return ++val; };
   auto displayer = [] (int x) { cout << x << " "; };
   generate(v.begin(), v.end(), generator);
   for_each(v.begin(), v.end(), displayer);
   cout << endl;
}
{% endhighlight %}

### Regex

A double-edged sword if there ever was one, regex is that fancy regular language with back reference extras that everyone should love and hate equally.
Especially in a contest setting.
There are definitely problems were regex is undeniably your friend, so you spent the five minutes getting the expression correct and now the problem is just solved.
However, regex can often be thought of as a one size fits all magic bullet.
That alone is bad enough, but coupled with overconfidence and you've got wasted time, effort, and a solution that's probably way too slow.

One of the biggest problems with regex solutions is not being able to grasp the runtime complexity as easily as other solutions.
The runtime complexity is dependent on the implementation under the hood and the features of that implementation you decide to use.
When you write a regex expression, you're writing a little program in an esoteric language, that makes things harder to understand, harder to implement, and significantly more painful when you discover you don't actually know what the problem is asking.

With all of these downsides, I'll remind you that sometimes regex is just what the doctor ordered.
Not commonly, but sometimes.
There is too much detail that needs to be understood about regex for me to elucidate it in an introduction, but suffice to say it is present in C++11, and if you know what you're doing don't be too afraid to use it.

## General C++ Style

There are a view style guidelines what will help you when you're programming in a competitive setting.
If you've analyzed the code snippets in this post already you may have noticed a couple of interesting things.
The first is the include header.
In every example there is only one include header, `#include <bits/std++.h>`.
This is a compiler specific header that will include all of the STL headers for you.
Its uses outside of a competitive setting are for pre-compiled headers, but for us it's a quick way to get everything we are going to want.
It should be noted again that this header is not part of the standard, and it's possible that a compiler wont support it.
Most of the time a contest setting is using some variant of gcc in which case it's very likely the header will be supported.

The next tidbit is `using namespace std;` which comes immediately after.
This statement is to prevent the need to prefix every standard call with `std::`.
It's just a quick time saver to prevent those same five characters from appearing and reappearing.

A couple of final remarks on style.
Competitive problems almost always give a bounds on the input variables.
These bounds are guarantees and do not need to be checked.
More often than not someone brand new to competitive programming will add `if` statements attempting to confirm these bounds to make sure they're okay without needing to.
The reverse of that is using the information supplied by the bounds to initialize just enough memory in a convenient and cache efficient static array.
If you can do this: `int array[10001];` then you should.
Other minor details are that the `main` function does not need arguments or a `return 0;` statement at the end, although it does not hurt.


## IO Performance

Very rarely IO in a problem turns out to be the bottleneck of your solution.
There are two ways to go about correcting this if you ever suspect it to be an issue:

1. Use C-style IO, with scanf and printf for everything.
2. Unsync and untie C++ io streams from C io streams.

To go about the second method, you can just add this struct to the top of all of your solutions:

{% highlight c++ %}
struct iofix {
   ios_base::Init i;
   iofix() { cin.sync_with_stdio(0); cin.tie(0); }
} iofix;
{% endhighlight %}


## Java

C++ is my preferred language of choice for competitive programming.
That doesn't make Java any worse or any better, it can handle all of the aspects here and perform equally well in a contest setting.
That is of course not to say it's perfect, either.
It's just different, but there are some undeniable benefits to Java, and that's what this section is about.


### When to Bother

Switching from a language you're most comfortable in to a language that you might not have used in years is a big risk, especially in a high stress environment like the last hour of a contest with a problem on the line.
Being able to weigh the benefits for the rewards is the best way to make sure that the right call is made in that stressful moment.
Going with Java means you have to change paradigms to a language with garbage collection that forces object oriented design principles on you when you just want to write a bloody function.
Even worse, you're probably going to be working with an old version of Java and not have more of the useful features available to you.

All the same, if the problem you're tackling can be solved or greatly assisted by any of: `BigInteger`, `BigDecimal`, `LocalDate` (Java 8), `Line2D`, `Arc2D`, `Polygon`, or regex (and you don't have C++11), then you should probably choose Java.
All of these instances are quite rare, and all of them can be solved in C++ land with a little bit of know-how and careful planning.
Yet, they're all already there in Java, ready and waiting.


### BigInteger and BigDecimal

The arbitrary arithmetic helper classes `BigInteger` and `BigDecimal` in Java can outright solve some otherwise difficult math problems.
It is incredibly rare (verging on non-existent) for the intended solution to a problem to require arbitrary precision arithmetic.
There are however problems, like computing factorials, which can be "cheesed" with `BigInteger`.
There are also instances of testing primality of a large integers which can be "cheesed" with probabilistic algorithms (already present in `BigInteger`).
These are both risky prospects, because an astute and determined problem writer is either going to concede that these are proper solutions or guarantee they'll fail.
In the heat of the moment, though, if you don't know the correct solution, but you know how to solve it with these classes, then go for it.

Example (Java 7 or 8):

{% highlight java %}
import java.math.BigInteger;
class Test {
   public static void main(String[] args)
   {
      BigInteger factorial = new BigInteger("1");
      for (int i = 1; i < 1000; ++i)
      {
         factorial = factorial.multiply(new BigInteger("" + i));
      }
      System.out.println(factorial.toString());
   }
}
{% endhighlight %}

### LocalDate

A Gregorian calendar is the fancy name for the calendar that just about everyone across the world uses.
Just about as rarely as intentional arbitrary arithmetic problems, you'll get a problem that deals with large spans of time over a calendar year that expects you to handle all the little details.
This is arguably easier to handle in C++ if you already know some formulas to generate a calendar and manipulate it, but if you don't, you're probably out of luck.

Enter `LocalDate`, a concrete implementation of an every day calendar.
There are some hang ups to using this class, mostly being accustom to using it.
It's unlikely for anyone to expect you to memorize the Java `LocalDate` object and how to use it, so what you should expect is for it to show up in your reference material.
From there, you can figure out how exactly to use it and solve that quirky calendar problem without too much worry.

Example (Java 8):

{% highlight java %}
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
class Test {
   public static void main(String[] args)
   {
      LocalDate birthday = LocalDate.of(1990, 12, 10);
      LocalDate now = LocalDate.now();
      long years = ChronoUnit.YEARS.between(birthday, now);
      System.out.println(years); // Should be 25
   }
}
{% endhighlight %}

In the above example `ChronoUnit` is used to compute the years between two `LocalDate`s.
There are a couple helper classes in `java.time` and `java.time.temporal` that interact with `LocalDate` or other useful time abstractions.
Although we only touch on `LocalDate` here, it wouldn't hurt to explore these options.

### Geometry

Geometry is probably the best example of what can be gained from switching to Java.
Rarely is there an "easy" geometry problem that can't be solved with some quick math, but geometry problems can run the gambit from easy to impossible.
Throughout all possibilities, it's definitely nice not having to implement your own line class and intersect function.
If you've got a math guy with you who knows how to use `complex<T>` in C++ as a two dimensional vector and can derive the problem, then let him have it.
Otherwise, it can't hurt to switch over and utilize all those handy geometric objects and associated functions to get a solve on that otherwise time consuming geometry problem.

Example (Java 7 or 8):
{% highlight java %}
import java.awt.geom.Line2D;
import java.awt.geom.Line2D.Double;
class Test {
   public static void main(String[] args)
   {
      Line2D l1 = new Line2D.Double(0, 0, 1, 1);
      Line2D l2 = new Line2D.Double(0, 0, -1, 1);
      boolean ans = l1.intersectsLine(l2);
      assert ans;
   }
}
{% endhighlight %}

### Regex

Much like the section on C++11 regex, all the same dos and don'ts apply.
If you find yourself in need of a regex library, and also don't have C++11 available, then Java has come to the rescue.
I'll reiterate, make sure you know what you're doing.
Make sure you know what you're doing.
Make sure the problem *actually calls for regex* and you're not taking a sledge hammer to a screw.


## Final Tips

Breathe, relax, have fun, and make sure to print out and build a binder or some kind of reference material out of anything you know you're going to forget but will probably need.
In almost any off-line contest you're allowed any written material you can carry!
Make a template file with all of your headers, needed functions, macros, or what have you.
You don't have to make it instantly, but if there is a lull have someone work it out so you don't have to redo the work.
The template doesn't have to be just for C++ either, a quick and easy Java template can't hurt in a lull period either.

You should also take a look at the [C++ Reference](http://en.cppreference.com/w/) and [Java Reference](http://docs.oracle.com/javase/8/docs/api/).

My C++ template (as of today):

{% highlight c++ %}
#include <bits/stdc++.h>
using namespace std;
struct iofix
{
   ios_base::Init i;
   iofix() {
      cin.sync_with_stdio(0);
      cin.tie(0);
   }
} iofix;

typedef int i32;
typedef long long i64;
typedef unsigned int u32;
typedef unsigned long long u64;

int main()
{

   return 0;
}
{% endhighlight %}
