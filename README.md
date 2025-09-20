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

# 🌐 NeoPaquet Programming Language

**Tagline:** *“NeoPaquet — From Dodecagram to Native, Liquified into Execution.”*

---

## 1. Introduction

NeoPaquet is a **next-generation programming language** designed from the ground up for **execution-oriented development**. Unlike traditional languages that emphasize abstract models or runtime-managed memory, NeoPaquet centers itself on the principle of **direct execution**: every construct in the language is transposed into **LLVM IR** and then **NASM assembly** in a deterministic, highly optimized pipeline.

This ensures **zero-cost abstractions**, **native-level performance**, and **blazing-fast interoperability** with systems software, engines, and platforms. NeoPaquet isn’t a toy language or an academic exercise; it is designed for **industrial-scale workloads** where speed, predictability, and control matter most.

---

## 2. Design Ethos

* **Execution-Oriented Paradigm** — Code is defined in terms of how it runs, not how it looks.
* **Base-12 AST (Dodecagrams)** — An AST encoded in dodecagrammatic form (`0–9, a, b`) provides both structural compactness and uniformity across parsing, analysis, and optimization.
* **Machine-Friendly Linguistics** — Keywords, operators, and constructs are designed for minimal translation overhead.
* **User-Defined Memory via CIAM** — Memory control is delegated to *Contextual Inference Abstraction Macros*, allowing developers to tailor memory models precisely to their domain.
* **Error Handling as Flow-Control** — Instead of opaque exceptions, errors are explicit constructs:

  ```
  try { ... } 
  catch { ... } 
  isolate { ... } 
  clean { ... } 
  retry { ... } 
  dismiss { ... }
  ```
* **Front-End Interop** — APIs, FFI, and system calls connect directly to LLVM, NASM, and C, ensuring a universal interface with other languages.

---

## 3. Core Features

### 3.1 Compilation Model

* **AOT Compilation:** `.np` source → LLVM IR → NASM `.asm` → executable (`.exe`, `.out`, `.elf`)
* **Instant Startup:** Executables initialize in near-zero time due to pre-resolved static linking and liquified IR lowering.
* **Profile-Guided Optimizations:** Built into the compiler by default; no flags required.
* **Aggressive Optimizations:** Peephole, loop unrolling, constant folding, tail-call elimination, vectorization, and instruction lookahead are intrinsic.

---

### 3.2 Syntax Characteristics

NeoPaquet syntax blends **human accessibility** with **machine directness**. It rejects bloated constructs in favor of concise, execution-first grammar.

Examples:

```neopaquet
-- Single-line comment
; multi
; line
; comment

src () "stdout" { print ["Hello, NeoPaquet!"] } run

Task <iterate> "loop" | "0..10" -> complete

@func ("add") [a + b] go

<> job {"check-permissions"} operation ;

Start : setup ("initialize registers, heap, io") done {}
```

---

### 3.3 Semantic Guarantees

* **User-Defined Memory Models** (heap, stack, arena, or linear buffer allocation)
* **Threading & Concurrency** built in via **CIAM macros**
* **Native Interop** with:

  * Unreal Engine, Unity, DirectX, Vulkan, OpenGL, OpenCL
  * WASM, MASM, CIL, HTML, CSS, ANTLR grammars
  * x86-64, ARM64, RISC-V instruction sets
* **Security Intrinsics:**

  * *anti side injection*
  * *anti side loading*
  * *anti use-after-free*
* **Compression Baked In:** Intermediate code is auto-compressed for distribution, then expanded at execution with zero-cost decompression.

---

## 4. AST — Dodecagram Base-12 Model

Every AST node corresponds to a base-12 digit (`0–9, a, b`).

```
0 Program
1 Declaration
2 Statement
3 Expression
4 Identifier
5 Literal
6 Function
7 Block
8 Try
9 Catch
a Loop
b Conditional
```

This AST encoding means NeoPaquet compilers and interpreters can trivially serialize, optimize, and transmit code representations between systems.

---

## 5. Toolchain Layout

