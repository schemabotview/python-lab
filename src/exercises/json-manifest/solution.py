import json


def to_json(config):
  """Pretty, stable JSON text — the kind that diffs cleanly in review."""
  return json.dumps(config, indent=2, sort_keys=True)


def from_json(text):
  """Parse JSON text back into Python objects."""
  return json.loads(text)


def save_manifest(path, data):
  """Straight to a file — no intermediate string."""
  with open(path, "w", encoding="utf-8") as handle:
    json.dump(data, handle, indent=2, sort_keys=True)
  return path


def load_manifest(path):
  """Straight from a file."""
  with open(path, encoding="utf-8") as handle:
    return json.load(handle)


def safe_json(value):
  """Serialise anything, falling back to str() for types JSON has never heard of."""
  return json.dumps(value, default=str, sort_keys=True)
