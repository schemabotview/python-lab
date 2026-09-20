# The Data Directory

A `Path` is an object, not a string. Everything here returns a plain `str` or
`list` so it can be asserted on.

## `build_path(root, *parts)`

```python
build_path("/tmp", "lab", "orders.csv")   # "/tmp/lab/orders.csv"
```

## `describe(path)`

What a path knows about itself, **without touching the disk**.

```python
describe("/tmp/lab/orders.csv")
```

```text
Name: orders.csv
Stem: orders
Suffix: .csv
Parent: /tmp/lab
```

## `ensure_dir(path)`

Creates the directory **and its parents**, returns `True`, and doesn't fail if
it already exists.

## `save(path, text)` / `load(path)`

Whole-file write and read, with no `open()`. `save` returns the number of
characters written.

## `find_csvs(root, recursive)`

The **names** of the `.csv` files, sorted. `recursive=False` looks one level;
`True` goes all the way down.

## Notes

- **Join with `/`, never with string concatenation.** `Path("data") / "x.csv"`
  gets the separator right on every OS, and can't produce the `//` or missing
  `/` that string-building does.
- **A path knows itself.** `.name`, `.stem`, `.suffix` and `.parent` are pure
  string work — no disk access, so they answer for files that don't exist.
- **`.suffix` is only the last extension.** `archive.tar.gz` has stem
  `archive.tar` and suffix `.gz`. A test pins that, because it surprises people
  who expect `.tar.gz`.
- **`mkdir(parents=True, exist_ok=True)` is the combination you almost always
  want.** Without `parents` a nested path raises; without `exist_ok` running
  twice raises. A test calls `ensure_dir` twice on purpose.
- **`glob` is one level, `rglob` recurses.** The test builds an `archive/`
  subfolder precisely so the two give different answers — choosing the wrong
  one silently misses files or silently finds too many.
- `read_text`/`write_text` are the one-call form. Reach for `open()` only when
  you need to stream rather than take the file whole.