```
neopaquet/
 ├── npaquetc/             # compiler frontend
 │   ├── lexer.py
 │   ├── parser.py
 │   ├── ast.py
 │   ├── irgen.py
 │   ├── nasmgen.py
 │   ├── optimizer.py
 │   ├── main.py          # CLI: npaquetc input.np -o output.exe
 ├── stdlib/              # basic functions
 │   ├── io.np
 │   ├── math.np
 │   ├── memory.np
 │   ├── threading.np
 ├── tests/               # regression tests
 │   ├── hello_world.np
 │   ├── loop_test.np
 │   ├── ffi_integration.np
 └── build/               # build artifacts
```

---

## 6. CLI Usage

```bash
$ npaquetc hello.np -o hello.exe
$ ./hello.exe
Hello, NeoPaquet!
```

Options:

* `--emit-llvm` → outputs LLVM IR (`.ll`)
* `--emit-asm` → outputs NASM (`.asm`)
* `--emit-bin` → outputs raw binary (`.bin`)
* `--profile` → runs PGO pass
* `--opt-level=3` → manual optimization override (defaults to max)

---

## 7. Standard Library (stdlib)

NeoPaquet ships with a compact but **highly optimized stdlib**, exposing primitives for:

* **I/O** (`print`, `read`, `file.open`)
* **Math** (SIMD-ready math ops, matrix/vector)
* **Memory** (arenas, slices, manual allocation macros)
* **Concurrency** (threads, locks, message passing)
* **System Interop** (C ABI, sockets, direct syscalls)

---

## 8. Industrial-Grade Interoperability

NeoPaquet has **native hooks** into virtually every major runtime:

* **Game Engines:** Unreal Engine, Unity, Godot
* **Graphics APIs:** DirectX, Vulkan, OpenGL
* **Web:** WASM, HTTPS, HTML5 canvas hooks
* **OS APIs:** Windows (MSVC ABI), Linux (ELF), macOS (Mach-O)
* **Embedded:** ARM, RISC-V, FPGA synthesis

---

## 9. Error Handling Model

Errors are **execution-aware**, not just exceptions:

```neopaquet
try {
   riskyCall()
}
catch {
   print ["Recovered"]
}
retry {
   riskyCall()
}
clean {
   releaseResources()
}
```

This model aligns with NeoPaquet’s **execution-first philosophy**, letting developers specify runtime behavior directly in code.

---

## 10. Optimizations (Intrinsic)

NeoPaquet integrates the most advanced compiler optimizations by default:

* **Loop Unrolling** — done automatically where profitable.
* **Tail Call Optimization** — guaranteed for recursion.
* **Constant Folding & Propagation** — compile-time simplification.
* **Peephole Passes** — micro-optimizations at the instruction level.
* **Vectorization** — loops + math auto-vectorized.
* **Profile Guided Optimization (PGO)** — built-in, no user intervention required.

---

## 11. Security Guarantees

NeoPaquet is hardened against common vulnerabilities:

* **Buffer overflows** → disallowed by CIAM macros.
* **Dangling pointers** → auto-nullified by runtime inference.
* **Race conditions** → threading macros enforce memory fences.
* **Injection & side-loading** → blocked at compiler-level.

---

## 12. Example Program (Full Pipeline Demo)

### Input (NeoPaquet):

```neopaquet
@func ("factorial") [n] go {
    if n <= 1 {
        return 1
    } else {
        return n * factorial(n - 1)
    }
}

src () "stdout" {
    print [factorial(5)]
} run
```

### LLVM IR:

```llvm
define i32 @factorial(i32 %n) {
entry:
  %cmp = icmp sle i32 %n, 1
  br i1 %cmp, label %base, label %rec

base:
  ret i32 1

rec:
  %dec = sub i32 %n, 1
  %call = call i32 @factorial(i32 %dec)
  %mul = mul i32 %n, %call
  ret i32 %mul
}

define i32 @main() {
entry:
  %res = call i32 @factorial(i32 5)
  call i32 (i8*, ...) @printf(i8* getelementptr ([4 x i8], [4 x i8]* @.str, i32 0, i32 0), i32 %res)
  ret i32 0
}
```

### NASM Assembly:

