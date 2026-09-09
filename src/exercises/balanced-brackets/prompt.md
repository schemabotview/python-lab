# Balanced Brackets

Write a function `is_balanced(text)` that returns `True` if every bracket in
`text` is closed by a matching bracket in the right order, and `False`
otherwise.

Three kinds of bracket count: `()`, `[]` and `{}`. Any other character is
ignored.

## Examples

```python
is_balanced("(a + b)")       # True
is_balanced("{[()]}")        # True
is_balanced("(]")            # False  — wrong closer
is_balanced("(()")           # False  — never closed
is_balanced(")(")            # False  — closed before opened
```

## Notes

- An empty string is balanced.
- Order matters: `"([)]"` is **not** balanced, because the `)` closes a
  bracket that isn't the most recent one still open.
- A list used as a stack is the natural tool. Push each opener; when you meet a
  closer, the top of the stack must be its partner.
