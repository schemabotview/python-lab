# Class Roster Cleanup

A roster was typed in by hand, so some names appear twice and one entry came out
blank. Write `roster_report(roster)` that cleans it up and returns a summary as
one multi-line string.

Clean the roster in this order:

1. Remove the one blank `""` entry.
2. Drop duplicates, then sort alphabetically — still a list.
3. Add `"Noor"` to the end.

## Example

```python
roster_report(["Ali", "Sara", "Ali", "Bilal", "", "Zara", "Sara", "Hamza"])
```

returns this string:

```text
Roster: ['Ali', 'Bilal', 'Hamza', 'Sara', 'Zara']
Unique students: 5
First: Ali
Last: Zara
Middle: Hamza
Final: ['Ali', 'Bilal', 'Hamza', 'Sara', 'Zara', 'Noor']
```

`Roster` is the cleaned, sorted list *before* Noor joins; `Final` is after.
`First`, `Last` and `Middle` all describe that sorted list — `Middle` is the
name at index `len(names) // 2`.

## Notes

- An f-string prints a list the same way the interpreter does, quotes and all,
  so `f"Roster: {names}"` already gives you the format above.
- De-duplicate with `set`, and sort with `sorted()`. Don't write a loop that
  checks each name against the ones before it — that is the O(n²) shape the
  `list` lesson warns about, and `set` exists to avoid it.
- Compute `Middle` from `len(...)`. An index typed in by hand will fail the
  test with a longer roster.
- **Don't damage the caller's list.** `.remove()` changes the list in place, and
  the list you were handed belongs to whoever called you. Take a copy first —
  `list(roster)` or `roster[:]` — and work on that. One test checks the argument
  is unchanged afterwards.
