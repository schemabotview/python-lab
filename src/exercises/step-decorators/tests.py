assert load("orders") == "loaded orders", "the wrapped function still does its job"
assert load.calls >= 1, "and the wrapper counted the call"

BEFORE = load.calls
load("a")
load("b")

assert load.calls == BEFORE + 2, "each call is tallied"
assert load("c") == "loaded c", "the return value passes straight through the wrapper"

assert load.__name__ == "load", "functools.wraps keeps the original name — without it this is 'wrapper'"
assert load.__doc__ == "Load one table.", "and the original docstring"

assert summarise("orders") == "[etl] summary of orders", "a decorator with an argument"
assert summarise.__name__ == "summarise", "wraps applies to this one too"


@counted
def add(left, right=0):
  return left + right


assert add(2, 3) == 5, "positional arguments forward unchanged"
assert add(2, right=8) == 10, "and keyword arguments too — that is what *args/**kwargs buys"
assert add(2) == 2, "including a defaulted one"
assert add.calls == 3, "three calls counted"


ATTEMPTS = {"n": 0}


@retry(3)
def flaky():
  ATTEMPTS["n"] += 1
  if ATTEMPTS["n"] < 3:
    raise ValueError("connection reset")
  return "succeeded"


assert flaky() == "succeeded", "it failed twice and worked on the third attempt"
assert ATTEMPTS["n"] == 3, "which took exactly three attempts"


@retry(2)
def always_fails():
  raise ValueError("disk full")


assert always_fails() == "gave up after 2: disk full", "the last error is reported once the attempts run out"


@retry(5)
def never_fails():
  return "first time"


assert never_fails() == "first time", "a successful call returns immediately, without using its retries"
