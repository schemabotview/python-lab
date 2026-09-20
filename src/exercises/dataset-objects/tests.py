assert Dataset("orders").name == "orders", "the name is per-instance"
assert Dataset("orders").columns == [], "a fresh dataset has no columns"
assert Dataset("orders").region == "eu-west-1", "the region is read off the class"
assert Dataset.region == "eu-west-1", "and can be read from the class itself"

ORDERS = Dataset("orders")
EVENTS = Dataset("events")
ORDERS.add_column("id")

assert ORDERS.columns == ["id"], "the column landed on this dataset"
assert EVENTS.columns == [], "and NOT on the other — a list in the class body would show 'id' here too"
assert ORDERS.add_column("amount") == ["id", "amount"], "add_column returns the list so far"
assert EVENTS.columns == [], "still independent after a second add"

assert same_object(ORDERS, ORDERS) is True, "one object, two names"
assert same_object(Dataset("orders"), Dataset("orders")) is False, "two datasets with the same name are still two objects"
assert same_object(ORDERS, EVENTS) is False, "plainly different"

assert same_type(ORDERS, Dataset) is True, "an instance of Dataset"
assert same_type("orders", Dataset) is False, "a string is not"
assert same_type(5, int) is True, "isinstance works on built-in types too"

assert attributes(Dataset("orders")) == ["columns", "name"], "the two attributes __init__ set"
assert "region" not in attributes(Dataset("orders")), "a class attribute is not in the instance's own vars()"

DYNAMIC = Dataset("orders")

assert tag(DYNAMIC, "owner", "data-team") == ["columns", "name", "owner"], "attributes can be added after construction"
assert DYNAMIC.owner == "data-team", "and read back like any other"
assert attributes(Dataset("fresh")) == ["columns", "name"], "the new attribute is on that one object, not the class"

SHADOWED = Dataset("orders")
SHADOWED.region = "us-east-1"

assert SHADOWED.region == "us-east-1", "assigning through the instance creates an instance attribute"
assert Dataset.region == "eu-west-1", "which shadows the class attribute without changing it"
assert Dataset("other").region == "eu-west-1", "so every other dataset still sees the shared value"
