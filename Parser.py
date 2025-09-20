# npaquetc/parser.py
# NeoPaquet Parser
# Builds AST (dodecagram base-12) from tokens
# Author: NeoPaquet Project

from typing import List, Optional
from lexer import Lexer, Token

# -----------------------------
# AST Node (Base-12 encoded)
# -----------------------------
class ASTNode:
    def __init__(self, kind: str, value: Optional[str] = None, children: Optional[List['ASTNode']] = None):
        self.kind = kind  # e.g., "0_PROGRAM", "1_DECL", "a_LOOP"
        self.value = value
        self.children = children or []

    def __repr__(self, level=0):
        indent = "  " * level
        rep = f"{indent}{self.kind}"
        if self.value:
            rep += f" ({self.value})"
        for child in self.children:
            rep += "\n" + child.__repr__(level + 1)
        return rep


# -----------------------------
# Dodecagram Node Mapping
# -----------------------------
NODE_MAP = {
    "PROGRAM": "0_PROGRAM",
    "DECL": "1_DECL",
    "STMT": "2_STMT",
    "EXPR": "3_EXPR",
    "IDENT": "4_IDENT",
    "LITERAL": "5_LITERAL",
    "FUNC": "6_FUNC",
    "BLOCK": "7_BLOCK",
    "TRY": "8_TRY",
    "CATCH": "9_CATCH",
    "LOOP": "a_LOOP",
    "IF": "b_IF"
}


