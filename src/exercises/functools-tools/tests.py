assert total_rows([1500, 300, 90]) == 1890, "reduce folds the list to one number"
assert total_rows([]) == 0, "the start value is what makes an empty fold work"
assert total_rows([7]) == 7, "one batch"

assert widest([100, 900, 50]) == 900, "reduce can carry a comparison as easily as a sum"
assert widest([]) == 0, "and still needs its start value"
assert widest([5]) == 5, "one batch is its own widest"

assert qualify("prod")("sales", "orders") == "prod.sales.orders", "partial pre-filled the environment"
assert qualify("dev")("sales", "orders") == "dev.sales.orders", "a different pre-fill, a different function"

PROD = qualify("prod")

assert PROD("sales", "orders") == "prod.sales.orders", "the partial is reusable"
assert PROD("ops", "runs") == "prod.ops.runs", "with the remaining arguments varying"
assert table_name("prod", "sales", "orders") == "prod.sales.orders", "the original still takes all three"

row_count.cache_clear()
LOOKUPS["calls"] = 0

assert row_count("orders") == 600, "six characters, a hundred each"
assert LOOKUPS["calls"] == 1, "the first call really ran"
assert row_count("orders") == 600, "the same answer"
assert LOOKUPS["calls"] == 1, "but the body did NOT run again — that is the cache"
assert row_count("events") == 600, "a different argument"
assert LOOKUPS["calls"] == 2, "which did have to run"
assert row_count("orders") == 600, "and the first is still cached"
assert LOOKUPS["calls"] == 2, "so no third call"

assert row_count.cache_info().hits == 2, "two calls were served from the cache"
assert row_count.cache_info().misses == 2, "and two had to be computed"

row_count.cache_clear()
LOOKUPS["calls"] = 0

assert row_count("orders") == 600, "after a clear"
assert LOOKUPS["calls"] == 1, "the body runs again — the cache really was emptied"
