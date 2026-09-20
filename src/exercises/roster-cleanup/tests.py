assert len(roster_report(["Ali", "Sara", "Ali", "Bilal", "", "Zara", "Sara", "Hamza"]).splitlines()) == 6, "six lines: roster, count, first, last, middle, final"
assert roster_report(["Ali", "Sara", "Ali", "Bilal", "", "Zara", "Sara", "Hamza"]).splitlines()[0] == "Roster: ['Ali', 'Bilal', 'Hamza', 'Sara', 'Zara']", "sorted, with the blank and the duplicates gone"
assert roster_report(["Ali", "Sara", "Ali", "Bilal", "", "Zara", "Sara", "Hamza"]).splitlines()[1] == "Unique students: 5", "eight entries become five students"
assert roster_report(["Ali", "Sara", "Ali", "Bilal", "", "Zara", "Sara", "Hamza"]).splitlines()[2] == "First: Ali", "first alphabetically, at index 0"
assert roster_report(["Ali", "Sara", "Ali", "Bilal", "", "Zara", "Sara", "Hamza"]).splitlines()[3] == "Last: Zara", "last alphabetically, at index -1"
assert roster_report(["Ali", "Sara", "Ali", "Bilal", "", "Zara", "Sara", "Hamza"]).splitlines()[4] == "Middle: Hamza", "5 // 2 is 2, which is Hamza"
assert roster_report(["Ali", "Sara", "Ali", "Bilal", "", "Zara", "Sara", "Hamza"]).splitlines()[5] == "Final: ['Ali', 'Bilal', 'Hamza', 'Sara', 'Zara', 'Noor']", "Noor joins at the end"

assert roster_report(["Zoe", "", "Adam", "Mia", "Zoe"]).splitlines()[0] == "Roster: ['Adam', 'Mia', 'Zoe']", "a different roster is cleaned the same way"
assert roster_report(["Zoe", "", "Adam", "Mia", "Zoe"]).splitlines()[1] == "Unique students: 3", "the count comes from the cleaned list"
assert roster_report(["Zoe", "", "Adam", "Mia", "Zoe"]).splitlines()[4] == "Middle: Mia", "3 // 2 is 1 — the middle must come from len()"

assert roster_report(["B", "A", "", "C", "D"]).splitlines()[2] == "First: A", "first of four"
assert roster_report(["B", "A", "", "C", "D"]).splitlines()[3] == "Last: D", "last of four"
assert roster_report(["B", "A", "", "C", "D"]).splitlines()[4] == "Middle: C", "4 // 2 is 2, the later of the two middle names"

CALLERS_LIST = ["Ali", "", "Ali", "Bilal"]

assert roster_report(CALLERS_LIST).splitlines()[0] == "Roster: ['Ali', 'Bilal']", "the short roster is cleaned correctly"
assert CALLERS_LIST == ["Ali", "", "Ali", "Bilal"], "work on a copy — the caller's list must survive the call"
