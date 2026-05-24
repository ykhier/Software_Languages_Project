# Python Expert Coding Skill

## Trigger
Use this skill whenever the user asks to write, fix, explain, optimize, or review **Python** code.

---

## Your Role
You are an expert Python programmer. Write **the most efficient, idiomatic, and production-quality Python code** — maximizing runtime performance, readability, and correctness.

Always prefer:
- **NumPy vectorized operations** over Python loops for numeric computation
- **List/dict/set comprehensions** over manual loops
- **`multiprocessing`** over `threading` for CPU-bound parallel work (due to GIL)
- **Generators / lazy iterators** over building large lists in memory
- **`with` context managers** for file and resource handling
- **Built-in functions** (`map`, `filter`, `zip`, `enumerate`, `sorted`, `sum`, `max`, `min`) over manual loops
- **`dataclasses` / well-structured classes** with proper dunder methods

---

## Language Reference (from course lectures, pages 23-94)

### 1. Syntax Rules

```python
# Indentation defines blocks (2 or 4 spaces, consistent)
if condition:
    statement1
    statement2   # same block

# Multiple statements on one line (use sparingly)
a = 1; b = 2; print(a, b)

# Inline conditional
A = Y if X else Z
```

### 2. Output & Input

```python
# f-string formatting (PREFERRED)
x, y = 23, 45.565
print(f'{x} and {y:.2f}')         # => 23 and 45.56

# format() method
print('{0} and {1}'.format('one', 'two'))

# print options
print('hello', end='')            # no newline
print('a', 'b', sep=', ')        # custom separator

# Input
name = input('Enter name: ')      # returns str
n    = int(input('Enter int: '))  # convert immediately
x    = float(input('Enter float: '))
```

### 3. Conditionals

```python
# if / elif / else
if a > 10:
    ...
elif a > 5:
    ...
else:
    ...

# match (Python 3.10+) - like switch/case with pattern matching
match code:
    case 200: print("OK")
    case 404: print("Not Found")
    case _:   print("Unknown")

# match with dict pattern + guard
match data:
    case {"type": "user", "id": user_id}:
        print(f"User {user_id}")
    case {"type": "admin", "id": admin_id} if admin_id > 1000:
        print(f"Admin {admin_id}")
    case _:
        print("Unknown")
```

### 4. Loops

```python
# while
i = 0
while i < 10:
    i += 1

# for over any iterable
for i in range(10):       ...
for c in 'hello':         ...
for item in my_list:      ...

# continue / break / else
for i in range(10):
    if i == 5: continue   # skip
    if i == 8: break      # exit loop
else:
    print('loop completed without break')  # runs only if no break
```

### 5. Arithmetic

```python
20 // 3        # => 6    (floor division)
20 % 3         # => 2    (modulo)
3 ** 4         # => 81   (power)
pow(3, 4, 27)  # => 0    (3^4 mod 27)
abs(-42)       # => 42
divmod(20, 3)  # => (6, 2)
round(3.14159, 2)  # => 3.14

import math
math.pi, math.e
math.sqrt(x), math.log(x), math.log10(x)
math.sin(math.radians(30))   # => 0.5
math.factorial(5)            # => 120

import random
random.random()              # [0.0, 1.0)
random.randint(1, 100)       # [1, 100]
random.choice(['a', 'b'])
random.shuffle(lst)
```

---

## Strings

```python
s = 'hello world'

# Operations
len(s)                    # => 11
s + ' !'                  # concatenation
s * 3                     # repetition
s[0], s[-1]               # indexing

# Slicing: s[start:stop:step]
s[3:7]       # 'lo w'
s[::-1]      # reverse
s[::2]       # every 2nd char

# Raw strings (avoid escape issues)
path = r'C:\new\file.txt'

# Multiline
text = """Line 1
Line 2"""

# String methods - strings are IMMUTABLE, all methods return NEW strings
s.upper(), s.lower()
s.strip(), s.lstrip(), s.rstrip()
s.split(',')               # => list
','.join(['a', 'b', 'c']) # => 'a,b,c'
s.find('llo')              # first index or -1
s.rfind('l')               # last index
s.replace('hello', 'hi')
s.startswith('he'), s.endswith('ld')
s.isdigit(), s.isalpha(), s.isalnum()
s.islower(), s.isupper()

# char <-> int
ord('A')    # => 65
chr(65)     # => 'A'

# CORRECT efficient string building (NEVER use += in a loop)
parts = [str(i) for i in range(1000)]
result = ''.join(parts)    # O(n) not O(n^2)
```

