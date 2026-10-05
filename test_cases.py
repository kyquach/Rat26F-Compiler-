from lexer import NFSM, Lexer, build_identifier_fsm, build_integer_fsm, build_real_fsm


class TestCases:
    """
    Test cases for the Rat26F Lexer FSMs.

    Tests:
        1. Identifier FSM
        2. Integer FSM
        3. Real Number FSM
        4. Invalid inputs
        5. Example Rat26F source code
    """

    def __init__(self, identifier_fsm, integer_fsm, real_fsm):
        self.identifier_fsm = identifier_fsm
        self.integer_fsm = integer_fsm
        self.real_fsm = real_fsm
        self.passed = 0
        self.failed = 0

    def check(self, description, actual, expected):
        """Record and print one PASS or FAIL result."""
        if actual == expected:
            self.passed += 1
            print(f"PASS  {description}")
        else:
            self.failed += 1
            print(f"FAIL  {description}: expected {expected}, got {actual}")

    def check_fsm(self, name, fsm, accepted, rejected):
        """Check that an FSM accepts and rejects the given strings."""
        for text in accepted:
            self.check(f"{name} accepts {text!r}", fsm.is_accepted(text), True)
        for text in rejected:
            self.check(f"{name} rejects {text!r}", fsm.is_accepted(text), False)

    def test_identifier_fsm(self):
        self.check_fsm("identifier", self.identifier_fsm,
                       accepted=["a", "count", "count_1", "R2_value", "x9_", "Max_Val"],
                       rejected=["", "_abc", "9lives", "a.b", "a-b", "123"])

    def test_integer_fsm(self):
        self.check_fsm("integer", self.integer_fsm,
                       accepted=["0", "7", "123", "000456"],
                       rejected=["", "12a", "1.5", "-3", "1_000"])

    def test_real_fsm(self):
        self.check_fsm("real", self.real_fsm,
                       accepted=["123.00", ".001", "0.5", "2.25"],
                       rejected=["", "123.", ".", "123", "1.2.3", "1.a"])

    def test_invalid_inputs(self):
        """Characters and lexemes that are not part of Rat26F."""
        self.check("'$' is unknown", Lexer("$").tokenize(), [("unknown", "$")])
        self.check("'123.' is an integer then unknown '.'", Lexer("123.").tokenize(),
                   [("integer", "123"), ("unknown", ".")])
        self.check("'_abc' is unknown '_' then an identifier", Lexer("_abc").tokenize(),
                   [("unknown", "_"), ("identifier", "abc")])
        self.check("'12ab' is an integer then an identifier", Lexer("12ab").tokenize(),
                   [("integer", "12"), ("identifier", "ab")])

    def test_source_code(self):
        """A short Rat26F program with a comment, keywords, operators and a real."""
        source = "! sample ! while (low <= high) { low = low + .5; }"
        expected = [
            ("keyword", "while"), ("separator", "("), ("identifier", "low"),
            ("operator", "<="), ("identifier", "high"), ("separator", ")"),
            ("separator", "{"), ("identifier", "low"), ("operator", "="),
            ("identifier", "low"), ("operator", "+"), ("real", ".5"),
            ("separator", ";"), ("separator", "}"),
        ]
        self.check("sample program tokens", Lexer(source).tokenize(), expected)
        self.check("keywords ignore case", Lexer("WHILE If").tokenize(),
                   [("keyword", "WHILE"), ("keyword", "If")])
        self.check("'!=' is an operator, not a comment", Lexer("a != b").tokenize(),
                   [("identifier", "a"), ("operator", "!="), ("identifier", "b")])

    def run_all(self):
        """Run every test and print a summary. Returns True if all passed."""
        self.test_identifier_fsm()
        self.test_integer_fsm()
        self.test_real_fsm()
        self.test_invalid_inputs()
        self.test_source_code()
        print(f"\n{self.passed} passed, {self.failed} failed")
        return self.failed == 0


if __name__ == "__main__":
    TestCases(build_identifier_fsm(), build_integer_fsm(), build_real_fsm()).run_all()
