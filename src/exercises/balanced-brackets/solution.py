def is_balanced(text):
  """Return True if every bracket in `text` is properly closed."""
  partners = {")": "(", "]": "[", "}": "{"}
  stack = []
  for character in text:
    if character in "([{":
      stack.append(character)
    elif character in partners:
      if not stack or stack.pop() != partners[character]:
        return False
  return not stack
