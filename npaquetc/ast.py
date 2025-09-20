# npaquetc/ast.py
# NeoPaquet Abstract Syntax Tree
# Base-12 dodecagram encoding of AST nodes
# Author: NeoPaquet Project

from typing import List, Any, Optional

# -----------------------------
# Node Kind Map (Base-12)
# -----------------------------
NODE_MAP = {
    "Program": "0_PROGRAM",
    "Decl": "1_DECL",
    "Stmt": "2_STMT",
    "Expr": "3_EXPR",
    "Ident": "4_IDENT",
    "Literal": "5_LITERAL",
    "Func": "6_FUNC",
    "Block": "7_BLOCK",
    "Try": "8_TRY",
    "Catch": "9_CATCH",
    "Loop": "a_LOOP",
    "If": "b_IF"
}

# -----------------------------
# Base AST Node
# -----------------------------
class ASTNode:
    def __init__(self, kind: str, value: Optional[Any] = None, children: Optional[List['ASTNode']] = None):
        if kind not in NODE_MAP.values():
            raise ValueError(f"Unknown AST kind: {kind}")
        self.kind = kind
        self.value = value
        self.children = children or []

    def add_child(self, node: 'ASTNode'):
        self.children.append(node)

    def __repr__(self, level=0):
        indent = "  " * level
        rep = f"{indent}{self.kind}"
        if self.value is not None:
            rep += f" ({self.value})"
        for child in self.children:
            rep += "\n" + child.__repr__(level + 1)
        return rep

    def accept(self, visitor: 'ASTVisitor'):
        """Visitor dispatch based on kind"""
        method_name = "visit_" + self.kind.split("_", 1)[1].lower()
        visit = getattr(visitor, method_name, visitor.generic_visit)
        return visit(self)


# -----------------------------
# Visitor Base
# -----------------------------
class ASTVisitor:
    def generic_visit(self, node: ASTNode):
        for child in node.children:
            child.accept(self)


# -----------------------------
# Node Factory Helpers
# -----------------------------
def Program(children: List[ASTNode]) -> ASTNode:
    return ASTNode(NODE_MAP["Program"], children=children)

def Decl(value: str, children: List[ASTNode] = None) -> ASTNode:
    return ASTNode(NODE_MAP["Decl"], value=value, children=children)

def Stmt(value: str, children: List[ASTNode] = None) -> ASTNode:
    return ASTNode(NODE_MAP["Stmt"], value=value, children=children)

def Expr(value: Any) -> ASTNode:
    return ASTNode(NODE_MAP["Expr"], value=value)

def Ident(name: str) -> ASTNode:
    return ASTNode(NODE_MAP["Ident"], value=name)

def Literal(val: Any) -> ASTNode:
    return ASTNode(NODE_MAP["Literal"], value=val)

def Func(name: str, children: List[ASTNode] = None) -> ASTNode:
    return ASTNode(NODE_MAP["Func"], value=name, children=children)

def Block(children: List[ASTNode]) -> ASTNode:
    return ASTNode(NODE_MAP["Block"], children=children)

def Try(children: List[ASTNode]) -> ASTNode:
    return ASTNode(NODE_MAP["Try"], children=children)

def Catch(children: List[ASTNode]) -> ASTNode:
    return ASTNode(NODE_MAP["Catch"], children=children)

def Loop(value: str, children: List[ASTNode]) -> ASTNode:
    return ASTNode(NODE_MAP["Loop"], value=value, children=children)

def If(children: List[ASTNode]) -> ASTNode:
    return ASTNode(NODE_MAP["If"], children=children)


# -----------------------------
# Debug Harness
# -----------------------------
if __name__ == "__main__":
    # Construct an AST manually to test
    ast = Program([
        Decl("src", [
            Literal("stdout"),
            Block([
                Stmt("print", [Literal("Hello NeoPaquet")])
            ])
        ]),
        Func("add", [
            Ident("x"),
            Block([
                Stmt("return", [Ident("x")])
            ])
        ])
    ])

    print(ast)
