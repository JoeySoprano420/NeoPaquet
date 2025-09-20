#!/usr/bin/env python3
"""
NeoPaquet Language Error Checker

This module performs semantic analysis and error checking on the AST.
It checks for type errors, undefined variables, and other semantic issues.
"""

from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass
from enum import Enum, auto

from parser import (
    ASTNode, Program, Statement, Expression, 
    LetStatement, FunctionDefinition, ReturnStatement,
    IfStatement, WhileStatement, ForStatement, ExpressionStatement,
    Block, StructDefinition, ImportStatement, PackageDeclaration,
    Literal, Identifier, BinaryOp, UnaryOp, FunctionCall, MemberAccess,
    Parameter, StructField, Dependency
)

class ErrorType(Enum):
    TYPE_ERROR = auto()
    UNDEFINED_VARIABLE = auto()
    UNDEFINED_FUNCTION = auto()
    UNDEFINED_TYPE = auto()
    REDEFINITION = auto()
    INVALID_OPERATION = auto()
    SYNTAX_ERROR = auto()
    SEMANTIC_ERROR = auto()

@dataclass
class SemanticError:
    type: ErrorType
    message: str
    node: Optional[ASTNode] = None
    line: Optional[int] = None
    column: Optional[int] = None

@dataclass
class Symbol:
    name: str
    type: str
    defined: bool = True
    used: bool = False

class FunctionSymbol(Symbol):
    def __init__(self, name: str, type_name: str, parameters: List[Parameter], return_type: Optional[str], defined: bool = True, used: bool = False):
        super().__init__(name, type_name, defined, used)
        self.parameters = parameters
        self.return_type = return_type

class StructSymbol(Symbol):
    def __init__(self, name: str, type_name: str, fields: List[StructField], defined: bool = True, used: bool = False):
        super().__init__(name, type_name, defined, used)
        self.fields = fields

class Scope:
    def __init__(self, parent: Optional['Scope'] = None):
        self.parent = parent
        self.symbols: Dict[str, Symbol] = {}
    
    def define(self, name: str, symbol: Symbol) -> bool:
        if name in self.symbols:
            return False  # Already defined in this scope
        self.symbols[name] = symbol
        return True
    
    def lookup(self, name: str) -> Optional[Symbol]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None
    
    def mark_used(self, name: str):
        symbol = self.lookup(name)
        if symbol:
            symbol.used = True

