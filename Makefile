# NeoPaquet Makefile

.PHONY: install test build clean dev watch format help

# Default target
help:
	@echo "NeoPaquet Build System"
	@echo "======================"
	@echo ""
	@echo "Available targets:"
	@echo "  install    - Install dependencies and set up environment"
	@echo "  test       - Run test suite"
	@echo "  build      - Build distribution package"
	@echo "  clean      - Clean build artifacts"
	@echo "  dev        - Set up development environment"
	@echo "  watch      - Start development server with file watching"
	@echo "  format     - Format all NeoPaquet source files"
	@echo "  check      - Check all example files for errors"
	@echo "  help       - Show this help message"

install:
	python3 setup.py install

test:
	python3 setup.py test

build:
	python3 setup.py build

clean:
	python3 setup.py clean

dev:
	python3 setup.py dev

watch:
	python3 src/dev_tools.py watch

format:
	@echo "Formatting NeoPaquet files..."
	@find examples -name "*.np" -exec python3 src/dev_tools.py format {} \;
	@echo "Formatting complete!"

check:
	@echo "Checking all example files..."
	@for file in examples/*.np; do \
		if [ -f "$$file" ]; then \
			echo "Checking $$file..."; \
			python3 src/compiler.py check "$$file" || true; \
			echo ""; \
		fi; \
	done

# Development shortcuts
compile-simple:
	python3 src/compiler.py compile examples/simple.np

check-simple:
	python3 src/compiler.py check examples/simple.np

auto-fix-examples:
	@echo "Auto-fixing example files..."
	@for file in examples/*.np; do \
		if [ -f "$$file" ]; then \
			echo "Auto-fixing $$file..."; \
			python3 src/compiler.py auto-fix "$$file"; \
		fi; \
	done