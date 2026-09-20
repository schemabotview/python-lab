# The Run Log File

Real files, on a real filesystem — Python in the browser has one, in memory.
The tests write everything they read, so nothing here depends on a file you
can't see.

| Function | Does |
| --- | --- |
| `write_log(path, lines)` | writes the log **fresh**, returns how many lines |
| `append_log(path, line)` | adds one line, returns it |
| `read_all(path)` | the whole file as one string |
| `count_lines(path)` | counts lines **without** loading the file |
| `first_error(path)` | the first line starting `ERROR`, or `""` |

Each line you write gets its own `\n`. `first_error` returns the line
**without** its trailing newline.

```python
write_log(path, ["INFO started", "INFO loading"])   # 2
read_all(path)   # "INFO started\nINFO loading\n"
```

## Notes

- **`"w"` truncates the file before writing a single byte.** Not "overwrites
  what overlaps" — wipes. A test writes two lines, writes one line, and checks
  the first two are gone. This is how people lose data with one wrong mode
  letter; `"a"` is what you want to add.
- **Always use `with`.** It's the context manager from the previous track, and
  it guarantees the file is closed even if the code inside raises. Without it a
  written file can sit unflushed and look empty to the next reader.
- **Writing is exactly what you give it.** The module adds nothing — no
  newlines, no separators. If you want a line to end, you write the `\n`.
- **`for line in handle` is lazy — one line at a time.** `count_lines` and
  `first_error` are the two shapes that matter: one walks everything without
  ever holding it all, the other stops the moment it has an answer. Both work
  unchanged on a file too big to fit in memory, which `.read()` does not.
- **Pass `encoding="utf-8"` explicitly.** The default depends on the machine, so
  code that works on yours can mangle text on someone else's.
- The lines keep their commas and quotes exactly as given — a plain text file
  escapes nothing. That becomes the whole problem in the CSV exercise.