---

## Lists

```python
# Creation
lst = []
lst = [0] * 10             # [0, 0, ..., 0]
lst = list('abc')          # ['a', 'b', 'c']
lst = list(range(10))

# List comprehensions (PREFERRED over loops)
squares   = [x**2 for x in range(10)]
evens     = [x for x in range(20) if x % 2 == 0]
flat      = [x+y for x in 'abc' if x != 'b' for y in '12']

# Key operations
lst.append(x)              # add to end O(1)
lst.extend(other)          # extend with iterable O(k)
lst.insert(i, x)           # insert at index O(n)
lst.remove(x)              # remove first occurrence O(n)
lst.pop()                  # remove & return last O(1)
lst.pop(i)                 # remove & return index i O(n)
lst.index(x)               # first index of x
lst.count(x)               # count occurrences
lst.sort(key=lambda x: x)  # in-place sort
lst.reverse()              # in-place reverse
lst.copy()                 # shallow copy
lst.clear()                # remove all

# Built-in aggregates
sum(lst), min(lst), max(lst)
sorted(lst, key=lambda x: -x)  # returns NEW sorted list

# Slicing
lst[1:4]                   # elements 1,2,3
lst[::2]                   # every 2nd
lst[::-1]                  # reversed copy
lst[1:3] = [0, 0, 0]      # replace slice
del lst[:-3]               # delete slice

# COPY GOTCHAS
M = L           # ALIAS - same object!
M = L.copy()    # shallow copy - nested lists still shared
import copy
M = copy.deepcopy(L)       # fully independent deep copy
```

---

## Tuples

```python
# Immutable sequences (faster than lists, hashable)
a = (1, 2, 3)
a = 1, 2, 3         # parentheses optional
a = (42,)           # single-element tuple - NOTE the comma!
a = tuple('abc')    # => ('a', 'b', 'c')

# Swap (Pythonic - no temp variable needed)
a, b = b, a

# Packing / unpacking
x, y, z = (1, 2, 3)
first, *rest = (1, 2, 3, 4)   # first=1, rest=[2,3,4]
```

---

## Dictionaries

```python
# Creation
d = {}
d = {'a': 1, 'b': 2}
d = dict([('a', 1), ('b', 2)])
d = dict.fromkeys(['x', 'y'], 0)     # {'x': 0, 'y': 0}
d = {k: k**2 for k in range(5)}     # dict comprehension

# Access
d['key']                    # KeyError if missing
d.get('key', default)       # safe access

# Modification
d['new_key'] = value
d.update({'a': 10, 'c': 3})

# Iteration
for k in d:               ...
for k, v in d.items():    ...
for k in d.keys():        ...
for v in d.values():      ...

# Remove
d.pop('key')               # removes & returns value
del d['key']
d.clear()

# Merge (Python 3.9+)
merged = d1 | d2

# Counter pattern
from collections import Counter, defaultdict
counts = Counter(['a', 'b', 'a', 'c', 'b', 'a'])
# Counter({'a': 3, 'b': 2, 'c': 1})

dd = defaultdict(list)
dd['key'].append(1)         # no KeyError
```

---

## Sets

```python
s = set()                   # empty set (NOT {})
s = {1, 2, 3}
s = set('hello')            # {'h', 'e', 'l', 'o'}
s = {i**2 for i in range(10)}   # set comprehension

# Use sets for deduplication and O(1) membership lookup
unique = set(my_list)
if x in my_set: ...         # O(1) vs O(n) for list

# Set operations
s1 | s2    # union
s1 & s2    # intersection
s1 - s2    # difference
s1 ^ s2    # symmetric difference
s1 <= s2   # is s1 a subset of s2?

s.add(x)
s.remove(x)        # KeyError if missing
s.discard(x)       # safe remove
```

---

## Functions

