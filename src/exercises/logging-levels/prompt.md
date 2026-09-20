# Levelled Diagnostics

`print` debugging with a volume knob. `ListHandler` is written for you — it
collects formatted lines into a list so the tests can read them.

## `make_logger(name, level, sink)`

Returns a logger with:

- the given **threshold**
- a `ListHandler` writing into `sink`
- the format `"%(levelname)s %(message)s"`

Also clear any existing handlers and set `propagate = False`, so repeated calls
and the root logger don't double up.

## The four log calls

| Function | Level | Message |
| --- | --- | --- |
| `log_run(log, table, rows)` | INFO | `loaded 1500 rows into orders` |
| `log_slow(log, table, seconds)` | WARNING | `events took 90s` |
| `log_failure(log, table, error)` | ERROR | `users failed: timeout` |
| `log_crash(log, table)` | ERROR + traceback | `orders crashed` |

```python
sink = []
log = make_logger("app", logging.DEBUG, sink)
log_run(log, "orders", 1500)
sink   # ['INFO loaded 1500 rows into orders']
```

## Notes

- **The threshold is the whole idea.** The tests call the *same* `log_run` twice
   — once through a `DEBUG` logger and once through a `WARNING` one — and get a
  line the first time and nothing the second. DEBUG in development, WARNING in
  production, and **no code changes** between them.
- **Use `log.info("... %s", value)`, not an f-string.** The formatting is
  deferred until the record is actually emitted, so a message below the
  threshold costs nothing. The last test passes an object whose `__str__`
  **raises**: with lazy `%` args it is never called, and with an f-string the
  test would blow up at the call site. That's the difference made visible.
- **`log.exception(...)` belongs inside an `except` block.** It logs at ERROR
  *and* appends the traceback automatically — tests check both the message and
  that `ZeroDivisionError` and `Traceback` made it into the line.
- **Clearing handlers matters more than it looks.** `getLogger` returns the
  *same* logger for the same name, so calling `make_logger` twice without
  clearing attaches a second handler and every line appears twice — a genuinely
  confusing bug to meet in the wild.
- Libraries log and say nothing about where it goes; the application attaches
  handlers and sets policy. That separation is why `basicConfig` belongs in your
  entry point and nowhere else.
