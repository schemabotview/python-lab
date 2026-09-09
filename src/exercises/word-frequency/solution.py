def word_frequency(text):
  """Return a dict mapping each lowercased word in `text` to its count."""
  counts = {}
  for word in text.lower().split():
    counts[word] = counts.get(word, 0) + 1
  return counts