class ErrorChecker:
    def __init__(self):
        self.errors: List[SemanticError] = []
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.current_function_return_type: Optional[str] = None
        
        # Built-in types
        self.built_in_types = {
            'String', 'i32', 'u32', 'i64', 'u64', 'f32', 'f64', 'bool', 'Version'
        }
        
        # Add built-in functions
        self._add_built_ins()
    
    def _add_built_ins(self):
        """Add built-in functions and types to the global scope."""
        # Built-in functions
        print_fn = FunctionSymbol("print", "void", [Parameter("message", "String")], "void")
        self.global_scope.define("print", print_fn)
        
        len_fn = FunctionSymbol("len", "u32", [Parameter("s", "String")], "u32")
        self.global_scope.define("len", len_fn)
    
    def enter_scope(self) -> Scope:
        new_scope = Scope(self.current_scope)
        self.current_scope = new_scope
        return new_scope
    
    def exit_scope(self):
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
    
    def add_error(self, error_type: ErrorType, message: str, node: Optional[ASTNode] = None):
        self.errors.append(SemanticError(error_type, message, node))
    
    def is_valid_type(self, type_name: str) -> bool:
        """Check if a type name is valid (built-in or user-defined)."""
        if type_name in self.built_in_types:
            return True
        
        # Check if it's a user-defined struct
        symbol = self.global_scope.lookup(type_name)
        return symbol is not None and isinstance(symbol, StructSymbol)
    
    def get_expression_type(self, expr: Expression) -> Optional[str]:
        """Determine the type of an expression."""
        if isinstance(expr, Literal):
            if isinstance(expr.value, int):
                return "i32"
            elif isinstance(expr.value, float):
                return "f64"
            elif isinstance(expr.value, str):
                return "String"
            elif isinstance(expr.value, bool):
                return "bool"
        
        elif isinstance(expr, Identifier):
            symbol = self.current_scope.lookup(expr.name)
            if symbol:
                self.current_scope.mark_used(expr.name)
                return symbol.type
            else:
                self.add_error(ErrorType.UNDEFINED_VARIABLE, f"Undefined variable: {expr.name}", expr)
                return None
        
        elif isinstance(expr, BinaryOp):
            left_type = self.get_expression_type(expr.left)
            right_type = self.get_expression_type(expr.right)
            
            if left_type is None or right_type is None:
                return None
            
            # Type checking for binary operations
            if expr.operator in ['+', '-', '*', '/', '%']:
                if left_type == right_type and left_type in ['i32', 'u32', 'i64', 'u64', 'f32', 'f64']:
                    return left_type
                elif expr.operator == '+' and left_type == 'String' and right_type == 'String':
                    return 'String'
                else:
                    self.add_error(ErrorType.TYPE_ERROR, 
                                 f"Cannot apply operator '{expr.operator}' to types '{left_type}' and '{right_type}'", expr)
                    return None
            
            elif expr.operator in ['==', '!=', '<', '<=', '>', '>=']:
                if left_type == right_type:
                    return 'bool'
                else:
                    self.add_error(ErrorType.TYPE_ERROR, 
                                 f"Cannot compare types '{left_type}' and '{right_type}'", expr)
                    return 'bool'  # Return bool even on error
            
            elif expr.operator in ['&&', '||']:
                if left_type == 'bool' and right_type == 'bool':
                    return 'bool'
                else:
                    self.add_error(ErrorType.TYPE_ERROR, 
                                 f"Logical operator '{expr.operator}' requires boolean operands", expr)
                    return 'bool'
        
        elif isinstance(expr, UnaryOp):
            operand_type = self.get_expression_type(expr.operand)
            
            if operand_type is None:
                return None
            
            if expr.operator == '!':
                if operand_type == 'bool':
                    return 'bool'
                else:
                    self.add_error(ErrorType.TYPE_ERROR, 
                                 f"Cannot apply '!' to type '{operand_type}'", expr)
                    return 'bool'
            
            elif expr.operator == '-':
                if operand_type in ['i32', 'i64', 'f32', 'f64']:
                    return operand_type
                else:
                    self.add_error(ErrorType.TYPE_ERROR, 
                                 f"Cannot apply unary '-' to type '{operand_type}'", expr)
                    return operand_type
        
        elif isinstance(expr, FunctionCall):
            func_type = self.get_expression_type(expr.function)
            
            if isinstance(expr.function, Identifier):
                symbol = self.current_scope.lookup(expr.function.name)
                if isinstance(symbol, FunctionSymbol):
                    # Check argument count
                    if len(expr.arguments) != len(symbol.parameters):
                        self.add_error(ErrorType.TYPE_ERROR, 
                                     f"Function '{expr.function.name}' expects {len(symbol.parameters)} arguments, got {len(expr.arguments)}", expr)
                    
                    # Check argument types
                    for i, (arg, param) in enumerate(zip(expr.arguments, symbol.parameters)):
                        arg_type = self.get_expression_type(arg)
                        if arg_type != param.type_annotation:
                            self.add_error(ErrorType.TYPE_ERROR, 
                                         f"Argument {i+1} of function '{expr.function.name}' expects type '{param.type_annotation}', got '{arg_type}'", arg)
                    
                    return symbol.return_type
                else:
                    self.add_error(ErrorType.UNDEFINED_FUNCTION, f"Undefined function: {expr.function.name}", expr)
        
        elif isinstance(expr, MemberAccess):
            object_type = self.get_expression_type(expr.object)
            
            if object_type:
                # Check if the object type has the requested member
                struct_symbol = self.global_scope.lookup(object_type)
                if isinstance(struct_symbol, StructSymbol):
                    for field in struct_symbol.fields:
                        if field.name == expr.member:
                            return field.type_annotation
                    
                    self.add_error(ErrorType.SEMANTIC_ERROR, 
                                 f"Type '{object_type}' has no member '{expr.member}'", expr)
                else:
                    self.add_error(ErrorType.TYPE_ERROR, 
                                 f"Cannot access member '{expr.member}' on non-struct type '{object_type}'", expr)
        
        return None
    
    def check_program(self, program: Program) -> List[SemanticError]:
        """Main entry point for error checking."""
        self.errors = []
        
        for statement in program.statements:
            self.check_statement(statement)
        
        # Check for unused variables (warning-level errors)
        self._check_unused_symbols()
        
        return self.errors
    
    def check_statement(self, stmt: Statement):
        if isinstance(stmt, LetStatement):
            self.check_let_statement(stmt)
        elif isinstance(stmt, FunctionDefinition):
            self.check_function_definition(stmt)
        elif isinstance(stmt, ReturnStatement):
            self.check_return_statement(stmt)
        elif isinstance(stmt, IfStatement):
            self.check_if_statement(stmt)
        elif isinstance(stmt, WhileStatement):
            self.check_while_statement(stmt)
        elif isinstance(stmt, ForStatement):
            self.check_for_statement(stmt)
        elif isinstance(stmt, ExpressionStatement):
            self.check_expression_statement(stmt)
        elif isinstance(stmt, Block):
            self.check_block(stmt)
        elif isinstance(stmt, StructDefinition):
            self.check_struct_definition(stmt)
        elif isinstance(stmt, ImportStatement):
            self.check_import_statement(stmt)
        elif isinstance(stmt, PackageDeclaration):
            self.check_package_declaration(stmt)
    
    def check_let_statement(self, stmt: LetStatement):
        # Check type annotation if present
        if stmt.type_annotation and not self.is_valid_type(stmt.type_annotation):
            self.add_error(ErrorType.UNDEFINED_TYPE, f"Undefined type: {stmt.type_annotation}", stmt)
        
        # Check if variable is already defined in current scope
        if stmt.name in self.current_scope.symbols:
            self.add_error(ErrorType.REDEFINITION, f"Variable '{stmt.name}' is already defined", stmt)
        
        # Check initializer expression if present
        expr_type = None
        if stmt.value:
            expr_type = self.get_expression_type(stmt.value)
        
        # Type compatibility check
        if stmt.type_annotation and expr_type:
            if stmt.type_annotation != expr_type:
                self.add_error(ErrorType.TYPE_ERROR, 
                             f"Cannot assign value of type '{expr_type}' to variable of type '{stmt.type_annotation}'", stmt)
        
        # Determine final type
        final_type = stmt.type_annotation or expr_type
        if final_type:
            symbol = Symbol(stmt.name, final_type)
            self.current_scope.define(stmt.name, symbol)
        else:
            self.add_error(ErrorType.TYPE_ERROR, "Cannot determine type of variable", stmt)
    
    def check_function_definition(self, stmt: FunctionDefinition):
        # Check if function is already defined
        if stmt.name in self.global_scope.symbols:
            self.add_error(ErrorType.REDEFINITION, f"Function '{stmt.name}' is already defined", stmt)
        
        # Check parameter types
        for param in stmt.parameters:
            if not self.is_valid_type(param.type_annotation):
                self.add_error(ErrorType.UNDEFINED_TYPE, f"Undefined type: {param.type_annotation}", stmt)
        
        # Check return type
        if stmt.return_type and not self.is_valid_type(stmt.return_type):
            self.add_error(ErrorType.UNDEFINED_TYPE, f"Undefined return type: {stmt.return_type}", stmt)
        
        # Add function to global scope
        func_symbol = FunctionSymbol(stmt.name, stmt.return_type or "void", stmt.parameters, stmt.return_type)
        self.global_scope.define(stmt.name, func_symbol)
        
        # Check function body in new scope
        self.enter_scope()
        self.current_function_return_type = stmt.return_type
        
        # Add parameters to function scope
        for param in stmt.parameters:
            param_symbol = Symbol(param.name, param.type_annotation)
            self.current_scope.define(param.name, param_symbol)
        
        # Check body statements
        for body_stmt in stmt.body:
            self.check_statement(body_stmt)
        
        self.current_function_return_type = None
        self.exit_scope()
    
    def check_return_statement(self, stmt: ReturnStatement):
        if self.current_function_return_type is None:
            self.add_error(ErrorType.SEMANTIC_ERROR, "Return statement outside function", stmt)
            return
        
        if stmt.value:
            return_type = self.get_expression_type(stmt.value)
            if return_type != self.current_function_return_type:
                self.add_error(ErrorType.TYPE_ERROR, 
                             f"Cannot return value of type '{return_type}' from function expecting '{self.current_function_return_type}'", stmt)
        elif self.current_function_return_type != "void":
            self.add_error(ErrorType.TYPE_ERROR, 
                         f"Function expecting return type '{self.current_function_return_type}' must return a value", stmt)
    
    def check_if_statement(self, stmt: IfStatement):
        condition_type = self.get_expression_type(stmt.condition)
        if condition_type != "bool":
            self.add_error(ErrorType.TYPE_ERROR, f"If condition must be boolean, got '{condition_type}'", stmt)
        
        # Check then body
        self.enter_scope()
        for then_stmt in stmt.then_body:
            self.check_statement(then_stmt)
        self.exit_scope()
        
        # Check else body if present
        if stmt.else_body:
            self.enter_scope()
            for else_stmt in stmt.else_body:
                self.check_statement(else_stmt)
            self.exit_scope()
    
    def check_while_statement(self, stmt: WhileStatement):
        condition_type = self.get_expression_type(stmt.condition)
        if condition_type != "bool":
            self.add_error(ErrorType.TYPE_ERROR, f"While condition must be boolean, got '{condition_type}'", stmt)
        
        # Check body
        self.enter_scope()
        for body_stmt in stmt.body:
            self.check_statement(body_stmt)
        self.exit_scope()
    
    def check_for_statement(self, stmt: ForStatement):
        # Check iterable (simplified - would need more complex logic for real implementation)
        iterable_type = self.get_expression_type(stmt.iterable)
        
        # Check body in new scope with loop variable
        self.enter_scope()
        
        # Add loop variable to scope (simplified type inference)
        loop_var_type = "i32"  # Simplified assumption
        loop_var_symbol = Symbol(stmt.variable, loop_var_type)
        self.current_scope.define(stmt.variable, loop_var_symbol)
        
        for body_stmt in stmt.body:
            self.check_statement(body_stmt)
        
        self.exit_scope()
    
    def check_expression_statement(self, stmt: ExpressionStatement):
        self.get_expression_type(stmt.expression)
    
    def check_block(self, stmt: Block):
        self.enter_scope()
        for block_stmt in stmt.statements:
            self.check_statement(block_stmt)
        self.exit_scope()
    
    def check_struct_definition(self, stmt: StructDefinition):
        # Check if struct is already defined
        if stmt.name in self.global_scope.symbols:
            self.add_error(ErrorType.REDEFINITION, f"Struct '{stmt.name}' is already defined", stmt)
        
        # Check field types
        field_names = set()
        for field in stmt.fields:
            if field.name in field_names:
                self.add_error(ErrorType.REDEFINITION, f"Field '{field.name}' is defined multiple times", stmt)
            field_names.add(field.name)
            
            if not self.is_valid_type(field.type_annotation):
                self.add_error(ErrorType.UNDEFINED_TYPE, f"Undefined field type: {field.type_annotation}", stmt)
        
        # Add struct to global scope
        struct_symbol = StructSymbol(stmt.name, stmt.name, stmt.fields)
        self.global_scope.define(stmt.name, struct_symbol)
    
    def check_import_statement(self, stmt: ImportStatement):
        # Basic validation of import statement
        # In a real implementation, this would check if the module exists
        pass
    
    def check_package_declaration(self, stmt: PackageDeclaration):
        # Basic validation of package declaration
        # In a real implementation, this would validate version format and dependencies
        pass
    
    def _check_unused_symbols(self):
        """Check for unused variables and functions."""
        def check_scope(scope: Scope):
            for name, symbol in scope.symbols.items():
                if not symbol.used and not isinstance(symbol, (FunctionSymbol, StructSymbol)):
                    # Only warn about unused variables, not functions/structs
                    self.add_error(ErrorType.SEMANTIC_ERROR, f"Unused variable: {name}")
        
        check_scope(self.global_scope)

def check_errors(program: Program) -> List[SemanticError]:
    """Convenience function to check a program for errors."""
    checker = ErrorChecker()
    return checker.check_program(program)

if __name__ == "__main__":
    from lexer import lex_source
    from parser import parse_source
    
    # Test with some sample code
    test_code = '''
    let name = "NeoPaquet"
    let age: i32 = 25
    let invalid_age: String = 30  // Type error
    
    fn greet(person: String) -> String {
        return "Hello, " + person + "!"
    }
    
    fn bad_function(x: UnknownType) -> String {  // Undefined type error
        return x
    }
    
    struct User {
        name: String,
        age: i32,
        name: String  // Duplicate field error
    }
    
    let result = greet(42)  // Type error
    let unused_var = "test"  // Unused variable warning
    '''
    
    try:
        program = parse_source(test_code)
        errors = check_errors(program)
        
        if errors:
            print(f"Found {len(errors)} errors:")
            for error in errors:
                print(f"  {error.type.name}: {error.message}")
        else:
            print("No errors found!")
    except Exception as e:
        print(f"Error during analysis: {e}")