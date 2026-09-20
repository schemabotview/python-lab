from pathlib import Path

ROOT = "/tmp/lab/data"

assert build_path("/tmp", "lab", "orders.csv") == "/tmp/lab/orders.csv", "the separators are added for you"
assert build_path("/tmp") == "/tmp", "no parts to join"
assert build_path("data", "raw", "x.json") == "data/raw/x.json", "a relative path works the same way"

assert describe("/tmp/lab/orders.csv").splitlines()[0] == "Name: orders.csv", "the filename with its extension"
assert describe("/tmp/lab/orders.csv").splitlines()[1] == "Stem: orders", "the filename without it"
assert describe("/tmp/lab/orders.csv").splitlines()[2] == "Suffix: .csv", "the extension, dot included"
assert describe("/tmp/lab/orders.csv").splitlines()[3] == "Parent: /tmp/lab", "the folder it sits in"
assert describe("/tmp/notes").splitlines()[2] == "Suffix: ", "a file with no extension has an empty suffix"
assert describe("/tmp/archive.tar.gz").splitlines()[1] == "Stem: archive.tar", "only the LAST extension is the suffix"

assert ensure_dir(ROOT) is True, "the directory is created"
assert ensure_dir(ROOT) is True, "and creating it again is not an error"
assert ensure_dir("/tmp/lab/deep/nested/tree") is True, "parents are created too"

assert save(f"{ROOT}/orders.csv", "id,amount\n1,5\n") == 14, "write_text returns how many characters it wrote"
assert load(f"{ROOT}/orders.csv") == "id,amount\n1,5\n", "and read_text gives them straight back"
assert save(f"{ROOT}/empty.csv", "") == 0, "an empty write"
assert load(f"{ROOT}/empty.csv") == "", "reads back empty"

save(f"{ROOT}/events.csv", "x")
save(f"{ROOT}/notes.txt", "x")
ensure_dir(f"{ROOT}/archive")
save(f"{ROOT}/archive/old.csv", "x")

assert find_csvs(ROOT, False) == ["empty.csv", "events.csv", "orders.csv"], "glob looks one level only — archive/old.csv is not here"
assert find_csvs(ROOT, True) == ["empty.csv", "events.csv", "old.csv", "orders.csv"], "rglob recurses into subfolders"
assert "notes.txt" not in find_csvs(ROOT, True), "the pattern excludes other extensions"
assert find_csvs(f"{ROOT}/archive", False) == ["old.csv"], "a folder with one match"

ensure_dir("/tmp/lab/nothing")

assert find_csvs("/tmp/lab/nothing", True) == [], "a folder with no matches gives an empty list, not an error"

assert Path(build_path(ROOT, "orders.csv")).exists() is True, "a path can query the disk about itself"
assert Path(build_path(ROOT, "missing.csv")).exists() is False, "and say no"
