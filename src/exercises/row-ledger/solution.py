def lookup(counts, table):
  """Rows loaded for a table — 0 for one that never ran."""
  return counts.get(table, 0)


def merge_runs(first, second):
  """Merge a later run over an earlier one. Neither input is touched."""
  merged = dict(first)
  merged.update(second)
  return merged


def add_row(index, table, row_id):
  """File a row id under its table, starting the list if it's the first."""
  updated = {}
  for key, value in index.items():
    updated[key] = list(value)
  updated.setdefault(table, []).append(row_id)
  return updated


def ledger_report(counts):
  """One line per table in name order, then the total."""
  lines = []
  for table in sorted(counts):
    lines.append(f"{table}: {counts[table]}")
  total = 0
  for rows in counts.values():
    total += rows
  lines.append(f"TOTAL: {total}")
  return "\n".join(lines)


def drop_table(counts, table):
  """Remove a table from the ledger. Dropping one that isn't there is fine."""
  updated = dict(counts)
  updated.pop(table, None)
  return updated


def column_order(pairs):
  """Build a schema from (name, type) pairs and report the column order."""
  schema = {}
  for name, kind in pairs:
    schema[name] = kind
  return list(schema)
