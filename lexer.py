from NFSM import NFSM
from dataclasses import dataclass


@dataclass
class Token:
    token: str
    lexeme: str
    line: int = 1


KEYWORDS = {"function", "integer", "boolean", "real", "if", "else", "fi",
            "while", "return", "get", "put", "true", "false"}
SEPARATORS = {"(", ")", "{", "}", ",", ";", "@"}
OPERATORS = {"==", "!=", "<=", ">=", "+", "-", "*", "/", "=", "<", ">"}


def build_identifier_fsm():
    transitions = {
        (0, "letter"): {1},
        (1, "letter"): {1},
        (1, "digit"): {1},
        (1, "_"): {1},
    }
    return NFSM({0, 1}, {"letter", "digit", "_"}, transitions, 0, {1})


def build_integer_fsm():
    transitions = {
        (0, "digit"): {1},
        (1, "digit"): {1},
    }
    return NFSM({0, 1}, {"digit"}, transitions, 0, {1})


def build_real_fsm():
    transitions = {
        (0, "digit"): {0},
        (0, "."): {1},
        (1, "digit"): {2},
        (2, "digit"): {2},
    }
    return NFSM({0, 1, 2}, {"digit", "."}, transitions, 0, {2})


class Lexer:
    def __init__(self, source_code, identifier_fsm=None, integer_fsm=None, real_fsm=None):
        self.source_code = source_code
        self.position = 0
        self.line_number = 1
        self.tokens = []
        self.identifier_fsm = identifier_fsm or build_identifier_fsm()
        self.integer_fsm = integer_fsm or build_integer_fsm()
        self.real_fsm = real_fsm or build_real_fsm()

    def skip_whitespace_and_comments(self):
        src = self.source_code
        while self.position < len(src):
            if src[self.position].isspace():
                if src[self.position] == "\n":
                    self.line_number += 1
                self.position += 1
            # I skip "!=" here because it is an operator, not the start of a comment
            elif src[self.position] == "!" and src[self.position:self.position + 2] != "!=":
                end = src.find("!", self.position + 1)
                comment_end = len(src) if end == -1 else end + 1
                # I count the newlines inside the comment so line numbers stay right
                self.line_number += src.count("\n", self.position, comment_end)
                self.position = comment_end
            else:
                break

    def lexer(self):
        self.skip_whitespace_and_comments()
        src, start, line = self.source_code, self.position, self.line_number
        if start >= len(src):
            return None

        # Collect the run of letters, digits, "_" and "." starting here, then
        # find the longest prefix of it that one of the FSMs accepts.
        end = start
        while end < len(src) and self.identifier_fsm.classify_character(src[end]) is not None:
            end += 1
        while end > start:
            lexeme = src[start:end]
            if self.identifier_fsm.is_accepted(lexeme):
                self.position = end
                kind = "keyword" if lexeme.lower() in KEYWORDS else "identifier"
                return Token(kind, lexeme, line)
            if self.integer_fsm.is_accepted(lexeme):
                self.position = end
                return Token("integer", lexeme, line)
            if self.real_fsm.is_accepted(lexeme):
                self.position = end
                return Token("real", lexeme, line)
            end -= 1

        # Operators (two-character ones first), then separators.
        if src[start:start + 2] in OPERATORS:
            self.position = start + 2
            return Token("operator", src[start:start + 2], line)
        self.position = start + 1
        if src[start] in OPERATORS:
            return Token("operator", src[start], line)
        if src[start] in SEPARATORS:
            return Token("separator", src[start], line)
        return Token("unknown", src[start], line)

    def tokenize(self):
        self.position = 0
        self.line_number = 1
        self.tokens = []
        while True:
            token = self.lexer()
            if token is None:
                break
            self.tokens.append((token.token, token.lexeme))
        return self.tokens
