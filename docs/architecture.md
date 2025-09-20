# 📂 `docs/architecture.md`

```markdown
# 🏗️ NeoPaquet Compiler Architecture

This document explains the **toolchain architecture** of NeoPaquet — how source code flows from `.np` files into **LLVM IR**, **NASM assembly**, and finally **native executables**.

---

## 1. High-Level Pipeline

**Source Code (`.np`)**  
⬇️ Lexer  
⬇️ Parser  
⬇️ AST (Dodecagram Base-12)  
⬇️ IR Generator → LLVM IR  
⬇️ NASM Generator  
⬇️ Linker  
⬇️ **Executable (`.exe` / `.out`)**

---

## 2. ASCII Architecture Diagram

```

+--------------------+
\|   Source Code      |   hello.np
+--------------------+
|
v
+--------------------+
\| Lexer (tokens)     |   SRC, PRINT, STRING("Hello")
+--------------------+
|
v
+--------------------+
\| Parser (AST)       |   Base-12 Dodecagram Nodes
+--------------------+
|
v
+--------------------+
\| AST Visitor (IRGen)|   IR lowering
+--------------------+
|
v
+--------------------+
\| LLVM IR Module     |   printf call, SSA registers
+--------------------+
|
v
+--------------------+
\| NASM Backend       |   x86-64 Assembly
+--------------------+
|
v
+--------------------+
\| Linker (Clang/LLD) |   platform binary
+--------------------+
|
v
+--------------------+
\| Executable Output  |   hello.exe / a.out
+--------------------+

````

---

## 3. Mermaid Flowchart

```mermaid
flowchart TD
    A[.np Source Code] --> B[Lexer]
    B --> C[Parser]
    C --> D[AST (Base-12)]
    D --> E[IRGen → LLVM IR]
    E --> F[NASM Generator]
    F --> G[Linker (Clang/LLD)]
    G --> H[Executable (.exe / .out)]
````

---

## 4. Modules

| Module       | Responsibility                             |
| ------------ | ------------------------------------------ |
| `lexer.py`   | Converts raw text → tokens                 |
| `parser.py`  | Consumes tokens → builds AST               |
| `ast.py`     | Defines AST node types (base-12)           |
| `irgen.py`   | Walks AST → emits LLVM IR                  |
| `nasmgen.py` | Converts LLVM IR → NASM + links executable |
| `main.py`    | CLI driver (`npaquetc`)                    |

---

## 5. Example Flow

### Input

```neopaquet
src () "stdout" {
  print ["Hello NeoPaquet!"]
} run
```

### Tokens

```
SRC, LPAREN, RPAREN, STRING("stdout"),
LBRACE, PRINT, STRING("Hello NeoPaquet!"),
RBRACE, RUN
```

### AST (simplified)

```
Program
 └── SrcDecl("stdout")
     └── Block
         └── PrintStmt("Hello NeoPaquet!")
```

### LLVM IR (generated)

```llvm
@.str0 = private constant [17 x i8] c"Hello NeoPaquet!\00"

define i32 @main() {
entry:
  %0 = getelementptr [17 x i8], [17 x i8]* @.str0, i32 0, i32 0
  call i32 (i8*, ...) @printf(i8* %0)
  ret i32 0
}
```

### NASM (lowered)

```asm
section .data
hello db "Hello NeoPaquet!",0

section .text
global main
main:
    mov rdi, hello
    call printf
    mov eax, 0
    ret
```

### Executable

```
$ ./hello.exe
Hello NeoPaquet!
```

---

## 6. Extended Features

* **CIAM Memory Model** → Macros for safe arenas, slices.
* **Execution-Aware Error Handling** → `try`, `catch`, `clean`, `retry`, `dismiss`.
* **Optimizations baked in** → constant folding, loop unrolling, vectorization.
* **Cross-platform builds** → Ubuntu, Windows, macOS, Kali.

---

## 7. Related Docs

* [Specification](spec.md) → Grammar + semantics
* [Tutorial](tutorial.md) → Beginner’s guide
* [Cheatsheet](cheatsheet.md) → Quick reference
* [Examples](examples/) → Ready-to-run programs
* [Roadmap](../ROADMAP.md) → Future development

```

---

## ✅ What This Adds
- **Visual pipeline diagrams** (ASCII + Mermaid).  
- **Clear mapping** from `.np` → tokens → AST → LLVM → NASM → exe.  
- **Example transformation** at every stage.  
- Cross-links to other docs.  

---

⚡
```
