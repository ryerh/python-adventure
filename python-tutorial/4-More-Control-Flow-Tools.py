# -*- coding: utf-8 -*-


# if Statements
x = int(input("Please enter an integer: "))
if x < 0:
  print('Negative number')
elif x > 0:
  print('Positive number')
else:
  print('Zero')


# for Statement
words = ['cat', 'window', 'door']
for w in words:
  print(w, len(w))


# range(begin=0, end, step) Function
for i in range(5):
  print(i)  # 0 1 2 3 4

range(10)        # -> an iterator
list(range(10))  # -> a list


# stay away from else Clauses on loops, anti-pattern
for n in range(10):
  pass
else:
  pass


# functions
def fib(n):
  if n <= 0:
    return 0
  elif n == 1:
    return 1
  else:
    return fib(n - 1) + fib(n - 2)

print('fib of 10', fib(10))


# default argument values
def ask_ok(prompt, retries=4, remider='Please try again'):
  while True:
    ok = input(prompt)
    if ok in ('y', 'yes'):
      return True
    if ok in ('n', 'no'):
      return False
    retries = retries - 1
    if retries < 0:
      raise ValueError('invalid user')
    print(remider)


# the scope of default argument values
i = 100
def foo(bar=i):
  print(bar)
i = 6
foo()  # 5


# default arguments caution
def f(a, L=None):
  if L is None:
    L = []
  L.append(a)
  return L

f(1)  # [1]
f(2)  # [2]
f(3)  # [3]


# keyword arguments
def foo(a, b='b', c='c'):
  pass
foo(1)
foo(1, c=3)
foo(b=2)

def cheeseshop(kind, *arguments, **keywords):
  print("-- Do you have any", kind, "?")
  print("-- I'm sorry, we're all out of", kind)
  for arg in arguments:
    print(arg)
  print("-" * 40)
  keys = sorted(keywords.keys())
  for kw in keys:
    print(kw, ":", keywords[kw])

cheeseshop(
  "Limburger",
  *[
    "It's very runny, sir.",
    "It's really very, VERY runny, sir.",
  ],
  **{
    "shopkeeper": "Michael Palin",
    "client": "John Cleese",
    "sketch": "Cheese Shop Sketch",
  }
)
# -- Do you have any Limburger ?
# -- I'm sorry, we're all out of Limburger
# It's very runny, sir.
# It's really very, VERY runny, sir.
# ----------------------------------------
# client : John Cleese
# shopkeeper : Michael Palin
# sketch : Cheese Shop Sketch


# lambda expression
f = lambda x: x + n


# documentation strings
def func():
  """
  it's func
  """
  pass
print(func.__doc__)


# function annotations, but you can still pass other typed values
def f(ham: str, eggs: str = 'eggs') -> str:
  print("Annotations:", f.__annotations__)
  print("Arguments:", ham, eggs)
  return ham + ' and ' + eggs