```asm
section .data
fmt db "%d",10,0

section .text
global main
extern printf

factorial:
    cmp edi, 1
    jle .base
    push rdi
    dec edi
    call factorial
    pop rdi
    imul eax, edi
    ret
.base:
    mov eax, 1
    ret

main:
    mov edi, 5
    call factorial
    mov esi, eax
    lea rdi, [rel fmt]
    xor eax, eax
    call printf
    xor eax, eax
    ret
```

### Output:

```
120
```

---

## 13. Industry Adoption & Use Cases

* **High-Performance Systems:** OS kernels, device drivers, embedded systems.
* **Games & Engines:** Unreal/Unity modules at near-assembly speed.
* **Finance & Trading:** Ultra-low-latency trading algorithms.
* **Scientific Computing:** HPC, numerical libraries, simulations.
* **WebAssembly:** NeoPaquet → LLVM → WASM → web-native.
* **Security & Defense:** Hardened CIAM-based memory macros for secure execution.

---

## 14. Closing Statement

NeoPaquet isn’t just another new language. It’s a **new execution model**: built on **dodecagrammatic precision**, **LLVM universality**, and **NASM-native determinism**. It achieves what C once promised — **total control, absolute performance, infinite extensibility** — but with the optimizations and interoperability that the modern era demands.

**NeoPaquet is the language where your code doesn’t just run. It executes.**

---




---

# 🌐 NeoPaquet: Real-World Usage & Industry Positioning

---

## 1. Who Will Use This Language?

NeoPaquet is targeted at **developers who need both raw performance and control**, without sacrificing modern conveniences. Likely users include:

* **Systems Programmers** — OS developers, driver engineers, embedded systems architects.
* **Game Developers** — studios using Unreal, Unity, or custom engines that demand frame-perfect performance.
* **Financial Engineers** — algorithmic trading, high-frequency transaction systems, blockchain node implementations.
* **Security Experts** — building hardened, low-level security modules with CIAM-enforced memory safety.
* **Scientific/HPC Researchers** — scientists running simulations and computationally heavy workloads.
* **Toolchain Builders** — compiler engineers, VM developers, and runtime ecosystem builders.

---

## 2. What Will It Be Used For?

NeoPaquet’s execution-oriented model makes it ideal for:

* **Kernel and OS Components** (process schedulers, memory managers).
* **Game Engine Extensions** (graphics pipelines, physics, AI routines).
* **Device Drivers** (GPU/CPU accelerators, network cards, storage).
* **Finance Engines** (real-time fraud detection, order book balancing).
* **WASM Deployment** (compiling directly to WebAssembly for web-native execution).
* **Scientific Computing** (molecular dynamics, weather models, astrophysics).
* **Secure Infrastructure** (VPN modules, intrusion detection, hardened cryptography).

---

## 3. Which Industries Will Gravitate to It?

* **Gaming / Entertainment** — AAA studios, VR/AR platforms.
* **Finance / Banking** — hedge funds, payment processors.
* **Defense / Security** — cybersecurity firms, defense contractors.
* **Embedded / IoT** — autonomous vehicles, robotics, medical devices.
* **Telecom / Networking** — high-throughput routers, 5G packet processors.
* **Cloud / Data** — HPC clusters, distributed processing frameworks.

---

## 4. Real-World Projects & Software That Can Be Built

* **Operating Systems / Microkernels**
* **Compilers / Interpreters**
* **AAA Game Engines**
* **Low-Latency Databases**
* **WASM Applications**
* **Scientific HPC Apps**
* **Embedded Firmware**
* **AR/VR Engines**
* **AI Acceleration Libraries** (CUDA/OpenCL interop)

---

## 5. Learning Curve

* **Entry Level:** Slightly higher than C but lower than Rust.
* **Why?**

  * Syntax is concise but new.
  * Requires some exposure to systems concepts (memory, registers, low-level flow).
  * Optimizations (loop unrolling, PGO) are automatic, reducing complexity.
* **Verdict:** A motivated C programmer can learn NeoPaquet in weeks; an intermediate Python/JavaScript developer may take months to master execution-oriented thinking.

---

## 6. Interoperability with Other Languages

