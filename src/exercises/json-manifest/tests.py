import os
os.makedirs("/tmp/lab", exist_ok=True)
MANIFEST = "/tmp/lab/manifest.json"

assert to_json({"b": 1, "a": 2}) == '{\n  "a": 2,\n  "b": 1\n}', "indented two spaces, and keys sorted"
assert to_json({}) == "{}", "an empty object"
assert to_json({"rows": [1, 2]}) == '{\n  "rows": [\n    1,\n    2\n  ]\n}', "nested structures are indented too"

assert from_json('{"a": 1}') == {"a": 1}, "an object becomes a dict"
assert from_json("[1, 2]") == [1, 2], "an array becomes a list"
assert from_json("null") is None, "null becomes None"
assert from_json("true") is True, "and true becomes True, capital and all"
assert from_json('"text"') == "text", "a bare string"
assert from_json(to_json({"a": 1, "b": [2, 3]})) == {"a": 1, "b": [2, 3]}, "a full round trip"

assert save_manifest(MANIFEST, {"table": "orders", "rows": 1500}) == MANIFEST, "save returns the path"
assert load_manifest(MANIFEST) == {"table": "orders", "rows": 1500}, "and it reads back identically"

save_manifest(MANIFEST, {"nested": {"deep": [1, {"x": None}]}})

assert load_manifest(MANIFEST) == {"nested": {"deep": [1, {"x": None}]}}, "arbitrarily nested data survives the trip"

save_manifest(MANIFEST, [])

assert load_manifest(MANIFEST) == [], "a top-level array is valid JSON too"

NUMERIC_KEYS = from_json(to_json({1: "orders", 2: "events"}))

assert NUMERIC_KEYS == {"1": "orders", "2": "events"}, "JSON keys are ALWAYS strings — the int keys came back as text"
assert 1 not in NUMERIC_KEYS, "so looking up the original int finds nothing"
assert "1" in NUMERIC_KEYS, "you have to ask for the string"

assert safe_json({"rows": 5}) == '{"rows": 5}', "ordinary values serialise normally"
assert safe_json({"when": None}) == '{"when": null}', "None is JSON's null"


class Stamp:
  def __str__(self):
    return "2026-01-04"


assert safe_json({"when": Stamp()}) == '{"when": "2026-01-04"}', "default=str rescues a type JSON has never heard of"

try:
  import json as _json
  _json.dumps({"when": Stamp()})
except TypeError:
  UNSERIALISABLE = "raises"
else:
  UNSERIALISABLE = "worked"

assert UNSERIALISABLE == "raises", "without default=, an unknown type is a TypeError"
