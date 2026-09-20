TABLES = [("orders", 1500), ("events", 300), ("users", 90), ("logs", 9000), ("temp", 12)]

assert top_k(TABLES, 2) == [("logs", 9000), ("orders", 1500)], "the two biggest, biggest first"
assert top_k(TABLES, 1) == [("logs", 9000)], "just the biggest"
assert len(top_k(TABLES, 99)) == 5, "asking for more than there are gives what there is"
assert top_k(TABLES, 0) == [], "asking for none"
assert top_k([], 3) == [], "nothing to rank"

assert bottom_k(TABLES, 2) == [("temp", 12), ("users", 90)], "the two smallest, smallest first"
assert bottom_k(TABLES, 1) == [("temp", 12)], "just the smallest"
assert bottom_k([], 3) == [], "nothing to rank"

assert streaming_top_k(TABLES, 2) == [("logs", 9000), ("orders", 1500)], "the streaming version agrees"
assert streaming_top_k(TABLES, 2) == top_k(TABLES, 2) == [("logs", 9000), ("orders", 1500)], "the streaming and batch versions agree, on the known answer"
assert streaming_top_k(TABLES, 5) == top_k(TABLES, 5) == [("logs", 9000), ("orders", 1500), ("events", 300), ("users", 90), ("temp", 12)], "even when k covers everything"
assert streaming_top_k([], 3) == [], "an empty stream"
assert streaming_top_k([("a", 1)], 3) == [("a", 1)], "fewer items than k"

BIG = [(f"t{n}", n) for n in range(1000)]

assert streaming_top_k(BIG, 3) == [("t999", 999), ("t998", 998), ("t997", 997)], "the top three of a thousand"
assert high_water(BIG, 3) == 3, "and the heap NEVER held more than three — a thousand items, three in memory"
assert high_water(BIG, 10) == 10, "bounded by k, not by the stream"
assert high_water([("a", 1)], 10) == 1, "or by the stream when it is shorter"


def endless():
  n = 0
  while True:
    n += 1
    yield (f"t{n}", n % 500)
    if n > 5000:
      return


assert high_water(endless(), 4) == 4, "five thousand items still fit in a heap of four"

assert merge_sorted([1, 4, 7], [2, 3, 9]) == [1, 2, 3, 4, 7, 9], "two sorted streams merged"
assert merge_sorted([1, 2], [], [3]) == [1, 2, 3], "an empty stream contributes nothing"
assert merge_sorted() == [], "no streams at all"
assert merge_sorted([1]) == [1], "one stream"
assert merge_sorted([1, 1], [1]) == [1, 1, 1], "duplicates across streams are all kept"
