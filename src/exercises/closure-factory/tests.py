assert scaler(2)(10) == 20, "the returned function remembers its factor"
assert scaler(3)(10) == 30, "a different factor, a different function"
assert scaler(0)(10) == 0, "a factor of zero"

DOUBLE = scaler(2)
TRIPLE = scaler(3)

assert DOUBLE(5) == 10, "each call to scaler captured independently"
assert TRIPLE(5) == 15, "so these two never interfere"
assert DOUBLE(1) == 2, "and the capture outlives the call to scaler that made it"

COUNT = make_counter()

assert COUNT() == 1, "the first bump"
assert COUNT() == 2, "the captured value persists between calls"
assert COUNT() == 3, "and keeps climbing"

SEPARATE = make_counter()

assert SEPARATE() == 1, "a second counter starts fresh — its own captured variable"
assert COUNT() == 4, "and the first one is unaffected"
assert make_counter(10)() == 11, "a counter can start anywhere"


def broken_counter():
  current = 0

  def bump():
    current += 1
    return current

  return bump


try:
  broken_counter()()
except UnboundLocalError:
  WITHOUT_NONLOCAL = "raises"
else:
  WITHOUT_NONLOCAL = "worked"

assert WITHOUT_NONLOCAL == "raises", "reassigning a captured name without `nonlocal` makes it local — hence UnboundLocalError"

assert threshold(100)(150) is True, "over the limit"
assert threshold(100)(50) is False, "under it"
assert threshold(100)(100) is False, "exactly the limit is not over it"
assert threshold(0)(1) is True, "a zero threshold"

assert [f(10) for f in build_scalers([1, 2, 3])] == [10, 20, 30], "each factory call captured its own factor"
assert build_scalers([]) == [], "no factors, no functions"
assert len(build_scalers([1, 2])) == 2, "one function per factor"

assert compose(str.strip, str.lower)("  Orders ") == "orders", "the steps run in order"
assert compose()("unchanged") == "unchanged", "no steps leaves the value alone"
assert compose(str.strip)("  a  ") == "a", "a single step"
assert compose(abs, str)(-3) == "3", "any callables, in the order given"

CLEAN = compose(str.strip, str.lower)

assert CLEAN("  A ") == "a", "the chain is built once and reused"
assert CLEAN(" B ") == "b", "remembering its steps each time"