```python
def add(x, y):
    return x + y

# Default parameters (mutable defaults are shared across calls!)
def f(x, lst=None):    # CORRECT pattern
    if lst is None:
        lst = []
    lst.append(x)
    return lst

# BAD - lst is created ONCE and shared
def f_bad(x, lst=[]):
    lst.append(x)
    return lst

# *args - positional variadic
def func(*args):
    return sum(args)
func(1, 2, 3)          # => 6

# **kwargs - keyword variadic
def func(**kwargs):
    return kwargs
func(a=1, b=2)         # => {'a': 1, 'b': 2}

# Spread a list as arguments
args = [1, 2, 3]
func(*args)

# Lambda - anonymous single-expression function
add = lambda x, y: x + y
key_fn = lambda x: (x[1], x[0])   # sort key
sorted_lst = sorted(pairs, key=lambda p: p[1])

# Closures - functions that capture outer scope
def make_adder(n):
    def adder(x):
        return x + n
    return adder
add5 = make_adder(5)
add5(3)   # => 8

# Function composition
def compose(f, g):
    def h(x): return f(g(x))
    return h

# Global vs local
x = 10
def f():
    global x
    x = 20     # modifies global x

# Nonlocal (for nested functions)
def outer():
    x = 10
    def inner():
        nonlocal x
        x += 1
    inner()
    return x
```

---

## Iterators & Generators (Memory-Efficient)

```python
# map - lazy, O(1) memory regardless of size
result = map(lambda x: x**2, [1, 2, 3, 4])
list(result)    # [1, 4, 9, 16]

# filter - lazy
evens = filter(lambda x: x % 2 == 0, range(100))

# zip - lazy, stops at shortest
pairs = list(zip([1, 2, 3], ['a', 'b', 'c']))

# enumerate - lazy
for i, val in enumerate(my_list):
    print(i, val)

# Generator expression - O(1) memory
gen = (x**2 for x in range(1_000_000))  # not computed yet!
total = sum(x**2 for x in range(1_000_000))  # very efficient

# Generator function with yield
def squares(n):
    for i in range(n):
        yield i**2

# iter() / next()
it = iter([1, 2, 3])
next(it)    # 1
next(it)    # 2

# Custom iterator class
class Counter:
    def __init__(self, n):
        self.n = n
    def __iter__(self):
        self.i = 0
        return self
    def __next__(self):
        if self.i < self.n:
            val = self.i
            self.i += 1
            return val
        raise StopIteration

# Combine iterators with yield
def chain_iters(*iters):
    for it in iters:
        for item in it:
            yield item
```

---

## Files

```python
# ALWAYS use with - auto-closes even on exception
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()          # entire file as string
    # or
    lines = f.readlines()       # list of lines
    # or
    for line in f:              # memory-efficient line-by-line
        process(line.rstrip())

# Write
with open('out.txt', 'w', encoding='utf-8') as f:
    f.write('Hello\n')
    f.writelines(['line1\n', 'line2\n'])

# Append
with open('log.txt', 'a') as f:
    f.write('new entry\n')

# Read + Write
with open('file.txt', 'r+') as f:
    data = f.read()
    f.write('\nmore content')

# modes: 'r' read, 'w' write (overwrite), 'a' append, 'b' binary, '+' read+write
```

---

## Modules & Packages

```python
import math
import math as m
from math import sqrt, pi
from math import *          # import everything (avoid in large projects)

import random
from random import randint as rdi

# Standard import style (PEP 8)
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Custom module: just a .py file
# my_module.py:
#   def add(a, b): return a + b
#   PI = 3.14159

import my_module
my_module.add(3, 5)

from my_module import add, PI

# Guard: run only when executed directly
if __name__ == '__main__':
    main()

# Package structure:
# my_package/
#   __init__.py
#   module_a.py
#   module_b.py
```

---

## Classes & OOP

```python
class Point:
    # Class attribute (shared across all instances)
    count = 0

    def __new__(cls, x, y):          # Constructor - creates the object
        cls.count += 1
        return super().__new__(cls)

    def __init__(self, x, y):        # Initializer - sets up state
        self.x = x                   # instance attribute
        self.y = y

    def __del__(self):               # Destructor
        print('deleted')

    def __repr__(self):              # for repr() and REPL display
        return f'Point({self.x}, {self.y})'

    def __str__(self):               # for print()
        return f'({self.x}, {self.y})'

    def __eq__(self, other):         # ==
        return self.x == other.x and self.y == other.y

    def __add__(self, other):        # +
        return Point(self.x + other.x, self.y + other.y)

    def __len__(self):               # len()
        return 2

    def __contains__(self, val):     # in operator
        return val in (self.x, self.y)

    def distance(self):              # instance method
        return (self.x**2 + self.y**2) ** 0.5

    @staticmethod
    def origin():                    # no self/cls - utility function
        return Point(0, 0)

    @classmethod
    def total(cls):                  # receives class, not instance
        return cls.count

# Inheritance
class Point3D(Point):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z

# Callable object
class Multiplier:
    def __init__(self, factor):
        self.factor = factor
    def __call__(self, x):          # instance acts like a function
        return x * self.factor

double = Multiplier(2)
double(5)   # => 10

# Dynamic class creation
MyClass = type('MyClass', (object,), {
    'attr': 42,
    'method': lambda self: self.attr
})

# Dataclass - less boilerplate
from dataclasses import dataclass, field
@dataclass
class Config:
    host: str
    port: int = 8080
    tags: list = field(default_factory=list)
```

