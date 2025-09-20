#!/usr/bin/env python3
"""
NeoPaquet Language Parser

This module handles parsing of tokenized NeoPaquet source code into an Abstract Syntax Tree (AST).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Union, Any
from enum import Enum, auto

from lexer import Token, TokenType, Lexer, LexerError

# AST Node Types
class ASTNode(ABC):
    """Base class for all AST nodes."""
    pass

@dataclass
class Program(ASTNode):
    statements: List['Statement']

@dataclass 
class Statement(ASTNode):
    pass

@dataclass
class Expression(ASTNode):
    pass

# Expressions
@dataclass
class Literal(Expression):
    value: Any
    type_hint: Optional[str] = None

@dataclass
class Identifier(Expression):
    name: str

@dataclass
class BinaryOp(Expression):
    left: Expression
    operator: str
    right: Expression

@dataclass
class UnaryOp(Expression):
    operator: str
    operand: Expression

@dataclass
class FunctionCall(Expression):
    function: Expression
    arguments: List[Expression]

@dataclass
class MemberAccess(Expression):
    object: Expression
    member: str

# Statements
@dataclass
class LetStatement(Statement):
    name: str
    type_annotation: Optional[str]
    value: Optional[Expression]

@dataclass
class FunctionDefinition(Statement):
    name: str
    parameters: List['Parameter']
    return_type: Optional[str]
    body: List[Statement]

@dataclass
class Parameter:
    name: str
    type_annotation: str

@dataclass
class ReturnStatement(Statement):
    value: Optional[Expression]

@dataclass
class IfStatement(Statement):
    condition: Expression
    then_body: List[Statement]
    else_body: Optional[List[Statement]]

@dataclass
class WhileStatement(Statement):
    condition: Expression
    body: List[Statement]

@dataclass
class ForStatement(Statement):
    variable: str
    iterable: Expression
    body: List[Statement]

@dataclass
class ExpressionStatement(Statement):
    expression: Expression

@dataclass
class Block(Statement):
    statements: List[Statement]

@dataclass
class StructDefinition(Statement):
    name: str
    fields: List['StructField']

@dataclass
class StructField:
    name: str
    type_annotation: str

@dataclass
class ImportStatement(Statement):
    module_name: str
    from_package: Optional[str]
    version_constraint: Optional[str]
    alias: Optional[str]

@dataclass
class PackageDeclaration(Statement):
    name: str
    version: str
    dependencies: List['Dependency']
    exports: List[str]

@dataclass
class Dependency:
    package: str
    version_constraint: str

class ParseError(Exception):
    def __init__(self, message: str, token: Optional[Token] = None):
        self.message = message
        self.token = token
        if token:
            super().__init__(f"Parse error at line {token.line}, column {token.column}: {message}")
        else:
            super().__init__(f"Parse error: {message}")

class Parser:
    def __init__(self, tokens: List[Token]):
        # Filter out whitespace and comment tokens
        self.tokens = [t for t in tokens if t.type not in [TokenType.WHITESPACE, TokenType.COMMENT]]
        self.position = 0
        
    def current_token(self) -> Optional[Token]:
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]
    
    def peek_token(self, offset: int = 1) -> Optional[Token]:
        pos = self.position + offset
        if pos >= len(self.tokens):
            return None
        return self.tokens[pos]
    
    def advance(self):
        if self.position < len(self.tokens):
            self.position += 1
    
    def expect_token(self, expected_type: TokenType) -> Token:
        token = self.current_token()
        if not token or token.type != expected_type:
            expected_name = expected_type.name
            actual = token.type.name if token else "EOF"
            raise ParseError(f"Expected {expected_name}, got {actual}", token)
        
        self.advance()
        return token
    
    def match_token(self, *token_types: TokenType) -> bool:
        token = self.current_token()
        return token is not None and token.type in token_types
    
    def skip_newlines(self):
        while self.match_token(TokenType.NEWLINE):
            self.advance()
    
    def parse(self) -> Program:
        statements = []
        
        while self.current_token() and self.current_token().type != TokenType.EOF:
            self.skip_newlines()
            if self.current_token() and self.current_token().type != TokenType.EOF:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
        
        return Program(statements)
    
    def parse_statement(self) -> Optional[Statement]:
        token = self.current_token()
        if not token:
            return None
        
        if token.type == TokenType.LET:
            return self.parse_let_statement()
        elif token.type == TokenType.FN:
            return self.parse_function_definition()
        elif token.type == TokenType.RETURN:
            return self.parse_return_statement()
        elif token.type == TokenType.IF:
            return self.parse_if_statement()
        elif token.type == TokenType.WHILE:
            return self.parse_while_statement()
        elif token.type == TokenType.FOR:
            return self.parse_for_statement()
        elif token.type == TokenType.STRUCT:
            return self.parse_struct_definition()
        elif token.type == TokenType.IMPORT:
            return self.parse_import_statement()
        elif token.type == TokenType.PACKAGE:
            return self.parse_package_declaration()
        elif token.type == TokenType.LBRACE:
            return self.parse_block()
        else:
            return self.parse_expression_statement()
    
    def parse_let_statement(self) -> LetStatement:
        self.expect_token(TokenType.LET)
        
        name_token = self.expect_token(TokenType.IDENTIFIER)
        name = name_token.value
        
        type_annotation = None
        if self.match_token(TokenType.COLON):
            self.advance()
            type_token = self.expect_token(TokenType.IDENTIFIER)
            type_annotation = type_token.value
        
        value = None
        if self.match_token(TokenType.ASSIGN):
            self.advance()
            value = self.parse_expression()
        
        return LetStatement(name, type_annotation, value)
    
    def parse_function_definition(self) -> FunctionDefinition:
        self.expect_token(TokenType.FN)
        
        name_token = self.expect_token(TokenType.IDENTIFIER)
        name = name_token.value
        
        self.expect_token(TokenType.LPAREN)
        
        parameters = []
        while not self.match_token(TokenType.RPAREN):
            param_name = self.expect_token(TokenType.IDENTIFIER).value
            self.expect_token(TokenType.COLON)
            param_type = self.expect_token(TokenType.IDENTIFIER).value
            parameters.append(Parameter(param_name, param_type))
            
            if self.match_token(TokenType.COMMA):
                self.advance()
            elif not self.match_token(TokenType.RPAREN):
                raise ParseError("Expected ',' or ')' in parameter list", self.current_token())
        
        self.expect_token(TokenType.RPAREN)
        
        return_type = None
        if self.match_token(TokenType.ARROW):
            self.advance()
            return_type = self.expect_token(TokenType.IDENTIFIER).value
        
        self.expect_token(TokenType.LBRACE)
        body = self.parse_block_body()
        self.expect_token(TokenType.RBRACE)
        
        return FunctionDefinition(name, parameters, return_type, body)
    
    def parse_return_statement(self) -> ReturnStatement:
        self.expect_token(TokenType.RETURN)
        
        value = None
        if not self.match_token(TokenType.NEWLINE, TokenType.RBRACE, TokenType.EOF):
            value = self.parse_expression()
        
        return ReturnStatement(value)
    
    def parse_if_statement(self) -> IfStatement:
        self.expect_token(TokenType.IF)
        condition = self.parse_expression()
        
        self.expect_token(TokenType.LBRACE)
        then_body = self.parse_block_body()
        self.expect_token(TokenType.RBRACE)
        
        else_body = None
        if self.match_token(TokenType.ELSE):
            self.advance()
            self.expect_token(TokenType.LBRACE)
            else_body = self.parse_block_body()
            self.expect_token(TokenType.RBRACE)
        
        return IfStatement(condition, then_body, else_body)
    
    def parse_while_statement(self) -> WhileStatement:
        self.expect_token(TokenType.WHILE)
        condition = self.parse_expression()
        
        self.expect_token(TokenType.LBRACE)
        body = self.parse_block_body()
        self.expect_token(TokenType.RBRACE)
        
        return WhileStatement(condition, body)
    
    def parse_for_statement(self) -> ForStatement:
        self.expect_token(TokenType.FOR)
        variable = self.expect_token(TokenType.IDENTIFIER).value
        # This is a simplified for loop, real implementation would handle more complex syntax
        iterable = self.parse_expression()
        
        self.expect_token(TokenType.LBRACE)
        body = self.parse_block_body()
        self.expect_token(TokenType.RBRACE)
        
        return ForStatement(variable, iterable, body)
    
    def parse_struct_definition(self) -> StructDefinition:
        self.expect_token(TokenType.STRUCT)
        name = self.expect_token(TokenType.IDENTIFIER).value
        
        self.expect_token(TokenType.LBRACE)
        fields = []
        
        while not self.match_token(TokenType.RBRACE):
            self.skip_newlines()
            if self.match_token(TokenType.RBRACE):
                break
                
            field_name = self.expect_token(TokenType.IDENTIFIER).value
            self.expect_token(TokenType.COLON)
            field_type = self.expect_token(TokenType.IDENTIFIER).value
            fields.append(StructField(field_name, field_type))
            
            if self.match_token(TokenType.COMMA):
                self.advance()
            
            self.skip_newlines()
        
        self.expect_token(TokenType.RBRACE)
        return StructDefinition(name, fields)
    
    def parse_import_statement(self) -> ImportStatement:
        self.expect_token(TokenType.IMPORT)
        
        module_name = self.expect_token(TokenType.IDENTIFIER).value
        
        from_package = None
        if self.match_token(TokenType.FROM):
            self.advance()
            from_package = self.expect_token(TokenType.STRING).value
        
        version_constraint = None
        if self.match_token(TokenType.VERSION):
            self.advance()
            version_constraint = self.expect_token(TokenType.STRING).value
        
        return ImportStatement(module_name, from_package, version_constraint, None)
    
    def parse_package_declaration(self) -> PackageDeclaration:
        self.expect_token(TokenType.PACKAGE)
        name = self.expect_token(TokenType.IDENTIFIER).value
        self.expect_token(TokenType.VERSION)
        version = self.expect_token(TokenType.STRING).value
        
        self.expect_token(TokenType.LBRACE)
        
        dependencies = []
        exports = []
        
        while not self.match_token(TokenType.RBRACE):
            self.skip_newlines()
            if self.match_token(TokenType.RBRACE):
                break
                
            if self.match_token(TokenType.DEPENDENCIES):
                self.advance()
                self.expect_token(TokenType.LBRACE)
                # Parse dependencies (simplified)
                while not self.match_token(TokenType.RBRACE):
                    self.skip_newlines()
                    if self.match_token(TokenType.RBRACE):
                        break
                    dep_name = self.expect_token(TokenType.STRING).value
                    self.expect_token(TokenType.VERSION)
                    dep_version = self.expect_token(TokenType.STRING).value
                    dependencies.append(Dependency(dep_name, dep_version))
                    
                    if self.match_token(TokenType.COMMA):
                        self.advance()
                    
                    self.skip_newlines()
                self.expect_token(TokenType.RBRACE)
            
            elif self.match_token(TokenType.EXPORTS):
                self.advance()
                self.expect_token(TokenType.LBRACE)
                # Parse exports (simplified)
                while not self.match_token(TokenType.RBRACE):
                    self.skip_newlines()
                    if self.match_token(TokenType.RBRACE):
                        break
                    export_name = self.expect_token(TokenType.IDENTIFIER).value
                    exports.append(export_name)
                    
                    if self.match_token(TokenType.COMMA):
                        self.advance()
                    
                    self.skip_newlines()
                self.expect_token(TokenType.RBRACE)
        
        self.expect_token(TokenType.RBRACE)
        return PackageDeclaration(name, version, dependencies, exports)
    
    def parse_block(self) -> Block:
        self.expect_token(TokenType.LBRACE)
        statements = self.parse_block_body()
        self.expect_token(TokenType.RBRACE)
        return Block(statements)
    
    def parse_block_body(self) -> List[Statement]:
        statements = []
        
        while not self.match_token(TokenType.RBRACE, TokenType.EOF):
            self.skip_newlines()
            if self.match_token(TokenType.RBRACE, TokenType.EOF):
                break
            
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        return statements
    
    def parse_expression_statement(self) -> ExpressionStatement:
        expr = self.parse_expression()
        return ExpressionStatement(expr)
    
    def parse_expression(self) -> Expression:
        return self.parse_logical_or()
    
    def parse_logical_or(self) -> Expression:
        expr = self.parse_logical_and()
        
        while self.match_token(TokenType.OR):
            operator = self.current_token().value
            self.advance()
            right = self.parse_logical_and()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_logical_and(self) -> Expression:
        expr = self.parse_equality()
        
        while self.match_token(TokenType.AND):
            operator = self.current_token().value
            self.advance()
            right = self.parse_equality()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_equality(self) -> Expression:
        expr = self.parse_comparison()
        
        while self.match_token(TokenType.EQUAL, TokenType.NOT_EQUAL):
            operator = self.current_token().value
            self.advance()
            right = self.parse_comparison()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_comparison(self) -> Expression:
        expr = self.parse_addition()
        
        while self.match_token(TokenType.LESS, TokenType.LESS_EQUAL, 
                              TokenType.GREATER, TokenType.GREATER_EQUAL):
            operator = self.current_token().value
            self.advance()
            right = self.parse_addition()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_addition(self) -> Expression:
        expr = self.parse_multiplication()
        
        while self.match_token(TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token().value
            self.advance()
            right = self.parse_multiplication()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_multiplication(self) -> Expression:
        expr = self.parse_unary()
        
        while self.match_token(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self.current_token().value
            self.advance()
            right = self.parse_unary()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_unary(self) -> Expression:
        if self.match_token(TokenType.NOT, TokenType.MINUS):
            operator = self.current_token().value
            self.advance()
            operand = self.parse_unary()
            return UnaryOp(operator, operand)
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> Expression:
        expr = self.parse_primary()
        
        while True:
            if self.match_token(TokenType.LPAREN):
                # Function call
                self.advance()
                arguments = []
                
                while not self.match_token(TokenType.RPAREN):
                    arguments.append(self.parse_expression())
                    if self.match_token(TokenType.COMMA):
                        self.advance()
                    elif not self.match_token(TokenType.RPAREN):
                        raise ParseError("Expected ',' or ')' in function call", self.current_token())
                
                self.expect_token(TokenType.RPAREN)
                expr = FunctionCall(expr, arguments)
            
            elif self.match_token(TokenType.DOT):
                # Member access
                self.advance()
                member = self.expect_token(TokenType.IDENTIFIER).value
                expr = MemberAccess(expr, member)
            
            else:
                break
        
        return expr
    
    def parse_primary(self) -> Expression:
        token = self.current_token()
        
        if not token:
            raise ParseError("Unexpected end of input")
        
        if token.type == TokenType.INTEGER:
            self.advance()
            return Literal(int(token.value))
        
        elif token.type == TokenType.FLOAT:
            self.advance()
            return Literal(float(token.value))
        
        elif token.type == TokenType.STRING:
            self.advance()
            return Literal(token.value)
        
        elif token.type == TokenType.BOOLEAN:
            self.advance()
            return Literal(token.value == 'true')
        
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(token.value)
        
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect_token(TokenType.RPAREN)
            return expr
        
        else:
            raise ParseError(f"Unexpected token: {token.type.name}", token)

def parse_source(source: str) -> Program:
    """Convenience function to parse source code."""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()

if __name__ == "__main__":
    # Simple test
    test_code = '''
    let name = "NeoPaquet"
    let version: String = "1.0.0"
    
    fn greet(name: String) -> String {
        return "Hello, " + name + "!"
    }
    
    struct User {
        name: String,
        age: u32
    }
    '''
    
    try:
        ast = parse_source(test_code)
        print(f"Parsed {len(ast.statements)} statements:")
        for i, stmt in enumerate(ast.statements):
            print(f"  {i+1}. {type(stmt).__name__}")
    except (LexerError, ParseError) as e:
        print(f"Error: {e}")