"""
    [A-Za-z\d]: This denotes a character class that matches any uppercase letter (A-Z),
    lowercase letter (a-z), or digit (\d is shorthand for [0-9]).
    {8,20}: This specifies the quantifier, meaning the previous character class (i.e., any uppercase letter,
    lowercase letter, or digit) should occur at least 8 times and at most 20 times.

    ^ and $ used together (^pattern$), it means the entire string must match the specified pattern
"""
password_pattern = r"^[A-Za-z\d]{8,20}$"