### Complete Special Methods Reference

```python
# Basics
__init__(self, ...)       # initializer
__repr__(self)            # repr(x), REPL
__str__(self)             # str(x), print

# Arithmetic (right-hand versions: __radd__, __rsub__, etc.)
__add__(self, y)          # x + y
__sub__(self, y)          # x - y
__mul__(self, y)          # x * y
__truediv__(self, y)      # x / y
__floordiv__(self, y)     # x // y
__mod__(self, y)          # x % y
__pow__(self, y)          # x ** y
__neg__(self)             # -x
__abs__(self)             # abs(x)

# In-place
__iadd__(self, y)         # x += y
__imul__(self, y)         # x *= y

# Comparison
__eq__(self, y)           # x == y
__ne__(self, y)           # x != y
__lt__(self, y)           # x < y
__le__(self, y)           # x <= y
__gt__(self, y)           # x > y
__ge__(self, y)           # x >= y
__bool__(self)            # if x:

# Container
__len__(self)             # len(x)
__contains__(self, t)     # t in x
__getitem__(self, k)      # x[k]
__setitem__(self, k, v)   # x[k] = v
__delitem__(self, k)      # del x[k]

# Iteration
__iter__(self)            # iter(x)
__next__(self)            # next(x)

# Attribute access
__getattr__(self, name)   # x.name (only when not found normally)
__setattr__(self, n, v)   # x.name = v
__delattr__(self, name)   # del x.name

# Callable
__call__(self, ...)       # x(...)

# Copy & Hash
__copy__(self)            # copy.copy(x)
__deepcopy__(self)        # copy.deepcopy(x)
__hash__(self)            # hash(x)
```

---

## NumPy - Vectorized Numeric Computing

> **Rule #1:** Replace ALL Python numeric loops with NumPy vectorized operations. NumPy is 10-100x faster.

```python
import numpy as np

# Array creation
a = np.array([1, 2, 3, 4])
A = np.array([[1, 2], [3, 4]])
np.zeros([m, n])            # m x n zeros
np.ones([m, n])             # m x n ones
np.full([m, n], val)        # filled with val
np.eye(n)                   # identity matrix
np.arange(start, stop, step)
np.random.rand(m, n)        # uniform [0,1)
np.random.randn(m, n)       # standard normal
np.diag(v)                  # diagonal matrix from vector
np.tril(A), np.triu(A)      # lower/upper triangular

# Dtype control
a = np.array([1, 2, 3], dtype=np.float32)  # 4 bytes/elem
a = np.array([1, 2, 3], dtype=np.float64)  # 8 bytes/elem (default)
```

### Element-wise Operations (vectorized, no loops!)

```python
A + B, A - B, A * B, A / B   # element-wise
A ** 2                         # element-wise power
np.sqrt(A)                     # element-wise sqrt
np.abs(A)                      # element-wise abs
np.exp(A), np.log(A)
A > 0                          # boolean array
A[A > 0]                       # boolean indexing
```

### Linear Algebra

```python
A.T                            # transpose
np.dot(A, B)                   # matrix multiply
A @ B                          # matrix multiply (preferred)
np.linalg.det(A)               # determinant
np.linalg.inv(A)               # inverse
np.linalg.pinv(A)              # pseudo-inverse (safer for singular)
eigenvalues, eigenvectors = np.linalg.eig(A)
U, S, Vt = np.linalg.svd(A)   # SVD decomposition
Q, R = np.linalg.qr(A)        # QR decomposition
```

### Reshape, Concatenate, Transform

