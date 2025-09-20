# 🔧 NeoPaquet Developer Internals
*A deep dive into compiler internals for contributors*

This document is intended for **compiler contributors** working on the NeoPaquet toolchain.  
It explains design choices, symbol tables, memory handling, CIAM macro expansion, and how modules interact.

---

## 1. Core Design Choices

- **Execution-Oriented**: Language constructs map directly to runtime instructions. No “sugar” without execution semantics.  
- **Dodecagram AST**: Every AST node has a **base-12 numeric ID** (`0–9, a, b`). Compact, unambiguous, machine-friendly.  
- **Visitor Pattern**: IR generation and NASM lowering are implemented as **visitors** over AST nodes.  
- **Always-On Optimizations**: Optimizations (constant folding, peephole, loop unrolling) are **intrinsic** and cannot be disabled.  
- **Interop by Default**: Functions are **C ABI–exposed** automatically.  

---

## 2. Compiler Modules

| Module        | Purpose |
|---------------|---------|
| `lexer.py`    | Converts raw source → tokens |
| `parser.py`   | Converts tokens → AST |
| `ast.py`      | Node definitions + visitor interface |
| `irgen.py`    | Lowers AST → LLVM IR (llvmlite) |
| `nasmgen.py`  | Converts LLVM IR → NASM assembly / object / executable |
| `main.py`     | CLI driver (`npaquetc`) |

---

## 3. Symbol Tables

### Variables
- Stored in `var_symtab` (Python dict).
- Keys: identifier names.
- Values: `llvmlite.ir.Value` or constants.
- Example:
```python
self.var_symtab["x"] = ir.Constant(ir.IntType(32), 5)
````

### Functions

* Stored in `func_symtab`.
* Keys: function names.
* Values: `llvmlite.ir.Function` objects.
* Example:

```python
self.func_symtab["square"] = ir.Function(...)
```

---

## 4. AST Node IDs (Base-12)

| Node Type | Dodecagram ID |
| --------- | ------------- |
| Program   | `0`           |
| SrcDecl   | `1`           |
| FuncDecl  | `2`           |
| TaskDecl  | `3`           |
| Block     | `4`           |
| Stmt      | `5`           |
| Expr      | `6`           |
| Literal   | `7`           |
| Ident     | `8`           |
| IfStmt    | `9`           |
| LoopStmt  | `a`           |
| TryStmt   | `b`           |

Every node is reduced to its **base-12 key** internally.

---

## 5. CIAM (Contextual Inference Abstraction Macros)

NeoPaquet’s unique **memory model** uses CIAM macros.

### Example

```neopaquet
mem.arena { size=1024 }
mem.slice { start=0, len=12 }
```

### Expansion

At IRGen stage:

```llvm
; Arena of 1024 bytes
%arena = alloca [1024 x i8]
```

At NASM stage:

```asm
section .bss
arena resb 1024
```

Guarantees:

* No implicit garbage collection.
* Anti use-after-free checks inserted at compile time.
* Memory macros can inline into **safe allocators** or **stack locals**.

---

## 6. Error Handling Lowering

NeoPaquet error model: `try / catch / retry / clean / dismiss`

### Example

```neopaquet
try {
  x = 10 / 0
} catch {
  print ["error"]
} clean {
  print ["cleanup"]
}
```

### LLVM IR Lowering

```llvm
invoke i32 @divide(i32 10, i32 0)
    to label %normal unwind label %lpad

lpad:
    %exn = landingpad { i8*, i32 }
    catch i8* null
    br label %catch

catch:
    call void @printf("error")
    br label %clean

clean:
    call void @printf("cleanup")
    ret i32 0
```

### NASM Lowering (simplified)

```asm
call divide
jc .catch       ; jump if error flag set
jmp .normal

.catch:
    mov rdi, error_msg
    call printf
    jmp .clean

.clean:
    mov rdi, cleanup_msg
    call printf
    ret
```

---

## 7. Optimizations (Compiler Intrinsics)

* **Constant Folding**: done during AST → IR.
* **Peephole Passes**: simplify redundant instructions.
* **Loop Unrolling**: expand small fixed loops at IRGen.
* **Tail-Call Optimization**: recognized in recursive calls.
* **Vectorization**: use SIMD intrinsics when LLVM target allows.

---

## 8. Execution Model

* **AOT only** → no interpreter.
* **Zero-cost runtime** → no VM overhead.
* **Native startup speed** → binaries start instantly.
* **Interop-first** → compiled symbols usable in C, Rust, etc.

---

## 9. Debugging Internals

* Use `--emit llvm` to dump IR.
* Use `--emit asm` to inspect NASM.
* Use `print(irgen.module)` inside `irgen.py` for IR debug.
* Use `pytest tests/` for regression coverage.

---

## 10. Developer Notes

* **Code Style:** Python (PEP 8) with debug harness in each file.
* **Contributions:** Require tests in `tests/` and doc updates in `docs/`.
* **CI/CD:** Multi-OS build pipeline (Ubuntu, Windows, macOS, Kali).
* **License:** All code/doc/spec under [S.U.E.T. License v1.0](../License.md).

---

```

---

## ✅ What This Adds
- Detailed **symbol table structure**.  
- **AST node IDs** in base-12 mapping.  
- **CIAM macro expansion examples** into LLVM + NASM.  
- **Error handling lowering** (IR + assembly).  
- Notes on **optimizations, execution model, debugging**.  
- Contributor-focused guidelines.  

---

⚡
