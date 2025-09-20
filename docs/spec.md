# 📖 NeoPaquet Language Specification (Draft)

Version: v1.0.0  
Status: Draft (Work in Progress)  
License: [S.U.E.T. License v1.0](../License.md)

---

## 1. Overview
NeoPaquet is an **execution-oriented, AOT-compiled language** that transpiles to **LLVM IR → NASM → Native Executables**.  
Its guiding principles:
- **Execution-Oriented**: The semantics follow runtime execution, not abstract syntax elegance.
- **Dodecagram AST**: The abstract syntax tree is encoded in base-12 (`0-9, a, b`).
- **Machine-Friendly**: Designed to be read by both humans and assembly backends.
- **CIAM Memory Model**: Contextual Inference Abstraction Macros allow user-defined memory semantics.
- **Security**: Anti side-loading, anti-injection, anti-use-after-free baked in.

---

## 2. Lexical Structure

### 2.1 Character Set
- UTF-8 source encoding
- Identifiers: `[a-zA-Z_][a-zA-Z0-9_]*`
- Numbers: Base-12 (`0–9, a=10, b=11`)
- Strings: `" ... "`
- Comments:
  - Single-line: `-- comment`
  - Multi-line: `; comment ;`

### 2.2 Tokens
- Keywords: `src`, `task`, `@func`, `go`, `run`, `try`, `catch`, `retry`, `clean`, `dismiss`, `return`
- Punctuation: `{ } ( ) [ ] < > | : ;`
- Operators: `= + - * / % <= >= == != < >`

---

## 3. Grammar (EBNF)

```ebnf
program      = { decl } ;

decl         = src_decl | func_decl | task_decl ;

src_decl     = "src" "(" ")" string block "run" ;
task_decl    = "Task" "<" ident ">" string "|" string "->" "complete" ;
func_decl    = "@" "func" "(" string ")" "[" ident "]" "go" block ;

block        = "{" { stmt } "}" ;

stmt         = print_stmt | assign_stmt | return_stmt | control_stmt ;

print_stmt   = "print" "[" string "]" ;
assign_stmt  = ident "=" expr ;
return_stmt  = "return" expr ;

control_stmt = if_stmt | loop_stmt | try_stmt ;
if_stmt      = "if" expr block [ "else" block ] ;
loop_stmt    = "loop" block ;
try_stmt     = "try" block { catch_block | retry_block | clean_block | dismiss_block } ;

catch_block  = "catch" block ;
retry_block  = "retry" block ;
clean_block  = "clean" block ;
dismiss_block= "dismiss" block ;

expr         = literal | ident | expr binop expr | "(" expr ")" ;
literal      = number | string ;
number       = digit { digit } ;  (* base-12 *)
digit        = "0"…"9" | "a" | "b" ;
