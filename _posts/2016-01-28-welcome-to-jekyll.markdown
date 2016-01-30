---
layout: post
title:  "Test Post"
date:   2016-01-28 23:18:40 -0500
categories: Test Post
---
This is a test post.

{% highlight c++ %}
void foo();

int main()
{
   typedef std::complex<long double> c64;
   typedef std::tuple<c64, c64, c64> triple;
   triple t = make_tuple(std::polar(1.0, 2.0), c64(1, 2), c64(0, 0));
   int x, y, z;
   foo();
   return 0;
}
{% endhighlight %}

$$
\begin{equation}
   \int_{0}^{\infty} \exp^x dx
\end{equation}
$$

$$
\begin{align*}
  & \phi(x,y) = \phi \left(\sum_{i=1}^n x_ie_i, \sum_{j=1}^n y_je_j \right)
  = \sum_{i=1}^n \sum_{j=1}^n x_i y_j \phi(e_i, e_j) = \\
  & (x_1, \ldots, x_n) \left( \begin{array}{ccc}
      \phi(e_1, e_1) & \cdots & \phi(e_1, e_n) \\
      \vdots & \ddots & \vdots \\
      \phi(e_n, e_1) & \cdots & \phi(e_n, e_n)
    \end{array} \right)
  \left( \begin{array}{c}
      y_1 \\
      \vdots \\
      y_n
    \end{array} \right)
\end{align*}
$$
