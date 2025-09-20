 ⚡ NeoPaquet Cheatsheet
Quick reference for the **NeoPaquet Language** — Execution-Oriented, Base-12, AOT compiled.

---

## 🧩 Program Structure
```neopaquet
src () "stdout" {
  print ["Hello NeoPaquet!"]
} run
````

* `src () "stdout" { ... } run` → entry point
* Blocks always wrapped in `{ }`
* Execution is always **oriented** (flows directly into machine code)

---

## 🔢 Numbers

NeoPaquet uses **base-12 (dodecagram)**:

* Digits: `0–9, a=10, b=11`
* Example:

  * `5a` → 70 decimal
  * `1b` → 23 decimal

---

## 🏷️ Keywords

| Keyword   | Purpose                            |
| --------- | ---------------------------------- |
| `src`     | Entry point declaration            |
| `run`     | Terminates a `src` block           |
| `@func`   | Function definition                |
| `go`      | Start of function body             |
| `Task`    | Special task block (workflow jobs) |
| `return`  | Return value from function         |
| `loop`    | Loop block                         |
| `if/else` | Conditional execution              |
| `try`     | Error handling start               |
| `catch`   | Handle error                       |
| `retry`   | Re-execute block on failure        |
| `clean`   | Always executed (like finally)     |
| `dismiss` | Abort execution safely             |

---

## 🛠️ Operators

| Operator  | Meaning          |
| --------- | ---------------- |
| `=`       | Assignment       |
| `+ - * /` | Arithmetic       |
| `%`       | Modulus          |
| `< <=`    | Less, less/equal |
| `> >=`    | Greater, geq     |
| `== !=`   | Equality, not    |

---

## 🖨️ Printing

```neopaquet
print ["Hello!"]
x = 5a
print [x]
```

---

## 🔁 Loops

```neopaquet
i = 0
loop {
  print [i]
  i = i + 1
  if i == 5 {
    break
  }
}
```

---

## 🔀 Conditionals

```neopaquet
if x > 5 {
  print ["big"]
} else {
  print ["small"]
}
```

---

## 📦 Functions

```neopaquet
@func ("square") [n] go {
  return n * n
}

src () "stdout" {
  print [square(7)]
} run
```

---

## ⚡ Error Handling

```neopaquet
try {
  x = 10 / 0
} catch {
  print ["error caught"]
} clean {
  print ["cleanup"]
}
```

---

## 🧩 CIAM Memory Macros (draft)

```neopaquet
mem.arena { size=1024 }
mem.slice { start=0, len=12 }
```

* User-defined contextual macros for memory safety.

---

## 🌐 Interop

* Functions exposed to **C ABI** automatically.
* Directly imports C libraries or exports functions:

```neopaquet
@func ("square") [n] go { return n * n }
```

---

## 🛠 Compilation

```bash
# Native executable
npaquetc hello.np -o hello.exe

# Emit LLVM IR
npaquetc hello.np --emit llvm -o hello.ll

# Emit NASM assembly
npaquetc hello.np --emit asm -o hello.asm
```

---

## 🚀 Optimizations (Always On)

* Constant folding
* Peephole passes
* Loop unrolling
* Tail-call elimination
* Profile-guided optimization (PGO)
* Intrinsic vectorization

---

## 📜 Attribution

* Language: **NeoPaquet**
* License: **[S.U.E.T. License v1.0](../License.md)**

```

---

## ✅ What This Adds
- **Quick syntax overview** for daily reference.  
- **Keyword + operator tables** (like a real language spec).  
- **Common patterns**: printing, loops, conditionals, functions, error handling.  
- **Interop + compilation commands** at a glance.  
- Linked to **License.md** for attribution.  

---

