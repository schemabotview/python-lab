from collections import deque

PARTNERS = {")": "(", "]": "[", "}": "{"}


def is_balanced(text):
  """Whether every bracket is closed by its own partner, in order."""
  stack = []
  for character in text:
    if character in "([{":
      stack.append(character)
    elif character in PARTNERS:
      if not stack or stack.pop() != PARTNERS[character]:
        return False
  return not stack


def unmatched_at(text):
  """Index of the first bracket that breaks the rule, or -1."""
  stack = []
  for index, character in enumerate(text):
    if character in "([{":
      stack.append((character, index))
    elif character in PARTNERS:
      if not stack or stack[-1][0] != PARTNERS[character]:
        return index
      stack.pop()
  if stack:
    return stack[0][1]
  return -1


def next_bigger(values):
  """For each value, the next larger one to its right — or -1."""
  answer = [-1] * len(values)
  stack = []
  for index, value in enumerate(values):
    while stack and values[stack[-1]] < value:
      answer[stack.pop()] = value
    stack.append(index)
  return answer


def simulate_queue(arrivals, capacity, per_tick):
  """Work a bounded queue. Returns (processed, dropped)."""
  queue = deque()
  processed = []
  dropped = 0
  for batch in arrivals:
    for job in batch:
      if len(queue) >= capacity:
        dropped += 1
      else:
        queue.append(job)
    for _ in range(per_tick):
      if not queue:
        break
      processed.append(queue.popleft())
  return processed, dropped
