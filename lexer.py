# npaquetc/lexer.py
# NeoPaquet Lexer
# Translates .np source into tokens for parsing
# Author: NeoPaquet Project

import re
from typing import List, Tuple

# -----------------------------
# Token Types
# -----------------------------
TOKEN_TYPES = [
    "KEYWORD", "IDENTIFIER", "NUMBER", "STRING",
    "SYMBOL", "OPERATOR", "COMMENT", "EOF"
]

# NeoPaquet keywords
KEYWORDS = {
    "src", "run", "Task", "complete", "Start", "setup", "done",
    "@func", "go", "job", "operation", "if", "else", "loop",
    "try", "catch", "isolate", "clean", "retry", "dismiss",
    "print", "return"
}

# Symbols
SYMBOLS = {
    "(", ")", "{", "}", "[", "]", "<", ">", ":", ";", "|"
}

# Operators
OPERATORS = {
    "+", "-", "*", "/", "%", "=", "==", "!=", "<=", ">=",
    "&&", "||", "->"
}

# -----------------------------
# Token Structure
# -----------------------------
class Token:
    def __init__(self, type_: str, value: str, line: int, col: int):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, col={self.col})"


# -----------------------------
# Lexer
# -----------------------------
class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.length = len(source)

    def _peek(self, k: int = 0) -> str:
        if self.pos + k < self.length:
            return self.source[self.pos + k]
        return "\0"

    def _advance(self) -> str:
        ch = self._peek()
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _skip_whitespace(self):
        while self._peek().isspace():
            self._advance()

    def _skip_comment(self):
        # Single-line comment --
        if self._peek() == "-" and self._peek(1) == "-":
            while self._peek() not in ("\n", "\0"):
                self._advance()
            return True

        # Multi-line comment ; ... ;
        if self._peek() == ";":
            self._advance()
            while not (self._peek() == ";" or self._peek() == "\0"):
                self._advance()
            if self._peek() == ";":
                self._advance()
            return True

        return False

    def _string(self) -> str:
        self._advance()  # skip opening "
        start = self.pos
        while self._peek() not in ("\"", "\0"):
            self._advance()
        value = self.source[start:self.pos]
        self._advance()  # closing "
        return value

    def _number(self) -> str:
        start = self.pos
        while self._peek().isalnum():  # allows 0-9, a, b (dodecagram base-12)
            self._advance()
        return self.source[start:self.pos]

    def _identifier(self) -> str:
        start = self.pos
        while self._peek().isalnum() or self._peek() in ("_", "-"):
            self._advance()
        return self.source[start:self.pos]

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []

        while self.pos < self.length:
            self._skip_whitespace()

            # Handle comments
            if self._skip_comment():
                continue

            ch = self._peek()

            # End of file
            if ch == "\0":
                break

            # String literal
            if ch == "\"":
                value = self._string()
                tokens.append(Token("STRING", value, self.line, self.col))
                continue

            # Number literal (dodecagram 0-9,a,b)
            if ch.isdigit() or ch in {"a", "b"}:
                value = self._number()
                tokens.append(Token("NUMBER", value, self.line, self.col))
                continue

            # Identifier / Keyword
            if ch.isalpha() or ch == "@" or ch == "<" or ch == ">":
                value = self._identifier()
                if value in KEYWORDS:
                    tokens.append(Token("KEYWORD", value, self.line, self.col))
                else:
                    tokens.append(Token("IDENTIFIER", value, self.line, self.col))
                continue

            # Symbols
            if ch in SYMBOLS:
                tokens.append(Token("SYMBOL", self._advance(), self.line, self.col))
                continue

            # Operators (multi-char)
            two = ch + self._peek(1)
            if two in OPERATORS:
                tokens.append(Token("OPERATOR", two, self.line, self.col))
                self._advance()
                self._advance()
                continue

            # Operators (single-char)
            if ch in OPERATORS:
                tokens.append(Token("OPERATOR", self._advance(), self.line, self.col))
                continue

            # Unknown char
            raise SyntaxError(f"Unexpected character {ch} at line {self.line}, col {self.col}")

        tokens.append(Token("EOF", "", self.line, self.col))
        return tokens


# -----------------------------
# Debug
# -----------------------------
if __name__ == "__main__":
    code = '''
    -- Hello World in NeoPaquet
    src () "stdout" { print ["Hello NeoPaquet"] } run
    '''
    lexer = Lexer(code)
    for token in lexer.tokenize():
        print(token)
