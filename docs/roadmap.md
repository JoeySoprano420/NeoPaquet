# 📂 `docs/roadmap.md`

```markdown
# 🗺️ NeoPaquet Roadmap
*Future development milestones and priorities for the NeoPaquet project.*

---

## 🎯 Vision
NeoPaquet is built to be a **next-generation execution-oriented language**:  
- **Machine-friendly** by design.  
- **Blazing-fast** compilation (LLVM → NASM → native).  
- **Base-12 AST** for compactness and symbolic clarity.  
- **CIAM memory macros** for safe, zero-cost memory management.  
- **Interop-first** with C, LLVM, NASM, Unreal, Unity, WASM.  

This roadmap ensures NeoPaquet continues to evolve into a **full production-ready ecosystem**.

---

## 📌 Short-Term (0–6 months)

- **Language Features**
  - [ ] Expand CIAM macros: `arena`, `pool`, `slice`, `page`.  
  - [ ] More operators (`**`, `&&`, `||`).  
  - [ ] Extended error handling (`retry`, `dismiss`).  
  - [ ] Function overloading + default arguments.  

- **Compiler Improvements**
  - [ ] Better error messages.  
  - [ ] Symbol table introspection (`--dump-symtab`).  
  - [ ] Configurable optimizations (`--O0`, `--O2`, `--Ofast`).  

- **Ecosystem**
  - [ ] Publish first **PyPI release** (`npaquetc`).  
  - [ ] Example suite expanded in `docs/examples/`.  
  - [ ] Cheatsheet + guide updates.  

---

## 🚀 Mid-Term (6–18 months)

- **Core Language**
  - [ ] Namespaces + imports.  
  - [ ] Modules + package system.  
  - [ ] Pattern matching syntax.  
  - [ ] Type annotations + type inference.  

- **Backends**
  - [ ] **WASM** backend (browser + server).  
  - [ ] **ARM64** backend (Apple Silicon, embedded).  
  - [ ] **RISC-V** backend.  

- **Developer Tools**
  - [ ] LSP (Language Server Protocol) for editors.  
  - [ ] **VSCode Extension**: syntax highlighting, inline diagnostics.  
  - [ ] Playground REPL (`npaquetc repl`).  
  - [ ] CI/CD integration across all OS targets.  

---

## 🌍 Long-Term (18+ months)

- **NeoPaquet VM (NP-VM)**
  - Lightweight interpreter for fast prototyping.  
  - Debugger + breakpoints.  
  - Sandboxed execution mode.  

- **Ecosystem**
  - Package manager (`npkg`).  
  - Official **NeoPaquet Standard Library** (stdlib 1.0).  
  - Interop with Python, Rust, Go, JavaScript.  
  - Bindings for Unreal, Unity, Vulkan, OpenGL.  

- **Research & Expansion**
  - CIAM 2.0 → memory contracts and lifetimes.  
  - Parallel + distributed compilation.  
  - JIT compilation layer for hybrid use cases.  
  - Formal verification tooling.  

---

## 🛡️ Community Goals
- Open-source contribution model.  
- Friendly onboarding (`docs/guide.md`, `docs/contributor_guide.md`).  
- Transparent governance (community RFC process).  
- Cross-project collaboration (LLVM, WASM, OS dev communities).  

---

## 📅 Timeline Snapshot
| Stage         | Goals                               |
|---------------|-------------------------------------|
| Short-Term    | Features, PyPI release, examples    |
| Mid-Term      | Namespaces, WASM backend, IDE tools |
| Long-Term     | VM, Package Manager, Stdlib 1.0     |

---

## 📖 Related Docs
- [Architecture](architecture.md)  
- [Developer Internals](dev_internals.md)  
- [Contributor Guide](contributor_guide.md)  
- [Cheatsheet](cheatsheet.md)  

---
```

---

## ✅ What This Adds

* **Clear roadmap** with short-term, mid-term, long-term goals.
* Includes **compiler, language, ecosystem, and community milestones**.
* Tied directly to docs so contributors know where to look.
* Future-facing with **NP-VM, npkg, WASM, stdlib**.

---

⚡ 
