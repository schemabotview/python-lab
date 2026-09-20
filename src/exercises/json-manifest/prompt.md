# Config & Manifest

JSON is how a pipeline talks to everything else.

## `to_json(config)`

Indented **two spaces**, keys **sorted**.

```python
to_json({"b": 1, "a": 2})
```

```json
{
  "a": 2,
  "b": 1
}
```

## `from_json(text)` → the Python objects

## `save_manifest(path, data)` / `load_manifest(path)`

Straight to and from a file, with **no intermediate string**. `save_manifest`
returns the path, and writes with the same indent and sorting.

## `safe_json(value)`

Serialises anything, falling back to `str()` for types JSON doesn't know.
Sorted keys, no indent.

## Notes

- **The `s` means string.** `dumps`/`loads` work with text; `dump`/`load`
  (no `s`) work with an open file. Getting them the wrong way round is the most
  common `json` mistake there is, and the error message doesn't make it obvious.
- **`sort_keys=True` is what makes a manifest reviewable.** Without it, two
  runs producing identical data can write it in different orders, and every
  diff is noise.
- **All JSON keys are strings.** A dict with `int` keys round-trips to a dict
  with `str` keys, silently — `{1: "orders"}` comes back as `{"1": "orders"}`,
  so the original lookup stops working. A test pins both halves: the string key
  is there and the int key is not.
- **`default=str` is the escape hatch** for types JSON has never heard of — a
  `datetime`, a `Decimal`, your own class. Without it you get a `TypeError`, and
  a test proves it. With it, the value goes out as whatever `str()` produced,
  which is fine to *write* and is on you to parse back.
- The data models line up almost exactly: `dict`↔object, `list`↔array,
  `None`↔`null`, `True`↔`true`. Almost — tuples come back as lists, because
  JSON has no tuple.
