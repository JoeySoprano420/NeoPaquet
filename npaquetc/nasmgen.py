# npaquetc/nasmgen.py
# NeoPaquet NASM Generator
# Lowers LLVM IR to NASM assembly + executable
# Author: NeoPaquet Project

import subprocess
import tempfile
import os
from llvmlite import binding as llvm

# -----------------------------
# Initialize LLVM
# -----------------------------
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

class NASMGen:
    def __init__(self, llvm_ir: str):
        self.llvm_ir = llvm_ir
        self.target = llvm.Target.from_default_triple()
        self.target_machine = self.target.create_target_machine()

    def emit_obj(self, obj_path: str):
        """Generate an object file (.o / .obj) from LLVM IR"""
        mod = llvm.parse_assembly(self.llvm_ir)
        mod.verify()
        with open(obj_path, "wb") as f:
            obj_data = self.target_machine.emit_object(mod)
            f.write(obj_data)

    def emit_asm(self, asm_path: str):
        """Generate NASM-style assembly from LLVM IR"""
        mod = llvm.parse_assembly(self.llvm_ir)
        mod.verify()
        with open(asm_path, "w") as f:
            asm_data = self.target_machine.emit_assembly(mod)
            f.write(asm_data)

    def emit_exe(self, exe_path: str):
        """Full pipeline: LLVM IR → .o → .exe/.out"""
        with tempfile.TemporaryDirectory() as tmpdir:
            obj_file = os.path.join(tmpdir, "out.o")
            self.emit_obj(obj_file)

            # Link depending on platform
            if os.name == "nt":  # Windows
                # Uses MSVC link or lld-link
                exe_file = exe_path if exe_path.endswith(".exe") else exe_path + ".exe"
                subprocess.run(["clang", obj_file, "-o", exe_file], check=True)
            else:
                # Linux / macOS
                exe_file = exe_path
                subprocess.run(["clang", obj_file, "-o", exe_file], check=True)

            return exe_file


# -----------------------------
# Debug Harness
# -----------------------------
if __name__ == "__main__":
    from lexer import Lexer
    from parser import Parser
    from irgen import IRGen

    code = '''
    src () "stdout" { print ["Hello NeoPaquet"] } run
    '''

    # Step 1: Lex + Parse
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse_program()

    # Step 2: IR Generation
    irgen = IRGen()
    ast.accept(irgen)
    llvm_ir = str(irgen.module)

    print("=== LLVM IR ===")
    print(llvm_ir)

    # Step 3: NASM Generation
    nasm = NASMGen(llvm_ir)
    nasm.emit_asm("out.asm")
    exe_path = nasm.emit_exe("hello")

    print(f"Generated: out.asm + {exe_path}")
