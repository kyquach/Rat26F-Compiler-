from NFSM import NFSM
from dataclasses import dataclass
@dataclass
class Token:
    token: str
    lexeme: str


class Lexer:
    def __init__(self, identifier_fsm, integer_fsm, real_fsm):
            self.identifier_fsm = identifier_fsm
            self.integer_fsm = integer_fsm
            self.real_fsm = real_fsm

    def Lexer(self, source_code):                                      #IMPLEMENTE LEXER CODE!!!!!!!!!!!!!!!!!!
        self.source_code = source_code
        self.position = 0
        self.tokens = []
