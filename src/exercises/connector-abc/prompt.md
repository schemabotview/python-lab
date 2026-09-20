# The Connector Contract

An abstract base class says *what* every connector must do and leaves *how* to
each one.

## `Connector(ABC)`

`name()` and `fetch()` are already marked `@abstractmethod` — they declare the
contract and have no body.

`report()` is **concrete**: write it once here, built on the two methods
subclasses are obliged to supply.

```python
"postgres: 3 rows"
```

## The two concrete connectors

- `PostgresConnector` → `name()` is `"postgres"`, `fetch()` returns `[1, 2, 3]`
- `EmptyConnector` → `name()` is `"empty"`, `fetch()` returns `[]`

Neither writes its own `report()`.

## `can_fetch(value)`

Whether a value satisfies the `Fetchable` protocol — declared for you.

```python
can_fetch(PostgresConnector())   # True
can_fetch("just a string")       # False
```

## Notes

- **The language enforces the contract.** `Connector()` raises `TypeError`,
  and so does a subclass that forgot one of the abstract methods. A test builds
  a deliberately half-finished subclass to prove it. Crucially the error fires
  **at construction** — not deep inside a later call, in production, at 3am.
- **An ABC can carry concrete methods too**, and `report()` is the reason that
  matters: shared logic lives in one place, written against methods that don't
  exist yet, and every subclass inherits it by filling in the gaps. Both
  connectors get `report()` for free and neither could have written it better.
- **ABC is nominal, `Protocol` is structural.** A subclass must explicitly
  inherit an ABC to count. A `Protocol` asks only whether the right methods are
  there — a test defines a class inheriting from nothing at all, and
  `can_fetch` still says `True`. That is duck typing made checkable.
- `@runtime_checkable` is what lets `isinstance` be used against a `Protocol`
  at all; without it a Protocol is a static-checking tool only.
- Use an ABC when you own the hierarchy and want the guarantee; use a `Protocol`
  when you want to accept types you don't control.
