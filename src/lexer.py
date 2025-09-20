#!/usr/bin/env python3
"""
NeoPaquet Language Lexer

This module handles tokenization of NeoPaquet source code.
It breaks down source text into tokens that can be processed by the parser.
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Iterator

class TokenType(Enum):
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    
    # Keywords
    LET = auto()
    FN = auto()
    STRUCT = auto()
    ENUM = auto()
    MATCH = auto()
    IF = auto()
    ELSE = auto()
    FOR = auto()
    WHILE = auto()
    RETURN = auto()
    IMPORT = auto()
    FROM = auto()
    PACKAGE = auto()
    VERSION = auto()
    DEPENDENCIES = auto()
    EXPORTS = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    ASSIGN = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    ARROW = auto()
    
    # Special
    NEWLINE = auto()
    EOF = auto()
    WHITESPACE = auto()
    COMMENT = auto()

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexer error at line {line}, column {column}: {message}")

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        # Keywords mapping
        self.keywords = {
            'let': TokenType.LET,
            'fn': TokenType.FN,
            'struct': TokenType.STRUCT,
            'enum': TokenType.ENUM,
            'match': TokenType.MATCH,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'for': TokenType.FOR,
            'while': TokenType.WHILE,
            'return': TokenType.RETURN,
            'import': TokenType.IMPORT,
            'from': TokenType.FROM,
            'package': TokenType.PACKAGE,
            'version': TokenType.VERSION,
            'dependencies': TokenType.DEPENDENCIES,
            'exports': TokenType.EXPORTS,
            'true': TokenType.BOOLEAN,
            'false': TokenType.BOOLEAN,
        }
    
    def current_char(self) -> Optional[str]:
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        if self.position < len(self.source):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def read_string(self) -> str:
        quote_char = self.current_char()
        self.advance()  # Skip opening quote
        
        value = ""
        while self.current_char() and self.current_char() != quote_char:
            char = self.current_char()
            if char == '\\':
                self.advance()
                next_char = self.current_char()
                if next_char == 'n':
                    value += '\n'
                elif next_char == 't':
                    value += '\t'
                elif next_char == 'r':
                    value += '\r'
                elif next_char == '\\':
                    value += '\\'
                elif next_char == quote_char:
                    value += quote_char
                else:
                    value += next_char or ''
                self.advance()
            else:
                value += char
                self.advance()
        
        if not self.current_char():
            raise LexerError("Unterminated string literal", self.line, self.column)
        
        self.advance()  # Skip closing quote
        return value
    
    def read_number(self) -> tuple[str, TokenType]:
        value = ""
        is_float = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if is_float:
                    break  # Second dot, not part of this number
                is_float = True
            value += self.current_char()
            self.advance()
        
        return value, TokenType.FLOAT if is_float else TokenType.INTEGER
    
    def read_identifier(self) -> str:
        value = ""
        while (self.current_char() and 
               (self.current_char().isalnum() or self.current_char() in '_-')):
            value += self.current_char()
            self.advance()
        return value
    
    def read_comment(self) -> str:
        value = ""
        self.advance()  # Skip first '/'
        self.advance()  # Skip second '/'
        
        while self.current_char() and self.current_char() != '\n':
            value += self.current_char()
            self.advance()
        
        return value
    
    def tokenize(self) -> List[Token]:
        while self.position < len(self.source):
            start_line = self.line
            start_column = self.column
            
            char = self.current_char()
            
            if not char:
                break
            
            # Skip whitespace
            if char in ' \t\r':
                self.skip_whitespace()
                continue
            
            # Newlines
            if char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, char, start_line, start_column))
                self.advance()
                continue
            
            # Comments
            if char == '/' and self.peek_char() == '/':
                comment_value = self.read_comment()
                self.tokens.append(Token(TokenType.COMMENT, comment_value, start_line, start_column))
                continue
            
            # Strings
            if char in '"\'':
                string_value = self.read_string()
                self.tokens.append(Token(TokenType.STRING, string_value, start_line, start_column))
                continue
            
            # Numbers
            if char.isdigit():
                number_value, number_type = self.read_number()
                self.tokens.append(Token(number_type, number_value, start_line, start_column))
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                identifier = self.read_identifier()
                token_type = self.keywords.get(identifier, TokenType.IDENTIFIER)
                self.tokens.append(Token(token_type, identifier, start_line, start_column))
                continue
            
            # Two-character operators
            if char == '=' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQUAL, '==', start_line, start_column))
                continue
            
            if char == '!' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', start_line, start_column))
                continue
            
            if char == '<' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', start_line, start_column))
                continue
            
            if char == '>' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', start_line, start_column))
                continue
            
            if char == '-' and self.peek_char() == '>':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ARROW, '->', start_line, start_column))
                continue
            
            if char == '&' and self.peek_char() == '&':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.AND, '&&', start_line, start_column))
                continue
            
            if char == '|' and self.peek_char() == '|':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.OR, '||', start_line, start_column))
                continue
            
            # Single-character tokens
            single_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
                '=': TokenType.ASSIGN,
                '<': TokenType.LESS,
                '>': TokenType.GREATER,
                '!': TokenType.NOT,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ';': TokenType.SEMICOLON,
                ',': TokenType.COMMA,
                '.': TokenType.DOT,
                ':': TokenType.COLON,
            }
            
            if char in single_char_tokens:
                token_type = single_char_tokens[char]
                self.tokens.append(Token(token_type, char, start_line, start_column))
                self.advance()
                continue
            
            # Unknown character
            raise LexerError(f"Unexpected character: '{char}'", start_line, start_column)
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens

def lex_source(source: str) -> List[Token]:
    """Convenience function to tokenize source code."""
    lexer = Lexer(source)
    return lexer.tokenize()

if __name__ == "__main__":
    # Simple test
    test_code = '''
    let name = "NeoPaquet"
    let version: Version = "1.0.0"
    
    fn greet(name: String) -> String {
        return "Hello, " + name + "!"
    }
    '''
    
    try:
        tokens = lex_source(test_code)
        for token in tokens:
            if token.type not in [TokenType.WHITESPACE, TokenType.NEWLINE, TokenType.EOF]:
                print(f"{token.type.name}: '{token.value}' at {token.line}:{token.column}")
    except LexerError as e:
        print(f"Error: {e}")