# 🧩 NeoPaquet Example Programs

This folder contains **ready-to-run `.np` source files** to help you learn NeoPaquet step by step.
Each example introduces a new concept — from *Hello World* to *error handling* and *C interop*.

---

## 1. `hello_world.np`

**Concepts:** Basic program structure, `src` block, printing.

```neopaquet
src () "stdout" {
  print ["Hello NeoPaquet!"]
} run
```

➡️ The simplest NeoPaquet program. Demonstrates **printing to stdout**.

---

## 2. `factorial.np`

**Concepts:** Functions, recursion, return values.

```neopaquet
@func ("factorial") [n] go { ... }
```

➡️ Shows how to **define a recursive function** (`factorial`) and call it.

---

## 3. `fibonacci.np`

**Concepts:** Recursion, loops, conditionals.

```neopaquet
loop { print [fib(i)] ... }
```

➡️ Combines **recursion + looping** to print Fibonacci numbers.

---

## 4. `base12_math.np`

**Concepts:** Base-12 numbers, arithmetic, printing.

```neopaquet
x = 5a   -- base-12 for 70
y = b    -- base-12 for 11
```

➡️ Demonstrates NeoPaquet’s **dodecagram (base-12)** numeric system.

---

## 5. `matrix_mult.np`

**Concepts:** Arithmetic, grouped variables, structured output.

```neopaquet
c11 = a11*b11 + a12*b21
```

➡️ Implements a **2x2 matrix multiplication** — shows how to do multi-step math operations.

---

## 6. `error_handling.np`

**Concepts:** `try`, `catch`, `clean` blocks.

```neopaquet
try { x = 10 / 0 } catch { ... } clean { ... }
```

➡️ Shows NeoPaquet’s **execution-aware error handling model**.

---

## 7. `interop_c.np`

**Concepts:** Exposing functions to C ABI.

```neopaquet
@func ("square") [n] go { return n * n }
```

➡️ Demonstrates **C interoperability** — NeoPaquet functions can be called directly from C.

---

## 8. `loop_test.np`

**Concepts:** Loops, conditionals, breaking execution.

```neopaquet
loop { print [i] ... if i == 5 { break } }
```

➡️ Simple **loop with counter** — shows looping and exit conditions.

---

# 🚀 Running Examples

From the project root:

```bash
npaquetc docs/examples/hello_world.np -o hello.exe
./hello.exe
```

Run any of the other examples the same way:

```bash
npaquetc docs/examples/factorial.np -o factorial.exe
./factorial.exe
```

---

# 🎯 Learning Path

1. **hello\_world.np** → Printing
2. **base12\_math.np** → Numbers & arithmetic
3. **loop\_test.np** → Loops
4. **factorial.np** → Functions & recursion
5. **fibonacci.np** → Combining recursion + loops
6. **matrix\_mult.np** → Structured math example
7. **error\_handling.np** → Robust execution model
8. **interop\_c.np** → C interoperability

---

Would you like me to also create a **`docs/cheatsheet.md`** — a one-page quick reference of all syntax (keywords, operators, number system, blocks) — so developers can learn NeoPaquet at a glance?
