import heapq


def top_k(pairs, k):
  """The k biggest (name, rows) pairs, biggest first."""
  return heapq.nlargest(k, pairs, key=lambda pair: pair[1])


def bottom_k(pairs, k):
  """The k smallest, smallest first."""
  return heapq.nsmallest(k, pairs, key=lambda pair: pair[1])


def streaming_top_k(stream, k):
  """Keep only k items in memory, however long the stream is."""
  heap = []
  for name, rows in stream:
    if len(heap) < k:
      heapq.heappush(heap, (rows, name))
    elif rows > heap[0][0]:
      heapq.heapreplace(heap, (rows, name))
  return [(name, rows) for rows, name in sorted(heap, reverse=True)]


def high_water(stream, k):
  """The largest the working set ever got — proof it stays bounded."""
  heap = []
  biggest = 0
  for name, rows in stream:
    if len(heap) < k:
      heapq.heappush(heap, (rows, name))
    elif rows > heap[0][0]:
      heapq.heapreplace(heap, (rows, name))
    biggest = max(biggest, len(heap))
  return biggest


def merge_sorted(*streams):
  """Merge already-sorted streams into one, lazily."""
  return list(heapq.merge(*streams))
