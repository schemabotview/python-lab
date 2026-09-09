# Word Frequency

Write a function `word_frequency(text)` that returns a dictionary mapping each
word in `text` to the number of times it appears.

Words are separated by whitespace. Counting is **case-insensitive**, so
`"The"` and `"the"` are the same word, and the keys in your result are
lowercase.

## Example

```python
word_frequency("the cat and the hat")
# {"the": 2, "cat": 1, "and": 1, "hat": 1}
```

## Notes

- Empty text returns an empty dictionary.
- Any amount of whitespace separates words — `str.split()` with no argument
  handles runs of spaces, tabs and newlines for you.
- Ignore punctuation entirely: `"hat."` and `"hat"` are different words here.
  Keeping the rule simple keeps the exercise about dictionaries.