# -----------------------------
# Parser
# -----------------------------
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def _peek(self, k: int = 0) -> Token:
        if self.pos + k < len(self.tokens):
            return self.tokens[self.pos + k]
        return Token("EOF", "", -1, -1)

    def _advance(self) -> Token:
        tok = self._peek()
        self.pos += 1
        return tok

    def _expect(self, type_: str, value: Optional[str] = None) -> Token:
        tok = self._advance()
        if tok.type != type_ and (value is None or tok.value != value):
            raise SyntaxError(f"Expected {type_} {value}, got {tok.type} {tok.value}")
        return tok

    # -------------------------
    # Top-Level Parse
    # -------------------------
    def parse_program(self) -> ASTNode:
        children = []
        while self._peek().type != "EOF":
            children.append(self.parse_decl())
        return ASTNode(NODE_MAP["PROGRAM"], children=children)

    # -------------------------
    # Declarations
    # -------------------------
    def parse_decl(self) -> ASTNode:
        tok = self._peek()

        if tok.value == "src":
            return self.parse_src()
        elif tok.value == "Task":
            return self.parse_task()
        elif tok.value == "@func":
            return self.parse_func()
        elif tok.value == "Start":
            return self.parse_start()
        else:
            return self.parse_stmt()

    def parse_src(self) -> ASTNode:
        self._expect("KEYWORD", "src")
        self._expect("SYMBOL", "(")
        self._expect("SYMBOL", ")")
        fmt = self._expect("STRING").value
        self._expect("SYMBOL", "{")
        body = self.parse_block()
        self._expect("SYMBOL", "}")
        self._expect("KEYWORD", "run")
        return ASTNode(NODE_MAP["DECL"], value="src", children=[ASTNode("FORMAT", fmt), body])

    def parse_task(self) -> ASTNode:
        self._expect("KEYWORD", "Task")
        self._expect("SYMBOL", "<")
        ident = self._expect("IDENTIFIER").value
        self._expect("SYMBOL", ">")
        instr = self._expect("STRING").value
        self._expect("SYMBOL", "|")
        fmt = self._expect("STRING").value
        self._expect("OPERATOR", "->")
        self._expect("KEYWORD", "complete")
        return ASTNode(NODE_MAP["DECL"], value="task", children=[
            ASTNode(NODE_MAP["IDENT"], ident),
            ASTNode(NODE_MAP["LITERAL"], instr),
            ASTNode(NODE_MAP["LITERAL"], fmt)
        ])

    def parse_func(self) -> ASTNode:
        self._expect("KEYWORD", "@func")
        self._expect("SYMBOL", "(")
        name = self._expect("STRING").value
        self._expect("SYMBOL", ")")
        self._expect("SYMBOL", "[")
        arg = self._expect("IDENTIFIER").value
        self._expect("SYMBOL", "]")
        self._expect("KEYWORD", "go")
        body = self.parse_block()
        return ASTNode(NODE_MAP["FUNC"], value=name, children=[
            ASTNode(NODE_MAP["IDENT"], arg),
            body
        ])

    def parse_start(self) -> ASTNode:
        self._expect("KEYWORD", "Start")
        self._expect("SYMBOL", ":")
        self._expect("KEYWORD", "setup")
        self._expect("SYMBOL", "(")
        proc = self._expect("STRING").value
        self._expect("SYMBOL", ")")
        self._expect("KEYWORD", "done")
        self._expect("SYMBOL", "{")
        self._expect("SYMBOL", "}")
        return ASTNode(NODE_MAP["DECL"], value="start", children=[
            ASTNode(NODE_MAP["LITERAL"], proc)
        ])

    # -------------------------
    # Statements
    # -------------------------
    def parse_stmt(self) -> ASTNode:
        tok = self._peek()

        if tok.value == "print":
            return self.parse_print()
        elif tok.value == "if":
            return self.parse_if()
        elif tok.value == "loop":
            return self.parse_loop()
        elif tok.value == "try":
            return self.parse_trycatch()
        else:
            ident = self._expect("IDENTIFIER").value
            self._expect("OPERATOR", "=")
            expr = self.parse_expr()
            return ASTNode(NODE_MAP["STMT"], value="assign", children=[
                ASTNode(NODE_MAP["IDENT"], ident),
                expr
            ])

    def parse_print(self) -> ASTNode:
        self._expect("KEYWORD", "print")
        self._expect("SYMBOL", "[")
        text = self._expect("STRING").value
        self._expect("SYMBOL", "]")
        return ASTNode(NODE_MAP["STMT"], value="print", children=[
            ASTNode(NODE_MAP["LITERAL"], text)
        ])

    def parse_if(self) -> ASTNode:
        self._expect("KEYWORD", "if")
        cond = self.parse_expr()
        self._expect("SYMBOL", "{")
        then_block = self.parse_block()
        self._expect("SYMBOL", "}")
        else_block = None
        if self._peek().value == "else":
            self._expect("KEYWORD", "else")
            self._expect("SYMBOL", "{")
            else_block = self.parse_block()
            self._expect("SYMBOL", "}")
        children = [cond, then_block]
        if else_block:
            children.append(else_block)
        return ASTNode(NODE_MAP["IF"], children=children)

    def parse_loop(self) -> ASTNode:
        self._expect("KEYWORD", "loop")
        rng = self._expect("STRING").value
        self._expect("SYMBOL", "{")
        body = self.parse_block()
        self._expect("SYMBOL", "}")
        return ASTNode(NODE_MAP["LOOP"], value=rng, children=[body])

    def parse_trycatch(self) -> ASTNode:
        self._expect("KEYWORD", "try")
        self._expect("SYMBOL", "{")
        try_block = self.parse_block()
        self._expect("SYMBOL", "}")
        self._expect("KEYWORD", "catch")
        self._expect("SYMBOL", "{")
        catch_block = self.parse_block()
        self._expect("SYMBOL", "}")
        return ASTNode(NODE_MAP["TRY"], children=[try_block, ASTNode(NODE_MAP["CATCH"], children=[catch_block])])

    def parse_expr(self) -> ASTNode:
        tok = self._advance()
        if tok.type == "NUMBER":
            return ASTNode(NODE_MAP["LITERAL"], tok.value)
        elif tok.type == "STRING":
            return ASTNode(NODE_MAP["LITERAL"], tok.value)
        elif tok.type == "IDENTIFIER":
            return ASTNode(NODE_MAP["IDENT"], tok.value)
        else:
            raise SyntaxError(f"Unexpected expression token {tok}")

    def parse_block(self) -> ASTNode:
        stmts = []
        while self._peek().value not in ("}", "done", "complete", "catch", "EOF"):
            stmts.append(self.parse_stmt())
        return ASTNode(NODE_MAP["BLOCK"], children=stmts)


# -----------------------------
# Debug
# -----------------------------
if __name__ == "__main__":
    from lexer import Lexer

    code = '''
    src () "stdout" { print ["Hello NeoPaquet"] } run
    @func ("add") [x] go { print ["Done"] }
    '''
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_program()
    print(ast)
