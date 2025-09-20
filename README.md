# NeoPaquet

A modern, package-centric programming language designed for simplicity, performance, and seamless dependency management.

## Overview

NeoPaquet is a statically-typed, compiled programming language that treats packages as first-class citizens. It combines the best features of modern languages with innovative package management directly built into the language syntax and runtime.

## Language Features

### Core Syntax
- Clean, readable syntax inspired by Python and Rust
- Strong static typing with type inference
- Memory safety without garbage collection
- Pattern matching and algebraic data types
- First-class functions and closures

### Package System
- Built-in package management (no external tools needed)
- Semantic versioning enforced at the language level
- Dependency resolution integrated into the compiler
- Package isolation and sandboxing

### Performance
- Ahead-of-time compilation to native code
- Zero-cost abstractions
- Minimal runtime overhead
- Optimized for modern multi-core systems

## Basic Syntax Examples

```neopaquet
// Variable declarations with type inference
let name = "NeoPaquet"
let version: Version = "1.0.0"

// Functions
fn greet(name: String) -> String {
    return "Hello, " + name + "!"
}

// Package imports with version constraints
import http from "std/http" version ">=2.0.0"
import json from "community/json-parser" version "~1.5.0"

// Data structures
struct User {
    name: String,
    email: String,
    age: u32
}

// Pattern matching
match response {
    Ok(data) => process_data(data),
    Err(error) => log_error(error)
}
```

## Package Management

```neopaquet
// Package declaration
package web-server version "0.1.0" {
    dependencies {
        "std/http" version ">=2.0.0",
        "community/database" version "^3.1.0"
    }
    
    exports {
        Server,
        start_server
    }
}
```

## Installation & Usage

```bash
# Install NeoPaquet compiler
curl -sSf https://neo.paquet.dev/install.sh | sh

# Create new package
neo new my-project
cd my-project

# Run program
neo run

# Build for production
neo build --release
```

## Project Structure

```
src/           # Source code
├── main.np    # Main entry point
├── lib.np     # Library code
└── mod/       # Modules
tests/         # Test files
paquet.toml    # Package configuration
```

## Development Status

NeoPaquet is currently in early development. The following components are being implemented:

1. **Lexer & Parser** - Tokenization and syntax analysis
2. **Type System** - Static type checking and inference
3. **Compiler** - Code generation and optimization
4. **Runtime** - Minimal runtime for memory management
5. **Package Manager** - Dependency resolution and management
6. **Standard Library** - Core functionality and APIs

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

NeoPaquet is released under the MIT License. See [LICENSE](LICENSE) for details.