# 🛣️ NeoPaquet Roadmap

This document outlines the **planned development path** for the NeoPaquet programming language, compiler toolchain, and ecosystem.  
NeoPaquet is built to be **execution-oriented, AOT-compiled, dodecagram-driven, and machine-friendly**, with seamless interop across C, LLVM, NASM, and modern platforms.

---

## ✅ Current Status (v1.0.0)
- [x] Lexer (base-12 dodecagram + NASM grammar)
- [x] Parser → AST builder
- [x] AST representation (dodecagram nodes)
- [x] LLVM IR generator (llvmlite-based)
- [x] NASM backend + executable output
- [x] CLI (`npaquetc`) with `--emit llvm|asm|exe`
- [x] Cross-platform builds (Ubuntu, Windows, macOS, Kali Linux)
- [x] CI/CD workflows (PyPI + GitHub Release)
- [x] Documentation (`README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`)

---

## 🔜 Short-Term Goals (v1.1.x – v1.3.x)
- [ ] **Expanded Standard Library**
  - Math (advanced functions, vectors, matrices)
  - IO (file streams, formatted printing)
  - Memory (CIAM macros for arenas, slices, safe allocators)
  - Threads (locks, atomics, lightweight tasks)
- [ ] **Error Handling**
  - Full support for `try`, `catch`, `clean`, `retry`, `dismiss`
- [ ] **Control Flow Enhancements**
  - `if / else` lowering to LLVM IR
  - `loop`, `while`, `for` with unrolling baked in
- [ ] **Testing Infrastructure**
  - More regression tests in `tests/`
  - Add fuzzing for lexer/parser stability
- [ ] **Docs**
  - Syntax guide
  - Compiler architecture doc
  - Tutorials for beginners

---

## 🚀 Mid-Term Goals (v2.0.x – v2.5.x)
- [ ] **Optimizations**
  - Intrinsic vectorization (SIMD)
  - Deeper peephole passes
  - Profile-guided optimization integration
- [ ] **Interop**
  - Enhanced C FFI (headers → callable funcs)
  - WASM backend for web execution
  - Unity & Unreal integration modules
- [ ] **Language Features**
  - Namespaces + modules
  - Imports/exports
  - Inline assembly macros
- [ ] **Deployment**
  - Static builds
  - Cross-compilation (ARM64, RISC-V)
  - Package manager (`npkg`) for NeoPaquet libraries

---

## 🌌 Long-Term Vision (v3.0+)
- [ ] **Industrial Adoption**
  - NeoPaquet as a **systems programming language** alternative to C
  - Used in embedded systems, game engines, compilers, cryptography
- [ ] **Security Guarantees**
  - Compile-time memory safety checks (anti UAF baked in)
  - Sandboxing for untrusted code
- [ ] **NeoPaquet VM (NP-VM)**
  - Lightweight JIT/interpreter for rapid testing
  - Ahead-of-time cross-compilation
- [ ] **Research Path**
  - CIAM-based AI macro-suggestions
  - Optimized dodecagram IR analysis for HPC workloads
- [ ] **Ecosystem**
  - VSCode plugin (syntax highlighting, inline LLVM/NASM preview)
  - Official NeoPaquet Language Server (LSP)
  - Developer portal with docs + tutorials

---

## 🧭 Guiding Principles
1. **Execution-Oriented** — always prioritize runtime efficiency.  
2. **Machine-Friendly** — readable for both humans *and* assembly.  
3. **Cross-Interop** — never siloed, always connected to C/LLVM/NASM ecosystems.  
4. **Security by Design** — anti-side injection, UAF protection, attribution baked in.  
5. **Sovereign Licensing** — governed under the **S.U.E.T. License v1.0**.  

---

## 📢 How to Contribute
Check out our [CONTRIBUTING.md](CONTRIBUTING.md) for details on how you can help shape the NeoPaquet roadmap.

