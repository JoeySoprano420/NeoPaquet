# NeoPaquet



---

# 🌐 NeoPaquet Language Specification (Draft v0.1)

## 1. Core Identity

* **Name:** NeoPaquet
* **Paradigm:** Execution-Oriented (EO)
* **AST Representation:** Dodecagrams base-12 (`0–9,a,b`)
* **Grammar:** Written in hybrid **Dodecagram tokens + NASM-style mnemonics**
* **Semantics:** Low-level, C-like
* **Compilation:** Ahead-of-Time (AOT) → LLVM IR → NASM → `.exe` / `.out` / `.elf`

---

## 2. Language Characteristics

* **Memory Model:** User-defined / CIAM (Contextual Inference Abstraction Macro)
* **Error Handling:**

  ```
  try { ... } 
  catch { ... } 
  isolate { ... } 
  clean { ... } 
  retry { ... } 
  dismiss { ... }
  ```
* **Interop:** Source automatically exposed to C and C to NeoPaquet (via LLVM FFI layer).
* **Inlining:** Automatic / baked in.
* **Optimizations baked in:** PGO, TCO, loop unrolling, constant folding, peephole, lookahead, vectorization, etc.
* **Security baked in:** anti side injection, anti side loading, anti use-after-free.
* **Runtime:** Zero-cost native speed.

---

## 3. Example Syntax

```neopaquet
-- single line comment
; multi
; line
; comment

src () "stdout" { print ["Hello, NeoPaquet!"] } run

Task <iterate> "loop" | "0..10" -> complete

@func ("sum") [a + b] go

<> job {"validate"} operation ;

Start : setup ("init memory, registers") done
{}
```

---

## 4. Grammar (in Dodecagram + NASM Hybrid)

```
<program>   ::= <decl>* "run"
<decl>      ::= "src" "(" ")" <string> "{" <stmt>* "}"
              | "Task" "<" ident ">" <string> "|" <string> "->" "complete"
              | "@func" "(" <string> ")" "[" <stmt>* "]" "go"
              | "<>" "job" "{" <stmt>* "}" "operation" ";"
              | "Start" ":" "setup" "(" <string> ")" "done" "{}"

<stmt>      ::= ident "=" expr
              | "print" "[" <string> "]"
              | "if" expr "{" <stmt>* "}" ("else" "{" <stmt>* "}")?
              | "loop" range "{" <stmt>* "}"
              | trycatch

<trycatch>  ::= "try" "{" <stmt>* "}" "catch" "{" <stmt>* "}"
```

(AST nodes will be encoded in base-12).

---

## 5. AST in Base-12 (Dodecagram)

Every node is labeled `0–9,a,b`. For example:

```
0 Program
1 Declaration
2 Statement
3 Expression
4 Identifier
5 Literal
6 Function
7 Block
8 ErrorTry
9 ErrorCatch
a Loop
b If
```

---

## 6. Compilation Pipeline

1. **Lexer** → Tokenizes hybrid syntax (NeoPaquet grammar).
2. **Parser** → Builds AST (encoded in base-12 nodes).
3. **IR Generator** → AST → LLVM IR.
4. **NASM Generator** → LLVM IR → `.asm`.
5. **Assembler/Linker** → `.asm` → `.exe` / `.out`.

---

## 7. Toolchain Layout

```
neopaquet/
 ├── npaquetc/             # compiler frontend
 │   ├── lexer.py
 │   ├── parser.py
 │   ├── ast.py
 │   ├── irgen.py
 │   ├── nasmgen.py
 │   ├── main.py          # CLI: npaquetc input.np -o output.exe
 ├── stdlib/              # basic functions
 │   ├── io.np
 │   ├── math.np
 ├── tests/               # regression tests
 │   ├── hello_world.np
 │   ├── loop_test.np
 └── build/               # build artifacts

```

---

## 8. Sample Output Flow

Input (`hello.np`):

```neopaquet
src () "stdout" { print ["Hello World"] } run
```

LLVM IR (generated):

```llvm
@.str = private constant [12 x i8] c"Hello World\00"

define i32 @main() {
entry:
  %0 = getelementptr [12 x i8], [12 x i8]* @.str, i32 0, i32 0
  call i32 (i8*, ...) @printf(i8* %0)
  ret i32 0
}
```

NASM (lowered):

```asm
section .data
str db "Hello World",0

section .text
global main
extern printf
main:
    mov rdi, str
    xor rax, rax
    call printf
    xor rax, rax
    ret
```

---

## 9. CLI Usage

$ npaquetc hello.np -o hello.exe
$ ./hello.exe
Hello World

```

---

