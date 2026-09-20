assert depth_of(5) == 0, "a plain value nests not at all"
assert depth_of("text") == 0, "a string is a leaf, not a container"
assert depth_of([]) == 1, "an empty list is still one level"
assert depth_of({}) == 1, "and so is an empty dict"
assert depth_of([1, 2]) == 1, "a flat list"
assert depth_of([1, [2]]) == 2, "one level of nesting"
assert depth_of({"a": {"b": {"c": 1}}}) == 3, "three dicts deep"
assert depth_of({"a": [1, {"b": 2}]}) == 3, "dicts and lists mixed"
assert depth_of([[], [[]]]) == 3, "empty containers still count as levels"

assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5], "every leaf, left to right"
assert flatten([]) == [], "nothing to flatten"
assert flatten([[], []]) == [], "empty branches contribute nothing"
assert flatten([1, 2]) == [1, 2], "already flat"
assert flatten([[[[7]]]]) == [7], "deeply buried"
assert flatten(["a", ["b"]]) == ["a", "b"], "strings are leaves, not lists to descend into"

assert count_leaves({"a": 1, "b": {"c": 2, "d": 3}}) == 3, "three leaf values"
assert count_leaves([]) == 0, "an empty container holds no leaves"
assert count_leaves({"a": []}) == 0, "nor does a nested empty one"
assert count_leaves(5) == 1, "a bare value is one leaf"
assert count_leaves([1, [2, [3]]]) == 3, "however deep they are"

assert fib_naive(10)[0] == 55, "the tenth Fibonacci number"
assert fib_memo(10)[0] == 55, "the memoised version agrees"
assert fib_naive(0)[0] == 0, "the base case"
assert fib_naive(1)[0] == 1, "the other base case"
assert fib_memo(30)[0] == 832040, "and it can go further"

assert fib_naive(20)[1] == 21891, "the naive version made twenty-one thousand calls for the twentieth number"
assert fib_memo(20)[1] == 21, "the memoised one made twenty-one — one per value"
assert fib_memo(30)[1] == 31, "still one per value at thirty"
assert fib_naive(20)[1] > fib_memo(20)[1] * 1000, "a thousand times the work, recomputing the same answers"
assert fib_naive(25)[1] > fib_naive(20)[1] * 10, "each step up roughly multiplies the naive cost — that is exponential"


def nest(depth):
  built = "leaf"
  for _ in range(depth):
    built = [built]
  return built


assert depth_of(nest(200)) == 200, "two hundred levels is fine"
assert flatten(nest(200)) == ["leaf"], "and flattens back to one leaf"

import sys

ORIGINAL_LIMIT = sys.getrecursionlimit()
sys.setrecursionlimit(60)

try:
  depth_of(nest(200))
except RecursionError:
  TOO_DEEP = "raised"
else:
  TOO_DEEP = "survived"

sys.setrecursionlimit(ORIGINAL_LIMIT)

assert TOO_DEEP == "raised", "recursion has a hard depth limit, and exceeding it raises RecursionError"
assert sys.getrecursionlimit() == ORIGINAL_LIMIT, "and the limit is put back, so later tests are unaffected"