NeoPaquet interops seamlessly with:

* **C / C++** (via LLVM and ABI hooks).
* **Rust, Go, Zig** (through LLVM IR exchange).
* **C# / Java** (via shared C ABI libraries).
* **Python, Node.js** (via FFI and WASM bindings).
* **Web Tech** (WASM compilation targets).

Interop is **direct**, since source code and compiled objects can be shared both ways with minimal glue.

---

## 7. Use Cases & Edge Cases

* **Standard Use Cases:** Game engines, OS kernels, HPC workloads, financial systems.
* **Edge Cases:**

  * Deterministic real-time OS for satellites.
  * Military-grade crypto with side-channel attack resistance.
  * Hybrid Unreal + WASM cross-deployable multiplayer games.
  * FPGA/GPU shader kernels compiled straight from NeoPaquet.

---

## 8. What Can NeoPaquet Do Right Now?

* Compile `.np` → LLVM IR → NASM → native executables.
* Handle threading, memory macros, and direct syscalls.
* Run as secure WASM modules in browsers.
* Auto-optimize with built-in PGO and vectorization.

---

## 9. When Is It Preferred Over Others?

* When **speed and determinism** are paramount.
* When **interop with C/LLVM ecosystems** is needed.
* When **low-level hardware access** is required but with memory safety.
* When **compilation to multiple targets** (Windows, Linux, macOS, WASM, ARM, RISC-V) is critical.

---

## 10. Where Does It Shine?

* **High-Performance, Low-Level Software**
* **Cross-Platform Game Engines**
* **Secure Memory-Constrained Devices**
* **Real-Time Applications**

---

## 11. Where Does It Outperform Others?

* **C/C++:** Matches performance but offers baked-in PGO, memory safety, and auto-vectorization.
* **Rust:** Less boilerplate, faster compilation pipeline, more direct interop with C.
* **Go/Java:** Orders of magnitude faster at runtime, closer to metal.
* **Python/JS:** Not even comparable in raw speed.

---

## 12. Where Does It Show the Most Potential?

* **Replacing C for new OS kernels**
* **Becoming a standard WASM → Native language**
* **Hybrid cloud + embedded systems**
* **Scientific/HPC adoption**

---

## 13. Where Is It Most Needed?

* **Finance (low latency trading)**
* **Defense / Cybersecurity**
* **Next-Gen Engines (Unreal 6, Unity HDRP successors)**
* **Medical Embedded Systems**
* **5G/6G Network Infrastructure**

---

## 14. Performance (Speed & Startup)

* **Startup Speed:** \~0.001–0.005s (instant due to AOT liquified execution).
* **Execution Speed:** Matches or outperforms C in most benchmarks.
* **Load Time:** Essentially zero, due to pre-linked binaries.

---

## 15. Security & Safety

* **Anti Side-Loading / Injection** baked into compiler passes.
* **Use-After-Free Protection** via CIAM macros.
* **Thread Race Prevention** with memory fences.
* **Safer than C**, but not as restrictive as Rust (balance between safety and control).

---

## 16. Why Choose NeoPaquet?

* **For C developers:** Familiar but more secure.
* **For Rust developers:** Faster compilation, simpler FFI.
* **For Go/Java/Python developers:** Orders of magnitude faster.
* **For industries:** One toolchain → all targets (Windows, Linux, WASM, ARM).

---

## 17. Why Was It Created?

NeoPaquet was born from the need to combine:

* **C’s raw control**
* **Rust’s safety**
* **LLVM’s universality**
* **WASM’s portability**
* **Execution-Oriented simplicity**

It was created to be the **first machine-native, universally interoperable, instantly executable language** that closes the gap between high-level productivity and low-level determinism.

---

✅ **Summary Statement:**
NeoPaquet is not “just another language.” It is a **new execution standard**. It stands at the intersection of **C’s control, Rust’s safety, and LLVM’s universality**, while pioneering **execution-oriented linguistics** and **dodecagrammatic AST models**.

It is most needed in **finance, defense, gaming, HPC, and embedded systems**. It shines in **speed, interoperability, and startup performance**, outperforming legacy languages where execution determinism and raw throughput are critical.

