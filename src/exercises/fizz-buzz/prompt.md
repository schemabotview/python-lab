# FizzBuzz

Write a function `fizzbuzz(n)` that returns a list with one entry for each
number from `1` to `n` inclusive:

| Condition | Entry |
| --- | --- |
| divisible by 3 and 5 | `"FizzBuzz"` |
| divisible by 3 | `"Fizz"` |
| divisible by 5 | `"Buzz"` |
| anything else | the number itself, as an `int` |

## Example

```python
fizzbuzz(15)
# [1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8,
#  "Fizz", "Buzz", 11, "Fizz", 13, 14, "FizzBuzz"]
```

## Notes

- Numbers stay as integers, not strings — `1`, not `"1"`.
- `fizzbuzz(0)` returns an empty list.
- Check divisibility by 15 *first*, or the `"FizzBuzz"` case never fires.
