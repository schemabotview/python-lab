PIPELINE = {
  "extract": [],
  "clean": ["extract"],
  "enrich": ["clean"],
  "load": ["enrich"],
  "report": ["load"],
}

FANOUT = {
  "extract": [],
  "clean_a": ["extract"],
  "clean_b": ["extract"],
  "join": ["clean_a", "clean_b"],
}

CYCLE = {"a": ["b"], "b": ["c"], "c": ["a"]}

assert topo_order(PIPELINE) == ["extract", "clean", "enrich", "load", "report"], "a straight chain runs in order"
assert topo_order(FANOUT)[0] == "extract", "the root always goes first"
assert topo_order(FANOUT)[-1] == "join", "and the task depending on both goes last"
assert set(topo_order(FANOUT)[1:3]) == {"clean_a", "clean_b"}, "the two independent tasks sit in the middle"
assert topo_order({}) == [], "an empty pipeline"
assert topo_order({"solo": []}) == ["solo"], "one task with no dependencies"
assert topo_order(CYCLE) == [], "a cycle has no runnable order at all"

assert has_cycle(CYCLE) is True, "a depends on b depends on c depends on a"
assert has_cycle(PIPELINE) is False, "a chain is fine"
assert has_cycle(FANOUT) is False, "so is a fan-out"
assert has_cycle({}) is False, "an empty pipeline has no cycle"
assert has_cycle({"a": ["a"]}) is True, "a task depending on itself"

assert ready_tasks(PIPELINE, []) == ["extract"], "only the root can start"
assert ready_tasks(PIPELINE, ["extract"]) == ["clean"], "then the next link"
assert ready_tasks(PIPELINE, ["extract", "clean"]) == ["enrich"], "and the next"
assert ready_tasks(FANOUT, ["extract"]) == ["clean_a", "clean_b"], "two tasks unblock at once"
assert ready_tasks(FANOUT, ["extract", "clean_a"]) == ["clean_b"], "join still waits on clean_b"
assert ready_tasks(FANOUT, ["extract", "clean_a", "clean_b"]) == ["join"], "now join can run"
assert ready_tasks(PIPELINE, ["extract", "clean", "enrich", "load", "report"]) == [], "everything is done"
assert ready_tasks({}, []) == [], "nothing to run"

assert levels(PIPELINE) == [["extract"], ["clean"], ["enrich"], ["load"], ["report"]], "a chain is five waves of one"
assert levels(FANOUT) == [["extract"], ["clean_a", "clean_b"], ["join"]], "the fan-out runs two tasks in one wave"
assert levels(CYCLE) == [], "a cycle has no waves"
assert levels({}) == [], "an empty pipeline"
assert levels({"a": [], "b": []}) == [["a", "b"]], "two independent tasks are a single wave"
assert len(levels(FANOUT)) == 3, "three waves, not four tasks — that is the parallelism"

DIAMOND = {"a": [], "b": ["a"], "c": ["a"], "d": ["b", "c"]}

assert levels(DIAMOND) == [["a"], ["b", "c"], ["d"]], "a diamond collapses to three waves"
assert topo_order(DIAMOND)[0] == "a" and topo_order(DIAMOND)[-1] == "d", "with a at the start and d at the end"
assert has_cycle(DIAMOND) is False, "a diamond is not a cycle — direction is what matters"
