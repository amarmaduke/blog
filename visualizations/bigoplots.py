import numpy as np
from matplotlib import collections, transforms
import matplotlib.pyplot as plt
import math

x = np.linspace(.1, 10, 1000)
y_logn = [math.log(k) for k in x]
y_n = x;
y_nlogn = [k*math.log(k) for k in x]
y_n2 = [k*k for k in x]
y_2n = [pow(2,k) for k in x]
y_nfact = [math.gamma(k + 1) for k in x]

plt.style.use('ggplot')

fig, axes = plt.subplots(ncols = 3, nrows = 2)
ax1, ax2, ax3, ax4, ax5, ax6 = axes.ravel()

ax1.plot(x, y_logn)
ax1.set_ylim(0, 25)
ax1.set_ylabel('$\log(n)$', fontsize=16)

ax2.plot(x, y_n)
ax2.set_ylim(0, 25)
ax2.set_ylabel('$n$', fontsize=16)

ax3.plot(x, y_nlogn)
ax3.set_ylim(0, 25)
ax3.set_ylabel('$n\log(n)$', fontsize=16)

ax4.plot(x, y_n2)
ax4.set_ylim(0, 100)
ax4.set_ylabel('$n^2$', fontsize=16)

ax5.plot(x, y_2n)
ax5.set_ylim(0, 100)
ax5.set_ylabel('$2^n$', fontsize=16)

ax6.plot(x, y_nfact)
ax6.set_ylim(0, 100)
ax6.set_ylabel('$n!$', fontsize=16)

plt.tight_layout()
plt.savefig('bigoplots.svg', format='svg')
