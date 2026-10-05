# Rat26F Compiler

Group project for CPSC 323 (Fall 2026). The compiler is built in three
assignments. This repository currently contains Assignment 1, the lexical
analyzer for the Rat26F language.

## What the lexer does

It reads a Rat26F source file and writes one line per token, showing the token
type and its lexeme. The token types are keyword, identifier, integer, real,
operator and separator. Comments (`! like this !`) and white space are skipped,
and any character that is not part of Rat26F is reported as unknown.

Identifiers, integers and reals are recognized with finite state machines:

| Token      | Regular expression  |
|------------|---------------------|
| Identifier | `L (L \| D \| _)*`  |
| Integer    | `D+`                |
| Real       | `D* . D+`           |

## Files

| File             | Purpose                                                    |
|------------------|------------------------------------------------------------|
| `main.py`        | Reads the source file, runs the lexer, writes the output   |
| `lexer.py`       | The three state machines and the `Lexer` class             |
| `NFSM.py`        | Nondeterministic finite state machine simulator            |
| `test_cases.py`  | Checks for the state machines and the lexer                |
| `tests/`         | Three Rat26F test programs (`test1`, `test2`, `test3`)     |
| `outputs/`       | The lexer's output for each test program                   |

## How to run

Python 3 is required. No other libraries are needed.

Run the lexer by giving an input file and an output file:

```
python3 main.py tests/test1 outputs/test1_output.txt
```

With no file names, it reads `input.txt` and writes `output.txt`:

```
python3 main.py
```

On Windows, use `python` if `python3` is not recognized.

## Running the checks

```
python3 test_cases.py
```

This tests each state machine against valid and invalid lexemes, then runs the
lexer on sample Rat26F code. It prints PASS or FAIL for each check and a total
at the end.

## Sample output

```
Token: keyword              Lexeme: integer
Token: identifier           Lexeme: count_1
Token: separator            Lexeme: ,
Token: identifier           Lexeme: total
Token: separator            Lexeme: ;
```
