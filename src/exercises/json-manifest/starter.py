import json


def to_json(config):
  """Pretty, stable JSON text — the kind that diffs cleanly in review."""
  pass


def from_json(text):
  """Parse JSON text back into Python objects."""
  pass


def save_manifest(path, data):
  """Straight to a file — no intermediate string."""
  pass


def load_manifest(path):
  """Straight from a file."""
  pass


def safe_json(value):
  """Serialise anything, falling back to str() for types JSON has never heard of."""
  pass
