---
layout: post
title:  "Using C++ and Java for Competitive Programming"
date:   2016-01-31 01:18:40 -0500
permalink: /:categories/:title.html
---

- C++ Data Structures
   - Pairs and Tuples
   - Containers
- C++ Standard Template Library
   - Fill and Copy
   - Reverse
   - Sort and Stable Sort
   - Max Heap
   - Max and Min Element
   - Permutations
- Understanding Iterators and Using the STL
- C++11
   - `auto` Keyword
   - Initializer Lists
   - Lambdas
   - Regex
- General C++ Style
- IO Performance
- Java
   - When to Bother
   - BigInteger and BigDecimal
   - GregorianCalendar
   - Geometry
   - Regex
- Final Tips
{:toc}

## C++ Data Structures

There are several useful data structures to know and understand from the Standard Template Library (STL).
They are `pair`, `tuple` (c++11), `vector`, `set`, `map`, `priority_queue`, and `unordered_map` (c++11).

### Pairs and Tuples

`pair` and `tuple` (c++11) can be used to join two or more heterogeneous types together.
Each value inside the structure can be accessed by member variables, or with `get<unsigned int>(tuple<T> t)` (c++11).
It is more or less a style choice to use `pair` and `tuple` over static areas if the type is homogeneous.
However, `pair` and `tuple` will be safer because of member access instead of pointer access.
Example:

{% highlight c++ %}
#include <bits/stdc++.h>
int main() {
   using namespace std;
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
The above code snippet will work perfect assuming `First`, `Second`, and `Third` are Plain ol' Data (POD) or value-types like `int`, `long long`, etc.
In a competitive setting we're usually working with value types anyway, but if you need to work with more complicated types, just make a dedicated struct.

### Containers

STL containers are useful for their properties and in a setting where you want to dynamically grow a data structure.
Static structures are better off as static arrays because of the bound information the problem gives.
However, it is still good to know the STL data structures when you inevitable encounter a problem that has you remove data or shrink and grow the container dynamically.

#### Vector

A `vector` should be considered the dynamic array. You should never bother using a pointer, allocating data yourself, and then worrying about deleting it.
Repeat after me, if you don't know what to use to store that data, use a `vector`.
The second step is to figure out what to use, and why you're choosing `vector` so often.

A `vector` can be thought of as a contiguous collection of data in memory.
This means that if you add data to the vector which is greater than it's originally allocated size, it has to copy all of it's data to a newly allocated array in memory.
This sounds slow, but in practice we know about how much data the vector is going to contain, and it's clever about how much additional data it's going to take if it has to regrow.

Thus, we can think of a `vector` as having $$\mathcal{O}(1)$$ insertion and index time complexity.
Deleting from a `vector` is more complicated.
If you are consistently deleting elements, a `vector` might start to be a poor choice.

Example usage:

{% highlight c++ %}
#include <bits/stdc++.h>
int main() {
   using namespace std;
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

We should choose a `set` either when we want to encapsulate some concept of uniqueness or we want to keep a dynamically changing collection of sorted values.
Because of the nature of a `set` the insertion, search, and deletion time complexities are all $$\mathcal{O}(\log(n))$$.

Example usage:

{% highlight c++ %}
#include <bits/stdc++.h>
int main() {
   using namespace std;
   set<int> s;
   vector<int> v = {1, 1, 2, 3, 4, 5, 5, 6}; // C++11 Initializer List
   for (int i : v)
      s.insert(i);
   for (int i : v)
      assert(s.count(i) == 1); // Can only have one unique element
}
{% endhighlight %}

#### Map

sdfsdf

#### Priority Queue

ppp

#### Unordered Map

afasdf

## C++ Standard Template Library

alsdfj

### Fill and Copy

qwer

### Reverse

qwer

### Sort and Stable Sort

qwer

### Max Heap

qwer


### Max and Min Element

qwer


### Permutations

qwer


## Understanding Iterators and Using the STL

qwer


## C++11

qwer


### `auto` Keyword

qwer


### Initializer Lists

qwer


### Lambdas

qwer


### Regex

qwer


## General C++ Style

qwer


## IO Performance

qwer


## Java

qwer


### When to Bother

qwer


### BigInteger and BigDecimal

qwer


### Gregorian Calendar

qwer


### Geometry

qwer


### Regex

qwer


## Final Tips

qwer
