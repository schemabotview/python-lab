from pathlib import Path


def build_path(root, *parts):
  """Join a path the safe way — no string concatenation."""
  pass


def describe(path):
  """What a path knows about itself, without touching the disk."""
  pass


def ensure_dir(path):
  """Create a directory, and its parents, without failing if it exists."""
  pass


def save(path, text):
  """Whole-file write, with no open() in sight."""
  pass


def load(path):
  """Whole-file read."""
  pass


def find_csvs(root, recursive):
  """CSV files in a folder — one level, or all the way down."""
  pass
