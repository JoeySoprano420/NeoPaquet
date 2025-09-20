# 📂 `docs/contributor_guide.md`

````markdown
# 🤝 NeoPaquet Contributor Guide
*A practical manual for extending the NeoPaquet language.*

Welcome, contributor! 🎉  
This guide explains how to safely add **new keywords, operators, CIAM macros, and features** to NeoPaquet while keeping the compiler stable.

---

## 1. Contribution Principles

- **Execution-Oriented First** → Features must map directly to execution.  
- **Minimal Surface Area** → Every addition should be justified by real use cases.  
- **Consistent with Base-12 AST** → New constructs require a dodecagram ID.  
- **Cross-Platform Always** → Features must work on Linux, macOS, Windows, Kali.  
- **Tests Required** → All new features must include `.np` examples in `tests/`.

---

## 2. Adding a New Keyword

### Example: Adding `defer`
We want a keyword that runs code after a block exits.

#### Step 1: Lexer (`lexer.py`)
Add a token:
```python
KEYWORDS = {
    ...
    "defer": "DEFER",
}
````

#### Step 2: Parser (`parser.py`)

Define a grammar rule:

```python
elif tok.type == "DEFER":
    node = DeferStmt(self.parse_block())
```

#### Step 3: AST (`ast.py`)

Add node:

```python
class DeferStmt(ASTNode):
    id = "b"   # next base-12 ID
    def __init__(self, block):
        self.block = block
```

#### Step 4: IRGen (`irgen.py`)

Lower into LLVM IR:

```python
def visit_DeferStmt(self, node):
    # Insert block at function exit
    self.defer_blocks.append(node.block)
```

#### Step 5: Tests (`tests/defer_test.np`)

```neopaquet
src () "stdout" {
  print ["start"]
  defer { print ["exit"] }
} run
```

---

## 3. Adding a New Operator

### Example: `**` (power)

#### Lexer

```python
OPERATORS = { ..., "**": "POW" }
```

#### Parser

Add precedence rule in `parse_expr`.

#### IRGen

```python
if node.op == "POW":
    return self.builder.call(self.intrinsics["pow"], [lhs, rhs])
```

---

## 4. Adding a CIAM Macro

### Example: `mem.pool`

#### Step 1: Lexer

Add reserved word `"mem.pool"`.

#### Step 2: AST

```python
class MemPool(ASTNode):
    id = "a"
    def __init__(self, size):
        self.size = size
```

#### Step 3: IRGen

```python
alloc = self.builder.alloca(ir.ArrayType(ir.IntType(8), node.size))
```

#### Step 4: NASM

```asm
section .bss
pool resb <size>
```

---

## 5. Testing New Features

* Place `.np` tests in `tests/`.
* Use `pytest` for compiler pipeline.
* Example:

```bash
pytest tests/test_new_feature.py -v
```

---

## 6. Code Review Checklist

* ✅ AST node has unique base-12 ID.
* ✅ Parser recognizes syntax.
* ✅ IRGen lowering exists.
* ✅ NASM lowering exists (if needed).
* ✅ Example test case added.
* ✅ Documentation updated (`docs/cheatsheet.md`, `docs/guide.md`).

---

## 7. CI/CD Integration

* GitHub Actions will:

  * Run `pytest` on all OS (Ubuntu, Windows, macOS, Kali).
  * Build artifacts on tagged releases.
  * Publish to PyPI + draft GitHub Release.

---

## 8. Licensing & Attribution

All contributions fall under the **[S.U.E.T. License v1.0](../License.md)**.

Include attribution in docs/tests where appropriate:

```
“Original Work by Joey Soprano and ChatGPT, licensed under the S.U.E.T. License.”
```

---

## 9. Where to Start

* Good first issues:

  * Add new CIAM macros (arena, pool, slice, page).
  * Expand error handling with `retry` semantics.
  * Improve NASM backend coverage.
* Advanced:

  * WASM backend.
  * Package manager (`npkg`).
  * NP-VM interpreter.

---

## 10. Getting Help

* Open issues on GitHub:
  👉 [NeoPaquet Issues](https://github.com/JoeySoprano420/NeoPaquet/issues)
* Join discussions:
  👉 [NeoPaquet Discussions](https://github.com/JoeySoprano420/NeoPaquet/discussions)

---

```

---

## ✅ What This Adds
- **Step-by-step contributor tutorial** for new keywords, operators, and macros.  
- **Hands-on examples** for lexer → parser → AST → IRGen → NASM.  
- **Testing + CI/CD integration** notes.  
- **Checklists & contributor workflow** so nothing gets missed.  

---

⚡
