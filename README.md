pytco - Python Tail Call Optimization decorator
=====

This package provides a @tco decorator, that modifies the source code of
tco functions. If applied to other recursive functions it will break the source
code, so be careful.

Example:

```python
>>>def f(n, acc=1):
       if n <= 1:
           return acc
       return f(n - 1, acc * n)
>>>f(5)
120       
>>>decorated = tco(f)
>>>decorated(5)
120
```