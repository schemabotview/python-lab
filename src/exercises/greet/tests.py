assert greet("Ada") == "Hello, Ada!", 'greet("Ada") should be "Hello, Ada!"'
assert greet("grace") == "Hello, grace!", "the name keeps its own capitalisation"
assert greet("") == "Hello, !", "an empty name still produces a greeting"
