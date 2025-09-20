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
