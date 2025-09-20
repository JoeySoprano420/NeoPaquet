## *****
# 🧑‍💻 NeoPaquet Tutorial
Welcome to **NeoPaquet** — an execution-oriented, AOT-compiled language that goes from source → LLVM IR → NASM → native executables.  
This tutorial will walk you through writing, compiling, and running your first programs.

---

## 1. Installing NeoPaquet
Make sure you have:
- **Python 3.9+**
- **LLVM toolchain** (for llvmlite + linking)
- **Clang/LLD** or system linker
- **NASM** (optional for manual inspection)

Clone the repo:
```bash
git clone https://github.com/JoeySoprano420/NeoPaquet.git
cd NeoPaquet
pip install -e .
````

Check installation:

```bash
npaquetc --help
```

---

## 2. Your First Program

### `hello.np`

```neopaquet
src () "stdout" {
  print ["Hello NeoPaquet!"]
} run
```

Compile and run:

```bash
npaquetc hello.np -o hello.exe
./hello.exe
```

Output:

```
Hello NeoPaquet!
```

---

## 3. Numbers in Base-12

NeoPaquet uses **dodecagram (base-12)** numbers:

* `0-9` are standard digits
* `a` = 10
* `b` = 11

Example:

```neopaquet
src () "stdout" {
  x = 5a   -- base-12 = (5 * 12) + 10 = 70
  print [x]
} run
```

---

## 4. Functions

### Factorial Example

```neopaquet
@func ("factorial") [n] go {
  if n <= 1 {
    return 1
  } else {
    return n * factorial(n - 1)
  }
}

src () "stdout" {
  result = factorial(5)
  print ["Factorial of 5 is:"]
  print [result]
} run
```

Run:

```
Factorial of 5 is:
5a0   -- base-12 result for 120
```

---

## 5. Control Flow

### If/Else

```neopaquet
src () "stdout" {
  x = 7
  if x > 5 {
    print ["x is big"]
  } else {
    print ["x is small"]
  }
} run
```

### Loops

```neopaquet
src () "stdout" {
  i = 0
  loop {
    print [i]
    i = i + 1
    if i == 5 {
      break
    }
  }
} run
```

---

## 6. Error Handling

NeoPaquet has **execution-aware errors**:

```neopaquet
src () "stdout" {
  try {
    x = 10 / 0
  } catch {
    print ["Divide by zero caught!"]
  } clean {
    print ["Cleanup executed."]
  }
} run
```

Output:

```
Divide by zero caught!
Cleanup executed.
```

---

## 7. Interop with C

NeoPaquet functions are automatically **C ABI exposed**:

```neopaquet
@func ("square") [n] go {
  return n * n
}
```

C code can call `square()` like a normal function.
Interop works both ways: you can also `import` external C functions.

---

## 8. Inspecting Output

Emit LLVM IR:

```bash
npaquetc hello.np --emit llvm -o hello.ll
cat hello.ll
```

Emit NASM assembly:

```bash
npaquetc hello.np --emit asm -o hello.asm
cat hello.asm
```

---

## 9. Standard Library

NeoPaquet ships with a **minimal stdlib**:

* `io.np` → printing, reading
* `math.np` → arithmetic, trig, vector ops
* `memory.np` → CIAM macros
* `threading.np` → concurrency primitives

Usage:

```neopaquet
import "stdlib/math.np"

src () "stdout" {
  y = sqrt(25)
  print [y]
} run
```

---

## 10. Next Steps

* Read the [Specification](spec.md) for formal grammar & semantics.
* Explore the [Roadmap](../ROADMAP.md) for upcoming features.
* Contribute to NeoPaquet via [CONTRIBUTING.md](../CONTRIBUTING.md).

---

## 🎯 Summary

You learned:

* Writing and compiling programs
* Base-12 numbers
* Functions, loops, if/else
* Error handling
* Interop with C
* Inspecting LLVM/NASM output

NeoPaquet is still evolving — your feedback and contributions can shape its future.

```

---



⚡ Do you want me to also create a **`docs/examples/` folder** with multiple ready-to-run `.np` sample programs (hello world, factorial, fibonacci, matrix multiply, error handling, etc.)?
```
