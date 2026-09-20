def read_rows(rows):
  """The simplest generator: hand back one row at a time."""
  for row in rows:
    yield row


def chunked(rows, size):
  """Batch a stream into lists of `size`, with a short final batch."""
  batch = []
  for row in rows:
    batch.append(row)
    if len(batch) == size:
      yield batch
      batch = []
  if batch:
    yield batch


def run_ids(prefix):
  """An endless stream of ids. Safe, because nothing is produced until asked."""
  number = 1
  while True:
    yield f"{prefix}-{number}"
    number += 1


def take(stream, count):
  """The first `count` values of any stream, however long it is."""
  collected = []
  # Check the count BEFORE pulling: asking for 0 from an endless stream must
  # return immediately, not loop forever waiting to reach a length it passed.
  if count <= 0:
    return collected
  for value in stream:
    collected.append(value)
    if len(collected) == count:
      break
  return collected


def merge_streams(*streams):
  """Re-emit every stream's items in turn, without a manual inner loop."""
  for stream in streams:
    yield from stream
