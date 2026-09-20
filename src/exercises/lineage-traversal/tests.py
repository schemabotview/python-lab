LINEAGE = {
  "raw_orders": ["stg_orders"],
  "raw_users": ["stg_users"],
  "stg_orders": ["fct_sales"],
  "stg_users": ["dim_customer"],
  "dim_customer": ["fct_sales"],
  "fct_sales": ["report_daily", "report_monthly"],
}

assert downstream(LINEAGE, "raw_orders") == ["fct_sales", "report_daily", "report_monthly", "stg_orders"], "everything reachable from raw_orders"
assert downstream(LINEAGE, "fct_sales") == ["report_daily", "report_monthly"], "the two reports"
assert downstream(LINEAGE, "report_daily") == [], "a leaf has nothing downstream"
assert downstream(LINEAGE, "unknown_table") == [], "a table not in the graph"
assert "raw_orders" not in downstream(LINEAGE, "raw_orders"), "a table is not downstream of itself"

assert downstream(LINEAGE, "raw_users") == ["dim_customer", "fct_sales", "report_daily", "report_monthly", "stg_users"], "a longer chain, reached through dim_customer"

assert upstream(LINEAGE, "fct_sales") == ["dim_customer", "raw_orders", "raw_users", "stg_orders", "stg_users"], "everything fct_sales is built from, on both branches"
assert upstream(LINEAGE, "stg_orders") == ["raw_orders"], "one step back"
assert upstream(LINEAGE, "raw_orders") == [], "a source has nothing upstream"
assert upstream(LINEAGE, "report_daily") == ["dim_customer", "fct_sales", "raw_orders", "raw_users", "stg_orders", "stg_users"], "a report depends on everything behind it"

assert path_between(LINEAGE, "raw_orders", "fct_sales") == ["raw_orders", "stg_orders", "fct_sales"], "the path through staging"
assert path_between(LINEAGE, "raw_orders", "raw_orders") == ["raw_orders"], "a table reaches itself in no steps"
assert path_between(LINEAGE, "report_daily", "raw_orders") == [], "lineage is directed — there is no way back"
assert path_between(LINEAGE, "raw_users", "report_monthly") == ["raw_users", "stg_users", "dim_customer", "fct_sales", "report_monthly"], "the full five-hop path"
assert path_between(LINEAGE, "raw_orders", "nowhere") == [], "no path to a table that isn't there"

DIAMOND = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}

assert len(path_between(DIAMOND, "a", "d")) == 3, "breadth-first finds a SHORTEST path, not just any path"
assert path_between(DIAMOND, "a", "d")[0] == "a", "starting where asked"
assert path_between(DIAMOND, "a", "d")[-1] == "d", "and ending there"
assert downstream(DIAMOND, "a") == ["b", "c", "d"], "d is reached twice but listed once"

assert impacted_by(LINEAGE, "fct_sales") == ["fct_sales", "report_daily", "report_monthly"], "the blast radius includes the table itself"
assert impacted_by(LINEAGE, "report_daily") == ["report_daily"], "a leaf impacts only itself"
assert impacted_by(LINEAGE, "unknown_table") == ["unknown_table"], "even a table not in the graph impacts itself"

CYCLIC = {"a": ["b"], "b": ["c"], "c": ["a"]}

assert downstream(CYCLIC, "a") == ["a", "b", "c"], "a cycle does not hang — the seen set stops it"
assert sorted(path_between(CYCLIC, "a", "c")) == ["a", "b", "c"], "and a path is still found"
