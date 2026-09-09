assert word_frequency("") == {}, "empty text has no words"
assert word_frequency("hello") == {"hello": 1}, "a single word appears once"
assert word_frequency("the cat and the hat") == {
  "the": 2,
  "cat": 1,
  "and": 1,
  "hat": 1,
}, "repeated words are counted"
assert word_frequency("The the THE") == {"the": 3}, "counting is case-insensitive"
assert word_frequency("a  b\tc\nd") == {
  "a": 1,
  "b": 1,
  "c": 1,
  "d": 1,
}, "any whitespace separates words"
