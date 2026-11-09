import sys

from lexer import Lexer
from Syntax_analyzer import SyntaxAnalyzer


def main():
    # Input and output files (optional command-line arguments)
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.txt"

    # Read source code from input file
    with open(input_file, "r", encoding="utf-8") as file:
        source_code = file.read()

    # Get the lexer from Assignment 1
    lexer = Lexer(source_code)

    # The parser writes each token, lexeme and production rule to the output file
    with open(output_file, "w", encoding="utf-8") as file:
        success = SyntaxAnalyzer(lexer, file, print_rules=True).parse()

    if success:
        print(f"Parsing complete. Results written to {output_file}")
    else:
        print(f"Syntax error found. See {output_file}")


if __name__ == "__main__":
    main()