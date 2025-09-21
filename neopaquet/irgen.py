# npaquetc/irgen.py
# NeoPaquet IR Generator
# Translates AST (base-12) into LLVM IR
# Author: NeoPaquet Project

from llvmlite import ir
from ast import ASTNode, ASTVisitor, NODE_MAP

# -----------------------------
# IR Generator Visitor
# -----------------------------
class IRGen(ASTVisitor):
    def __init__(self, module_name="neopaquet"):
        self.module = ir.Module(name=module_name)
        self.builder = None
        self.func_symtab = {}  # symbol table for functions
        self.var_symtab = {}   # symbol table for variables

        # Declare external printf
        voidptr_ty = ir.IntType(8).as_pointer()
        self.printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
        self.printf = ir.Function(self.module, self.printf_ty, name="printf")

    # -------------------------
    # Visitor Overrides
    # -------------------------
    def visit_program(self, node: ASTNode):
        for child in node.children:
            child.accept(self)

    def visit_decl(self, node: ASTNode):
        if node.value == "src":  # src () "stdout" { ... } run
            self._gen_main(node)

    def visit_func(self, node: ASTNode):
        func_name = node.value
        func_ty = ir.FunctionType(ir.IntType(32), [ir.IntType(32)])
        func = ir.Function(self.module, func_ty, name=func_name)
        self.func_symtab[func_name] = func

        block = func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        # Map argument
        arg = func.args[0]
        arg.name = node.children[0].value
        self.var_symtab[arg.name] = arg

        # Visit body
        node.children[1].accept(self)

        if not self.builder.block.is_terminated:
            self.builder.ret(ir.Constant(ir.IntType(32), 0))

    def visit_block(self, node: ASTNode):
        for stmt in node.children:
            stmt.accept(self)

    def visit_stmt(self, node: ASTNode):
        if node.value == "print":
            string_val = node.children[0].value
            self._emit_print(string_val)
        elif node.value == "assign":
            name = node.children[0].value
            expr = node.children[1].value
            val = ir.Constant(ir.IntType(32), int(expr, 12))  # base-12 constant
            self.var_symtab[name] = val
        elif node.value == "return":
            ret_val = node.children[0]
            if ret_val.kind == NODE_MAP["Ident"]:
                val = self.var_symtab.get(ret_val.value)
                self.builder.ret(val)
            else:
                self.builder.ret(ir.Constant(ir.IntType(32), int(ret_val.value, 12)))

    def visit_expr(self, node: ASTNode):
        if node.kind == NODE_MAP["Literal"]:
            return ir.Constant(ir.IntType(32), int(node.value, 12))
        elif node.kind == NODE_MAP["Ident"]:
            return self.var_symtab.get(node.value)
        else:
            raise NotImplementedError(f"Unsupported expression {node}")

    # -------------------------
    # Helpers
    # -------------------------
    def _emit_print(self, text: str):
        # Define global string
        string_ty = ir.ArrayType(ir.IntType(8), len(text) + 1)
        cstr = ir.GlobalVariable(self.module, string_ty, name=f".str{len(self.module.globals)}")
        cstr.linkage = "internal"
        cstr.global_constant = True
        cstr.initializer = ir.Constant(string_ty, bytearray(text.encode("utf8") + b"\0"))

        # GEP pointer
        zero = ir.Constant(ir.IntType(32), 0)
        gep = self.builder.gep(cstr, [zero, zero])

        self.builder.call(self.printf, [gep])

    def _gen_main(self, node: ASTNode):
        # Create main()
        func_ty = ir.FunctionType(ir.IntType(32), [])
        main_fn = ir.Function(self.module, func_ty, name="main")
        block = main_fn.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        # Visit src block
        node.children[1].accept(self)

        if not self.builder.block.is_terminated:
            self.builder.ret(ir.Constant(ir.IntType(32), 0))


# -----------------------------
# Debug Harness
# -----------------------------
if __name__ == "__main__":
    from lexer import Lexer
    from parser import Parser

    code = '''
    src () "stdout" { print ["Hello NeoPaquet"] } run
    @func ("factorial") [n] go {
        if n <= 1 {
            return 1
        } else {
            return n * factorial(n - 1)
        }
    }
    '''
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_program()

    irgen = IRGen()
    ast.accept(irgen)
    print(irgen.module)
