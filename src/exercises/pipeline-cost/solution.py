# Rates the finance team publishes. Name them here, in UPPER_CASE.
COMPUTE_RATE = 0.55
STORAGE_RATE = 0.023
EGRESS_RATE = 0.09


def cost_report(compute_hours, storage_gb, egress_gb, discount_percent):
  """Return the nightly cost summary as one multi-line string."""
  compute = compute_hours * COMPUTE_RATE
  storage = storage_gb * STORAGE_RATE
  egress = egress_gb * EGRESS_RATE
  subtotal = compute + storage + egress
  discount = subtotal * discount_percent / 100
  total = subtotal - discount
  return "\n".join([
    "--- Nightly Run Cost ---",
    f"Compute ({compute_hours:.1f}h): ${compute:.2f}",
    f"Storage ({storage_gb:.1f}GB): ${storage:.2f}",
    f"Egress ({egress_gb:.1f}GB): ${egress:.2f}",
    "-" * 24,
    f"Subtotal: ${subtotal:.2f}",
    f"Discount ({discount_percent}%): ${discount:.2f}",
    f"Total: ${total:.2f}",
  ])


def parse_env(raw_hours, raw_retries, raw_debug):
  """Return (hours, retries, debug) converted from their env-var strings."""
  return float(raw_hours), int(raw_retries), raw_debug.lower() == "true"


def describe(value):
  """Return the kind of a config value: int, float, str, bool, none or other."""
  if value is None:
    return "none"
  # bool before int: every bool is also an int, so the int check would swallow it.
  if isinstance(value, bool):
    return "bool"
  if isinstance(value, int):
    return "int"
  if isinstance(value, float):
    return "float"
  if isinstance(value, str):
    return "str"
  return "other"


def to_iso(stamp):
  """Turn a DD-MM-YYYY stamp into YYYY-MM-DD."""
  day, month, year = stamp.split("-")
  return f"{year}-{month}-{day}"


def split_fields(line):
  """Split a CSV line into (table_name, [the remaining fields])."""
  table, *rest = line.split(",")
  return table, rest