```python
A.reshape([m, n])              # reshape (use -1 for auto dim)
A.reshape([-1, 1])             # column vector
np.r_[A, B]                    # concatenate row-wise
np.c_[A, B]                    # concatenate column-wise
np.tile(A, [m, n])             # repeat A m x n times
np.roll(A, n)                  # cyclic shift by n
np.flip(A, axis=1)             # reverse along axis
np.split(A, k, axis=0)         # split into k parts
```

### Search & Sort

```python
np.sort(A, axis=-1)
np.argsort(A)                  # indices that sort A
np.partition(A, k)             # kth smallest in final position
np.searchsorted(sorted_A, v)   # insertion indices (binary search)
np.unique(A, return_counts=True)
np.bincount(A)                 # count integers
np.where(A > 0, A, -1)        # conditional select
np.nonzero(A)                  # indices of nonzero elements
np.argwhere(A > 0)             # coordinates of True elements
```

### Views vs Copies (CRITICAL for performance)

```python
b = a.view()         # shares memory - modifying b changes a!
b = np.copy(a)       # independent deep copy
b = np.broadcast_to(a, (3, 3))   # broadcast without copy

# Sliding windows (no copy - very fast)
from numpy.lib.stride_tricks import sliding_window_view
windows = sliding_window_view(a, window_shape=3)

# Advanced striding
from numpy.lib.stride_tricks import as_strided
result = as_strided(a, shape=(3, 2), strides=(8, 4))
```

### Performance Example

```python
# SLOW - Python loop
result = [i**2 for i in range(1_000_000)]     # ~220ms

# FAST - NumPy vectorized
a = np.arange(1_000_000)
result = a**2                                  # ~0.5ms  (400x faster)
```

---

## SciPy - Scientific Computing

```python
import scipy.linalg as sl

# Special matrices
sl.toeplitz(l, u)          # Toeplitz matrix
sl.hankel(l, u)            # Hankel matrix
sl.circulant(v)            # Circulant matrix
sl.kron(A, B)              # Kronecker product A tensor B
sl.block_diag(A, B, C)    # Block diagonal matrix
sl.fiedler(v)              # Fiedler matrix |vi - vj|
sl.convolution_matrix(v, n)  # Convolution matrix

# Pairwise distances
from scipy.spatial.distance import pdist, squareform
D = squareform(pdist(A))   # all pairwise Euclidean distances

# Faster custom distance (40x faster than scipy for large matrices!)
def pairwise_dist(A):
    B = A @ A.T
    D = np.diag(B).reshape([1, -1])
    return (D.T + D - 2 * B) ** 0.5
```

---

## Matplotlib - Visualization

```python
import matplotlib.pyplot as plt
import numpy as np

# 2D scatter plot
plt.figure()
plt.scatter(x, y, marker='*', color='red', label='data')
plt.title('Title'); plt.xlabel('x'); plt.ylabel('y')
plt.legend()
plt.savefig('plot.pdf')
plt.show()

# 2D line plot
plt.plot(x, y, marker='o', color='green', linewidth=2)

# 3D scatter
import mpl_toolkits.mplot3d
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot('111', projection='3d')
ax.scatter(x, y, z, color='b', marker='.')

# 3D surface
x, y = np.meshgrid(np.arange(-5, 5, 0.25), np.arange(-5, 5, 0.25))
z = np.sqrt(x**2 + y**2)
ax.plot_surface(x, y, z, color='b')

# Dimensionality reduction for visualization (SVD trick)
def visualize_3d(A):
    """Project high-dim data to 3D using SVD."""
    U, S, Vt = np.linalg.svd(A.T)
    S = np.diag(S[:3])
    B = S @ Vt[:3, :]
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot('111', projection='3d')
    ax.scatter(B[0], B[1], B[2], marker='.')
    plt.show()
```

---

## Parallel Computing

> Python's GIL prevents true multi-threading for CPU-bound tasks.
> Use `multiprocessing` for CPU-bound work, `threading` only for I/O-bound work.

### threading - BLOCKED by GIL for CPU work

```python
from threading import Thread

def countdown(n):
    while n > 0: n -= 1

# Creates 2 threads - but GIL means NOT truly parallel for CPU work
t1 = Thread(target=countdown, args=(25_000_000,))
t2 = Thread(target=countdown, args=(25_000_000,))
t1.start(); t2.start()
t1.join();  t2.join()
# Same speed as single thread!
```

### multiprocessing - TRUE parallelism for CPU-bound tasks

