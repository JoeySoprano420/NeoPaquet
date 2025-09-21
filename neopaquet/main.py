# npaquetc/main.py
# NeoPaquet Compiler CLI
# Entry point for npaquetc
# Author: NeoPaquet Project

import argparse
import os
import sys

from lexer import Lexer
from parser import Parser
from irgen import IRGen
from nasmgen import NASMGen


def compile_file(input_file: str, output_file: str, emit: str):
    # Step 1: Read source
    try:
        with open(input_file, "r") as f:
            source = f.read()
    except FileNotFoundError:
        sys.stderr.write(f"error: file not found: {input_file}\n")
        sys.exit(1)

    # Step 2: Lexing
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    # Step 3: Parsing
    parser = Parser(tokens)
    ast = parser.parse_program()

    # Step 4: IR Generation
    irgen = IRGen()
    ast.accept(irgen)
    llvm_ir = str(irgen.module)

    if emit == "llvm":
        out = output_file if output_file.endswith(".ll") else output_file + ".ll"
        with open(out, "w") as f:
            f.write(llvm_ir)
        print(f"LLVM IR written to {out}")
        return

    # Step 5: NASM Backend
    nasm = NASMGen(llvm_ir)

    if emit == "asm":
        out = output_file if output_file.endswith(".asm") else output_file + ".asm"
        nasm.emit_asm(out)
        print(f"NASM assembly written to {out}")
        return

    # Step 6: Executable
    exe = nasm.emit_exe(output_file)
    print(f"Executable generated: {exe}")


def main():
    parser = argparse.ArgumentParser(
        prog="npaquetc",
        description="NeoPaquet Compiler (AOT → LLVM IR → NASM → Native)"
    )
    parser.add_argument("input", help="Input .np source file")
    parser.add_argument("-o", "--output", default="a.out", help="Output file (default: a.out)")
    parser.add_argument("--emit", choices=["exe", "llvm", "asm"], default="exe",
                        help="Emit format: native exe (default), llvm IR, or nasm asm")

    args = parser.parse_args()

    compile_file(args.input, args.output, args.emit)


if __name__ == "__main__":
    main()
