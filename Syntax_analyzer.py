QUALIFIERS = {"integer", "boolean", "real"}


class ParserError(Exception):
    pass


class SyntaxAnalyzer:
    def __init__(self, lexer, output_file, print_rules=True):
        self.lexer = lexer
        self.output_file = output_file
        self.print_rules = print_rules
        self.current_token = None

    # Helpers shared by every part of the parser

    def next_token(self):
        self.current_token = self.lexer.lexer()
        if self.current_token is not None:
            token, lexeme = self.current_token.token, self.current_token.lexeme
            self.output_file.write(f"Token: {token:<20} Lexeme: {lexeme}\n")

    def print_rule(self, rule):
        if self.print_rules:
            self.output_file.write(f"     {rule}\n")

    def check(self, lexeme):
        return self.current_token is not None and self.current_token.lexeme.lower() == lexeme

    def check_type(self, token_type):
        return self.current_token is not None and self.current_token.token == token_type

    def is_qualifier(self):
        return self.check_type("keyword") and self.current_token.lexeme.lower() in QUALIFIERS

    def match(self, lexeme):
        if not self.check(lexeme):
            self.error(f"'{lexeme}'")
        self.next_token()

    def match_type(self, token_type):
        if not self.check_type(token_type):
            self.error(token_type)
        self.next_token()

    def error(self, expected):
        if self.current_token is None:
            raise ParserError(f"Syntax error on line {self.lexer.line_number}: "
                              f"expected {expected}, but reached the end of the file")
        token = self.current_token
        raise ParserError(f"Syntax error on line {token.line}: expected {expected}, "
                          f"but found {token.token} '{token.lexeme}'")

    def parse(self):
        self.next_token()
        try:
            self.parse_rat26f()
        except ParserError as message:
            self.output_file.write(f"\n{message}\n")
            print(message)
            return False
        return True

    # Part 1: program structure, functions and declarations

    def parse_rat26f(self):
        self.print_rule("<Rat26F> -> <Opt Function Definitions> @ <Opt Declaration List> <Statement List> @")
        self.parse_opt_function_definitions()
        self.match("@")
        self.parse_opt_declaration_list()
        self.parse_statement_list()
        self.match("@")
        if self.current_token is not None:
            self.error("end of file")

    def parse_opt_function_definitions(self):
        if self.check("function"):
            self.print_rule("<Opt Function Definitions> -> <Function Definitions>")
            self.parse_function_definitions()
        else:
            self.print_rule("<Opt Function Definitions> -> <Empty>")
            self.parse_empty()

    def parse_function_definitions(self):
        self.print_rule("<Function Definitions> -> <Function> <Function Definitions Prime>")
        self.parse_function()
        self.parse_function_definitions_prime()

    def parse_function_definitions_prime(self):
        if self.check("function"):
            self.print_rule("<Function Definitions Prime> -> <Function Definitions>")
            self.parse_function_definitions()
        else:
            self.print_rule("<Function Definitions Prime> -> ε")

    def parse_function(self):
        self.print_rule("<Function> -> function <Identifier> ( <Opt Parameter List> ) "
                        "<Opt Declaration List> <Body>")
        self.match("function")
        self.match_type("identifier")
        self.match("(")
        self.parse_opt_parameter_list()
        self.match(")")
        self.parse_opt_declaration_list()
        self.parse_body()

    def parse_opt_parameter_list(self):
        if self.check_type("identifier"):
            self.print_rule("<Opt Parameter List> -> <Parameter List>")
            self.parse_parameter_list()
        else:
            self.print_rule("<Opt Parameter List> -> <Empty>")
            self.parse_empty()

    def parse_parameter_list(self):
        self.print_rule("<Parameter List> -> <Parameter> <Parameter List Prime>")
        self.parse_parameter()
        self.parse_parameter_list_prime()

    def parse_parameter_list_prime(self):
        if self.check(","):
            self.print_rule("<Parameter List Prime> -> , <Parameter List>")
            self.match(",")
            self.parse_parameter_list()
        else:
            self.print_rule("<Parameter List Prime> -> ε")

    def parse_parameter(self):
        self.print_rule("<Parameter> -> <IDs> <Qualifier>")
        self.parse_ids()
        self.parse_qualifier()

    def parse_qualifier(self):
        if not self.is_qualifier():
            self.error("integer, boolean or real")
        self.print_rule(f"<Qualifier> -> {self.current_token.lexeme.lower()}")
        self.next_token()

    def parse_body(self):
        self.print_rule("<Body> -> { <Statement List> }")
        self.match("{")
        self.parse_statement_list()
        self.match("}")

    def parse_opt_declaration_list(self):
        if self.is_qualifier():
            self.print_rule("<Opt Declaration List> -> <Declaration List>")
            self.parse_declaration_list()
        else:
            self.print_rule("<Opt Declaration List> -> <Empty>")
            self.parse_empty()

    def parse_declaration_list(self):
        self.print_rule("<Declaration List> -> <Declaration> ; <Declaration List Prime>")
        self.parse_declaration()
        self.match(";")
        self.parse_declaration_list_prime()

    def parse_declaration_list_prime(self):
        if self.is_qualifier():
            self.print_rule("<Declaration List Prime> -> <Declaration List>")
            self.parse_declaration_list()
        else:
            self.print_rule("<Declaration List Prime> -> ε")

    def parse_declaration(self):
        self.print_rule("<Declaration> -> <Qualifier> <IDs>")
        self.parse_qualifier()
        self.parse_ids()

    def parse_ids(self):
        self.print_rule("<IDs> -> <Identifier> <IDs Prime>")
        self.match_type("identifier")
        self.parse_ids_prime()

    def parse_ids_prime(self):
        if self.check(","):
            self.print_rule("<IDs Prime> -> , <IDs>")
            self.match(",")
            self.parse_ids()
        else:
            self.print_rule("<IDs Prime> -> ε")

    def parse_empty(self):
        self.print_rule("<Empty> -> ε")

    # Part 2: statements

    def parse_statement_list(self):
        # yall implement this part when you do your part
        pass

    def parse_statement(self):
        # yall implement this part when you do your part
        pass

    def parse_compound(self):
        # yall implement this part when you do your part
        pass

    def parse_assign(self):
        # yall implement this part when you do your part
        pass

    def parse_if(self):
        # yall implement this part when you do your part
        pass

    def parse_return(self):
        # yall implement this part when you do your part
        pass

    def parse_print(self):
        # yall implement this part when you do your part
        pass

    def parse_scan(self):
        # yall implement this part when you do your part
        pass

    def parse_while(self):
        # yall implement this part when you do your part
        pass

    def parse_condition(self):
        # yall implement this part when you do your part
        pass

    def parse_relop(self):
        # yall implement this part when you do your part
        pass

    # Part 3: expressions

    def parse_expression(self):
        # yall implement this part when you do your part
        pass

    def parse_term(self):
        # yall implement this part when you do your part
        pass

    def parse_factor(self):
        # yall implement this part when you do your part
        pass

    def parse_primary(self):
        # yall implement this part when you do your part
        pass
