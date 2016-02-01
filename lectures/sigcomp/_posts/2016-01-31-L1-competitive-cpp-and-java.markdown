---
layout: post
title:  "Using C++ and Java for Competitive Programming"
date:   2016-01-31 01:18:40 -0500
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

If you need a collection of key-value pairs for two heterogeneous types `Key` and `Value` then you want a `map`.
Under the hood a `map` is most likely a balanced tree (not unlike a `set`).
This means insertion, deletion, and search are going to have a similiar time complexity of $$\mathcal{O}(\log(n))$$.
One benefit of an STL `map` is the overloaded index operator:

{% highlight c++ %}
#include <bits/stdc++.h>
int main() {
   using namespace std;
   map<string, string> dictionary;
   string definition = "Name usually given to a boy or powerful wizard.";
   dictionary["Albus"] = definition;
   assert(
      equal(definition.begin(), definition.end(), dictionary["Albus"].begin())
   );
}
{% endhighlight %}

Having an index operator leads to more intuitive and often faster code, especially if your mapping is mostly from value-type to value-type.
A trick with `map` is using them as dynamically growing grids or spaces.
It's rare, but there may be a problem were initializing a grid statically will eat too much memory but the actual cells you care about are significantly less.
Consider this:

{% highlight c++ %}
#include <bits/stdc++.h>
int main() {
   using namespace std;
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

A `priority_queue` gives the largest element by the default ordering of the template argument.
This ordering can be changed by giving a different comparison function in the template arguments or in the constructor.
The benefit of a `priority_queue` is $$\mathcal{O}(1)$$ extraction of the largest element with respect to the ordering relation.
However, insertion and extraction (of other elements) from the queue are still just $$\mathcal{O}(log(n))$$ time complexity.
The trade off is that you can only extract the largest element (in the STL implementation), and you can't iterate over the elements.
All the same, if you're using a `priority_queue` you shouldn't want to do either of those things.
The idea is to process the largest element in the queue, perhaps while additional elements are being added until some condition is meant.
A classical use case for a priority_queue is implementing Dijkstras, were you want to greedily take the lowest cost path available to you.
To switch `priority_queue` from a largest element to lowest element is easy:

{% highlight c++ %}
#include <bits/stdc++.h>
int main() {
   using namespace std;
   // Template arguemnts are: value type, container type, comparison type
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

An `unordered_map` is much like a normal `map` except it's elements are not guaranteed to be ordered on traversal.
In reality, under the hood a `map` is most likely a balanced tree, an `unodered_map` is some kind of hash map.
With a hash map, `unordered_map` gives us on average constant time complexity for search, insertion, and deletion of elements.
You can do all the same things with `unordered_map` that you could with `map` but if you don't care much for sorted elements, you think using `map` itself is your bottleneck, and you have access to C++11, then try `unordered_map`.
It will probably be a very rare occurrence to both need and have it be available.

## C++ Standard Template Library Algorithms

Data structures are the ways in which we take data in and represent it.
A lot of data structures have member functions for access, search, insertion, and deletion of this data.
The STL also provides a very useful algorithm library for manipulation, transformation, comparison, and other operations on iterator ranges.
Just quickly, an iterator range is something almost all STL data structures implement (`priority_queue` proper being an exception, but you can use it's underlying container if you want).
To interface with many algorithms you have to use the data structure `.begin()` and `.end()` member functions which define two iterators that form a range over the data structure.
We'll get more into the specifics of ranges defined by two iterators later.

### Fill and Copy

Two simple algorithms that you might find your using on occasion are `fill` and `copy`.
They do precisely what you might expect: `fill` sets every value in a range to the supplied value, and `copy` copies one range to another.

Example:
{% highlight c++ %}
#include <bits/stdc++.h>
const int N = 100001;
int dp[N];
int main() {
   using namespace std;
   vector<int> x(N);
   fill(dp, dp + N, 0);
   fill(x.begin(), x.end(), 2);
   copy(x.begin(), x.end(), dp);
   assert(equal(x.begin(), x.end(), dp));
}
{% endhighlight %}

`fill` in particular is a good substitute for `memset` or writing the boilerplate of a for loop to set all the elements in a range.
If you think writing a for loop is quicker or easier than a `fill` or `copy` call then go for it, it probably wont matter performance wise.
However, you should take note that `fill` and `copy` can be optimized under the hood to be faster than your hand written for loop.

### Reverse

Another short and sweet algorithm is `reverse`. It's not terribly common to need to reverse a range, but when it does come up that you have to reverse that string and you can't just call `.reverse()` a certain kind of anger boils inside.

Enter `reverse`, a simple algorithm that will work on _any_ range, not just your strings:

{% highlight c++ %}
#include <bits/stdc++.h>
int main() {
   using namespace std;
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
The actual sorts that implement these algorithms are irrelevant, as they're almost definitely faster than an sorting algorithm you're going to implement (with the exception of an $$\mathcal{O}(n)$$ radix sort or similar).
If you don't know a lot of sorting algorithms, you do know what it means to sort something, so the only detail left is what's the difference between stable and not?
A stable sort will preserve the relative position of equal elements.
If I want to sort `{1, 2(1), 3, 2(2)}` (with parenthesis added for clarification), a unstable sort could give me `{1, 2(2), 2(1), 3}` but a stable sort will always give me `{1, 2(1), 2(2), 3}`.
Note that this has nothing to do with extra information about both of the twos in the above example, it's only preserving it's relative position in the unsorted array.
Not knowing when to use a `stable_sort` in a contest setting can be the difference between never getting that easy sorting problem and solving it instantly.
If relative position matters (e.g. with `pair`s sorting on the first element only) then *use stable_sort*.

Simple example:

{% highlight c++ %}
#include <bits/stdc++.h>
int main() {
   using namespace std;
   vector<int> v = {2, 3, 1, 6, 5, 4};
   vector<int> answer = {1, 2, 3, 4, 5, 6};
   sort(v.begin(), v.end());
   assert(equal(v.begin(), v.end(), answer.begin()));
}
{% endhighlight %}

Sorting an array is always relative to some order operating.
If you're only sorting value types than this is fine, worst case scenario you `reverse` the range once to get the ordering you want.
However, you might need to sort something that doesn't already have an ordering relation.
`sort` allows you to give it a comparison function to handle these cases:

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

Example:
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
Not that it's particularly complicated, but when a problem requires you to iterate through all the permutations of a string you might waste more time deriving how to do that in lexicographical order than solving the problem.
Enter `next_permutation` and `prev_permutation`. Permutations, like sorts, require an order relation in order to make sense.
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
`next_permutation` doesn't wrap around, it goes from the current state to the next lexicographical state.

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


### GregorianCalendar

qwer


### Geometry

qwer


### Regex

qwer


## Final Tips

qwer