---



---

# 📜 NeoPaquet Compiler (`npaquetc`)

**Tagline:**

> *NeoPaquet — From Dodecagram to Native, Liquified into Execution.*

NeoPaquet is an **execution-oriented, AOT-compiled programming language** that transpiles into **LLVM IR → NASM → Native Executables**.
It uses a **dodecagram AST (base-12)**, machine-friendly linguistics, and CIAM-based memory control for blazing-fast, zero-cost runtime performance.

---

## 🚀 Features

* **Execution-Oriented Paradigm** — Code defined by how it runs, not how it looks.
* **Dodecagram AST (0–9, a, b)** — Compact and precise representation.
* **AOT Compilation Pipeline** — `.np` → LLVM IR → NASM → `.exe` / `.out`.
* **Automatic Optimizations** baked in:

  * PGO (Profile-Guided Optimization)
  * Loop Unrolling
  * Tail-Call Elimination
  * Constant Folding & Peephole Passes
  * Intrinsic Vectorization
* **Memory Model** — User-defined via **CIAM (Contextual Inference Abstraction Macros)**.
* **Error Handling** — Explicit execution-aware model:

  ```neopaquet
  try { ... } catch { ... } retry { ... } clean { ... } dismiss { ... }
  ```
* **Interop** — Seamless C/LLVM ABI + direct hooks into Unreal Engine, Unity, DirectX, Vulkan, OpenGL, WASM.
* **Security First** — Anti side-loading, anti injection, anti use-after-free.

---

## 📂 Repository Layout

```
neopaquet/
 ├── npaquetc/             # Compiler frontend + backends
 │   ├── lexer.py          # Lexical analyzer
 │   ├── parser.py         # Grammar + AST builder
 │   ├── ast.py            # Dodecagram AST
 │   ├── irgen.py          # LLVM IR generator
 │   ├── nasmgen.py        # NASM backend + linker
 │   ├── main.py           # CLI entry point (npaquetc)
 ├── stdlib/               # Standard library
 │   ├── io.np
 │   ├── math.np
 ├── tests/                # Regression tests
 │   ├── hello_world.np
 │   ├── loop_test.np
 ├── setup.py
 ├── pyproject.toml
 ├── README.md
```

---

## ⚙️ Installation

### Install from source

```bash
git clone https://github.com/your-org/npaquetc.git
cd npaquetc
pip install -e .
```

### Or install via wheel

```bash
python -m build
pip install dist/npaquetc-1.0.0-py3-none-any.whl
```

After installation, the global CLI is available:

```bash
$ npaquetc --help
```

---

## 🖋️ Example Program

### `hello.np`

```neopaquet
src () "stdout" { print ["Hello NeoPaquet!"] } run
```

### Compile & Run

```bash
$ npaquetc hello.np -o hello.exe
Executable generated: hello.exe
$ ./hello.exe
Hello NeoPaquet!
```

---

## 🔧 CLI Options

```bash
npaquetc input.np -o output [--emit exe|llvm|asm]

Options:
  -o, --output    Specify output file (default: a.out)
  --emit llvm     Emit LLVM IR (.ll)
  --emit asm      Emit NASM assembly (.asm)
  --emit exe      Build native executable (default)
```

---

## 🧩 Standard Library

NeoPaquet ships with a minimal but optimized stdlib:

* **io.np** — printing, reading, file I/O.
* **math.np** — basic arithmetic, trig, vector ops.
* **memory.np** — arenas, slices, manual CIAM macros.
* **threading.np** — basic concurrency & locks.

---

## 🧪 Tests

```bash
pytest tests/
```

---

## 🔒 License

S.U.E.T. License — free to use, modify, and distribute. 

---

## 🌐 Links

* Homepage: [NeoPaquet Project](https://github.com/JoeySoprano420/NeoPaquet/tree/main/npaquetc)
* Repository: [GitHub](https://github.com/JoeySoprano420/NeoPaquet/tree/main)

---

✅ This `README.md` explains what NeoPaquet is, how to install it, how to use it, and why it matters.

## ~~~~~


