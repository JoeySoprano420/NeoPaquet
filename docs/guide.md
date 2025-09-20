# 📂 `docs/guide.md`

````markdown
# 📘 NeoPaquet Developer Guide
*A Deep Dive into the Compiler Architecture*  

NeoPaquet is an **execution-oriented language** that compiles from **source → LLVM IR → NASM → native executable**.  
This guide explains how the internals work: the lexer, parser, AST, IR generation, NASM backend, and the CIAM-based memory model.

---

## 1. Language Philosophy
- **Execution-Oriented** → Every construct exists to *execute efficiently*, not to look elegant.  
- **Dodecagram AST (base-12)** → Compact numeric encoding (`0–9, a=10, b=11`).  
- **Machine-Friendly** → Code flows directly into LLVM/NASM primitives.  
- **CIAM Memory Macros** → User defines memory semantics at compile time.  
- **Always Optimized** → Loop unrolling, constant folding, vectorization baked in.  

---

## 2. Compiler Pipeline

### Step 1 — Lexer
- Converts raw `.np` source into **tokens**.
- Handles:
  - **Identifiers**: `src`, `@func`, `Task`
  - **Numbers**: base-12 (e.g., `5a`, `1b`)
  - **Strings**: `"Hello"`
  - **Operators**: `+ - * / % == != < >`
  - **Comments**:
    - Single-line: `-- text`
    - Multi-line: `; text ;`

**Example:**  
```neopaquet
src () "stdout" { print ["Hello"] } run
````

➡️ Tokens: `SRC, LPAREN, RPAREN, STRING("stdout"), LBRACE, PRINT, ...`

---

### Step 2 — Parser

* Reads tokens and builds an **AST (Abstract Syntax Tree)**.
* AST nodes are tagged with **dodecagram base-12 IDs** for compact encoding.

**Example AST:**

```text
Program
 └── SrcDecl
     ├── Target: "stdout"
     └── Block
         └── PrintStmt("Hello")
```

---

### Step 3 — AST Representation

* Implemented in **`ast.py`**.
* Nodes:

  * `Program`
  * `SrcDecl`
  * `FuncDecl`
  * `TaskDecl`
  * `Block`
  * `Stmt`
  * `Expr`

Each node implements `.accept(visitor)` for **visitor pattern traversal**.

---

### Step 4 — IR Generation

* Implemented in **`irgen.py`** using **llvmlite**.
* Translates AST → LLVM IR.
* Example lowering:

```neopaquet
print ["Hello"]
```

➡️

```llvm
@.str0 = private constant [6 x i8] c"Hello\00"
call i32 (i8*, ...) @printf(i8* getelementptr ...)
```

* Functions map to C ABI:

```neopaquet
@func ("square") [n] go { return n * n }
```

➡️

```llvm
define i32 @square(i32 %n) {
entry:
  %mul = mul i32 %n, %n
  ret i32 %mul
}
```

---

### Step 5 — NASM Backend

* Implemented in **`nasmgen.py`**.
* Uses LLVM target machine to emit:

  * **Object files** (`.o / .obj`)
  * **NASM assembly** (`.asm`)
  * **Native executables** (`.exe` / `.out`)

Linking via:

* Windows: `clang` → `.exe`
* Linux/macOS: `clang` → ELF/Mach-O

---

### Step 6 — CLI Driver

* **`main.py`** provides CLI `npaquetc`.
* Options:

  * `--emit exe` (default): Native binary
  * `--emit llvm`: LLVM IR file
  * `--emit asm`: NASM assembly file

**Example:**

```bash
npaquetc hello.np -o hello.exe
./hello.exe
```

---

## 3. Memory Model (CIAM)

NeoPaquet introduces **Contextual Inference Abstraction Macros** for memory.

Examples:

```neopaquet
mem.arena { size=1024 }
mem.slice { start=0, len=12 }
```

Guarantees:

* No GC overhead.
* Anti use-after-free baked in.
* Memory macros inline directly into LLVM + NASM.

---

## 4. Error Handling

Execution-aware error handling:

```neopaquet
try {
  x = 10 / 0
} catch {
  print ["Error caught!"]
} clean {
  print ["Cleanup done"]
}
```

Lowered into IR with:

* `landingpad` blocks in LLVM IR.
* `catch`, `clean`, `retry` → structured unwind handlers.

---

## 5. Optimizations

Always-on optimizations:

* **Constant Folding**
* **Loop Unrolling**
* **Tail Call Optimization**
* **Peephole Passes**
* **Profile-Guided Optimization (PGO)**
* **SIMD Vectorization**

No compiler flags needed — baked in.

---

## 6. Interoperability

* Functions exposed via **C ABI**.
* Can import external C functions:

```neopaquet
extern ("puts") [s]
src () "stdout" { puts("Hello from C!") } run
```

* Compiles into symbols directly linkable with:

  * C, C++, Rust, Go
  * Unity, Unreal, OpenGL, Vulkan

---

## 7. Example Compilation

### Source

```neopaquet
src () "stdout" {
  print ["Hello NeoPaquet!"]
} run
```

### LLVM IR

```llvm
@.str0 = private constant [16 x i8] c"Hello NeoPaquet!\00"
define i32 @main() {
entry:
  %0 = getelementptr [16 x i8], [16 x i8]* @.str0, i32 0, i32 0
  call i32 (i8*, ...) @printf(i8* %0)
  ret i32 0
}
```

### NASM

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

```bash
./hello.exe
Hello NeoPaquet!
```

---

## 8. Roadmap

Planned:

* Namespaces + imports
* WASM backend
* Package manager (`npkg`)
* NeoPaquet VM (NP-VM)

See [ROADMAP.md](../ROADMAP.md).

---

## 9. Conclusion

NeoPaquet is a **serious, execution-oriented systems language**:

* Lightweight, AOT-compiled
* Native interop baked in
* Formal dodecagram AST
* Designed for performance, security, and machine-friendliness

Contribute via [CONTRIBUTING.md](../CONTRIBUTING.md).

```

---

## ✅ What This Adds
- A **developer-facing “mini-book”** on how NeoPaquet works internally.  
- Explains **each stage of compilation** clearly with examples.  
- Includes **sample lowering** from NeoPaquet → LLVM IR → NASM → Executable.  
- Links to roadmap and contributing docs.  

---

⚡
