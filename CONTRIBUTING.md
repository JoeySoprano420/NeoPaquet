# Contributing to NeoPaquet

Thank you for your interest in contributing to NeoPaquet! This document provides guidelines for contributing to the project.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/JoeySoprano420/NeoPaquet.git
   cd NeoPaquet
   ```

2. Set up the development environment:
   ```bash
   python setup.py dev
   ```
   
   Or using make:
   ```bash
   make dev
   ```

3. Test the installation:
   ```bash
   ./neo check examples/simple.np
   ```

## Project Structure

```
NeoPaquet/
├── src/                    # Compiler source code
│   ├── lexer.py           # Lexical analysis
│   ├── parser.py          # Syntax analysis
│   ├── error_checker.py   # Semantic analysis
│   ├── compiler.py        # Main compiler driver
│   └── dev_tools.py       # Development tools
├── tests/                 # Test suite
├── examples/              # Example NeoPaquet programs
├── docs/                  # Documentation
├── .github/workflows/     # CI/CD workflows
└── paquet.toml           # Package configuration
```

## Development Workflow

1. **Make Changes**: Edit the appropriate source files
2. **Test Changes**: Run the test suite
   ```bash
   make test
   ```
3. **Check Examples**: Verify examples still work
   ```bash
   make check
   ```
4. **Format Code**: Format Python code consistently
   ```bash
   black src/ tests/
   ```
5. **Submit PR**: Create a pull request with your changes

## Adding New Features

### Adding New Language Features

1. **Update Lexer** (`src/lexer.py`):
   - Add new token types to `TokenType` enum
   - Add keyword mappings if needed
   - Update tokenization logic

2. **Update Parser** (`src/parser.py`):
   - Add new AST node types
   - Add parsing methods for new syntax
   - Update grammar rules

3. **Update Error Checker** (`src/error_checker.py`):
   - Add semantic validation for new features
   - Add appropriate error messages
   - Update type checking logic

4. **Add Tests**:
   - Add unit tests for new functionality
   - Add integration tests with example code
   - Update test suite

5. **Update Documentation**:
   - Update README with new syntax examples
   - Add documentation for new features

### Example: Adding a New Operator

```python
# 1. In lexer.py - Add token type
class TokenType(Enum):
    # ... existing tokens ...
    POWER = auto()  # For ** operator

# 2. In lexer.py - Add tokenization
if char == '*' and self.peek_char() == '*':
    self.advance()
    self.advance()
    self.tokens.append(Token(TokenType.POWER, '**', start_line, start_column))

# 3. In parser.py - Add to expression parsing
def parse_power(self) -> Expression:
    expr = self.parse_unary()
    
    while self.match_token(TokenType.POWER):
        operator = self.current_token().value
        self.advance()
        right = self.parse_unary()
        expr = BinaryOp(expr, operator, right)
    
    return expr

# 4. In error_checker.py - Add type checking
elif expr.operator == '**':
    if left_type == right_type and left_type in ['i32', 'u32', 'f32', 'f64']:
        return left_type
    else:
        self.add_error(ErrorType.TYPE_ERROR, 
                     f"Power operator requires numeric types, got '{left_type}' and '{right_type}'", expr)
```

## Testing Guidelines

- All new features must include tests
- Tests should cover both success and error cases
- Use descriptive test names and docstrings
- Run the full test suite before submitting PRs

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
python tests/test_compiler.py

# Check examples
make check
```

## Code Style

- Use Black for Python code formatting
- Use descriptive variable and function names
- Add docstrings to public functions and classes
- Keep functions focused and reasonably sized
- Use type hints where appropriate

### Formatting

```bash
# Format Python code
black src/ tests/

# Check formatting
black --check src/ tests/

# Sort imports
isort src/ tests/
```

## Error Handling

- Use specific error types and clear error messages
- Include location information (line/column) when possible
- Provide suggestions for fixing errors where applicable
- Test error conditions thoroughly

## Performance Considerations

- The compiler should be fast for small to medium programs
- Memory usage should be reasonable
- Consider algorithmic complexity for core operations
- Profile performance-critical code paths

## Documentation

- Keep README up to date with new features
- Add inline code examples for new syntax
- Document public APIs with docstrings
- Update CONTRIBUTING.md for development process changes

## Submitting Changes

1. **Fork the Repository**: Create your own fork on GitHub
2. **Create Feature Branch**: `git checkout -b feature/my-new-feature`
3. **Make Changes**: Implement your feature with tests
4. **Test Thoroughly**: Run all tests and check examples
5. **Format Code**: Ensure consistent formatting
6. **Commit Changes**: Use descriptive commit messages
7. **Push Branch**: Push to your fork
8. **Create PR**: Submit pull request with description

### PR Requirements

- [ ] All tests pass
- [ ] Code is properly formatted
- [ ] New features include tests
- [ ] Documentation is updated
- [ ] Examples work correctly
- [ ] No breaking changes (unless discussed)

## Getting Help

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Ask questions in discussions
- Review the codebase to understand patterns

## Code of Conduct

Be respectful and constructive in all interactions. We welcome contributions from everyone regardless of experience level.

Thank you for contributing to NeoPaquet!