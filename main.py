import sys

from test_cases import TestCases
from lexer import Lexer

def main():
    # Input and output files (optional command-line arguments)
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.txt"

    # Read source code from input file
    with open(input_file, "r") as file:
        source_code = file.read()

    # Create lexer
    lexer = Lexer(source_code)

    # open output file for writing results
    with open(output_file, "w") as file:

        # generating tokens using the lexer
        tokens = lexer.tokenize()

        # printing tokens and lexemes to the output file
        for token, lexeme in tokens:
            file.write(f"Token: {token:<20} Lexeme: {lexeme}\n")

    print(f"Lexing complete. Results written to {output_file}")


if __name__ == "__main__":
    main()
