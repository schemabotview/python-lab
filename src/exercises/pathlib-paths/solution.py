from pathlib import Path


def build_path(root, *parts):
  """Join a path the safe way — no string concatenation."""
  path = Path(root)
  for part in parts:
    path = path / part
  return str(path)


def describe(path):
  """What a path knows about itself, without touching the disk."""
  target = Path(path)
  return "\n".join([
    f"Name: {target.name}",
    f"Stem: {target.stem}",
    f"Suffix: {target.suffix}",
    f"Parent: {target.parent}",
  ])


def ensure_dir(path):
  """Create a directory, and its parents, without failing if it exists."""
  Path(path).mkdir(parents=True, exist_ok=True)
  return Path(path).is_dir()


def save(path, text):
  """Whole-file write, with no open() in sight."""
  return Path(path).write_text(text, encoding="utf-8")


def load(path):
  """Whole-file read."""
  return Path(path).read_text(encoding="utf-8")


def find_csvs(root, recursive):
  """CSV files in a folder — one level, or all the way down."""
  target = Path(root)
  found = target.rglob("*.csv") if recursive else target.glob("*.csv")
  return sorted(item.name for item in found)