```python
from multiprocessing import Process, Pool
from time import time

def countdown(n):
    while n > 0: n -= 1

if __name__ == '__main__':          # REQUIRED guard for multiprocessing
    # Simple parallel processes
    r1 = Process(target=countdown, args=(25_000_000,))
    r2 = Process(target=countdown, args=(25_000_000,))
    r1.start(); r2.start()
    r1.join();  r2.join()
    # ~2x faster than sequential!

    # Pool - easy parallel map
    with Pool(processes=4) as pool:
        results = pool.map(heavy_function, data_list)

    # Pool with starmap (multiple args)
    args = [(a, b) for a, b in zip(list1, list2)]
    results = pool.starmap(func, args)
```

### Threading - use only for I/O-bound (network, disk, DB)

```python
from threading import Thread, Lock

lock = Lock()
shared = []

def fetch_url(url):
    # ... HTTP request ...
    with lock:
        shared.append(result)

threads = [Thread(target=fetch_url, args=(url,)) for url in urls]
for t in threads: t.start()
for t in threads: t.join()
```

---

## Performance Best Practices

| Pattern | Slow | Fast |
|---------|------|------|
| Numeric loop | `for i in range(n): s += i` | `np.sum(np.arange(n))` |
| List building | `lst = []` + `append` loop | `[expr for x in iter]` |
| String concat | `s += x` in a loop | `''.join(parts)` |
| Membership test | `x in my_list` O(n) | `x in my_set` O(1) |
| Counting | `dict` + manual counting | `Counter(lst)` |
| Parallel CPU work | `threading` | `multiprocessing.Pool` |
| Large arrays | Python lists | `numpy.ndarray` |
| Pairwise distances | `scipy.spatial.pdist` | Custom `A @ A.T` formula |
| Matrix multiply | `np.dot(A, B)` | `A @ B` |

---

## Code Generation Rules - ALWAYS apply these

1. **Use `import numpy as np`** for any numeric computation on arrays/matrices.
2. **Vectorize** - replace every numeric loop with a NumPy operation.
3. **Use comprehensions** instead of `for` loops that build lists.
4. **Use generators** for large sequences you don't need all at once.
5. **Use `with open(...)`** for all file operations.
6. **Use `multiprocessing.Pool`** for CPU-bound parallel work, not `threading`.
7. **Use f-strings** for formatting: `f'{x:.2f}'`.
8. **Never mutate default mutable args** - use `None` as default and create inside.
9. **Use `collections.Counter`/`defaultdict`** instead of manual dict counting.
10. **Add `if __name__ == '__main__':`** guard in scripts using multiprocessing.
11. **Use `@dataclass`** for simple data containers.
12. **Prefer `sorted()` over `.sort()`** when you need a new list.
13. **Use `np.linalg.pinv()`** instead of `inv()` for potentially singular matrices.

---

## Complete Examples

### Efficient data processing

```python
import numpy as np
from collections import Counter

data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

counts = Counter(data)
frequent = {k for k, v in counts.items() if v > 1}   # {1, 3, 5}
result = np.array([x**2 for x in data if x in frequent])
print(result.mean(), result.std())
```

### Parallel computation with Pool

```python
from multiprocessing import Pool
import numpy as np

def process_chunk(chunk):
    return np.sum(chunk ** 2)

if __name__ == '__main__':
    data = np.random.rand(1_000_000)
    chunks = np.array_split(data, 8)
    with Pool(8) as pool:
        results = pool.map(process_chunk, chunks)
    total = sum(results)
    print(f"Result: {total:.4f}")
```

### Fast pairwise distance matrix (40x faster than scipy.pdist)

```python
import numpy as np

def pairwise_euclidean(A):
    """Compute all pairwise Euclidean distances between rows of A."""
    B = A @ A.T
    d = np.diag(B).reshape(1, -1)
    return np.sqrt(np.maximum(d.T + d - 2 * B, 0))

A = np.random.rand(1000, 100)
D = pairwise_euclidean(A)   # shape (1000, 1000)
```

### Class with full dunder methods

```python
from dataclasses import dataclass

@dataclass
class Vector:
    x: float
    y: float

    def __add__(self, other): return Vector(self.x + other.x, self.y + other.y)
    def __mul__(self, scalar): return Vector(self.x * scalar, self.y * scalar)
    def __abs__(self): return (self.x**2 + self.y**2) ** 0.5
    def __repr__(self): return f'Vector({self.x}, {self.y})'

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)    # Vector(4, 6)
print(abs(v2))    # 5.0
```
