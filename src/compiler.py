#!/usr/bin/env python3
"""
NeoPaquet Language Compiler

Main entry point for the NeoPaquet programming language compiler.
Integrates lexing, parsing, and error checking.
"""

import sys
import argparse
from pathlib import Path
from typing import List, Optional

from lexer import lex_source, LexerError
from parser import parse_source, ParseError
from error_checker import check_errors, SemanticError, ErrorType

class CompilerError(Exception):
    pass

class NeoPaquetCompiler:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def compile_file(self, filename: str, check_only: bool = False) -> bool:
        """
        Compile a NeoPaquet source file.
        
        Args:
            filename: Path to the source file
            check_only: If True, only perform error checking without code generation
        
        Returns:
            True if compilation succeeded, False otherwise
        """
        try:
            # Read source file
            source_path = Path(filename)
            if not source_path.exists():
                self.errors.append(f"Source file not found: {filename}")
                return False
            
            with open(source_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            return self.compile_source(source_code, str(source_path), check_only)
            
        except IOError as e:
            self.errors.append(f"IO error reading {filename}: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Unexpected error compiling {filename}: {e}")
            return False
    
    def compile_source(self, source: str, filename: str = "<source>", check_only: bool = False) -> bool:
        """
        Compile NeoPaquet source code.
        
        Args:
            source: Source code string
            filename: Name of the source file (for error reporting)
            check_only: If True, only perform error checking without code generation
        
        Returns:
            True if compilation succeeded, False otherwise
        """
        self.errors.clear()
        self.warnings.clear()
        
        try:
            # Phase 1: Lexical Analysis
            print(f"Phase 1: Lexing {filename}...")
            tokens = lex_source(source)
            print(f"Generated {len(tokens)} tokens")
            
            # Phase 2: Parsing
            print(f"Phase 2: Parsing {filename}...")
            program = parse_source(source)
            print(f"Parsed {len(program.statements)} top-level statements")
            
            # Phase 3: Semantic Analysis
            print(f"Phase 3: Semantic analysis...")
            semantic_errors = check_errors(program)
            
            # Categorize errors and warnings
            error_count = 0
            warning_count = 0
            
            for error in semantic_errors:
                if error.type in [ErrorType.SEMANTIC_ERROR] and "unused" in error.message.lower():
                    self.warnings.append(f"Warning: {error.message}")
                    warning_count += 1
                else:
                    self.errors.append(f"Error: {error.message}")
                    error_count += 1
            
            # Report results
            if error_count > 0:
                print(f"Compilation failed with {error_count} errors")
                if warning_count > 0:
                    print(f"Also found {warning_count} warnings")
                return False
            
            if warning_count > 0:
                print(f"Compilation succeeded with {warning_count} warnings")
            else:
                print("Compilation succeeded with no errors or warnings")
            
            # Phase 4: Code Generation (if not check-only)
            if not check_only:
                print("Phase 4: Code generation (not implemented yet)")
                # TODO: Implement code generation
            
            return True
            
        except LexerError as e:
            self.errors.append(f"Lexer error: {e}")
            return False
        except ParseError as e:
            self.errors.append(f"Parser error: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Unexpected error: {e}")
            return False
    
    def check_file(self, filename: str) -> bool:
        """Check a file for errors without compiling."""
        return self.compile_file(filename, check_only=True)
    
    def get_errors(self) -> List[str]:
        """Get all compilation errors."""
        return self.errors.copy()
    
    def get_warnings(self) -> List[str]:
        """Get all compilation warnings."""
        return self.warnings.copy()
    
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0

def auto_fix_common_errors(source: str) -> str:
    """
    Attempt to automatically fix common errors in NeoPaquet source code.
    
    This is a simple implementation that fixes basic issues.
    In a real compiler, this would be much more sophisticated.
    """
    lines = source.split('\n')
    fixed_lines = []
    
    for line_num, line in enumerate(lines, 1):
        original_line = line
        
        # Fix missing semicolons (simplified heuristic)
        stripped = line.strip()
        if (stripped and 
            not stripped.endswith(('{', '}', ';')) and 
            not stripped.startswith(('if', 'while', 'for', 'fn', 'struct', 'package', '//', 'let')) and
            not any(keyword in stripped for keyword in ['import', 'return', 'else'])):
            line = line.rstrip() + ';'
        
        # Fix common type annotation issues
        if 'let' in line and '=' in line and ':' not in line:
            # Simple heuristic to add type annotations where missing
            if '"' in line:  # String literal
                line = line.replace('let ', 'let ').replace(' =', ': String =', 1)
            elif any(c.isdigit() for c in line) and '.' in line:  # Float literal
                line = line.replace(' =', ': f64 =', 1)
            elif any(c.isdigit() for c in line):  # Integer literal
                line = line.replace(' =', ': i32 =', 1)
            elif 'true' in line or 'false' in line:  # Boolean literal
                line = line.replace(' =', ': bool =', 1)
        
        if line != original_line:
            print(f"Auto-fix line {line_num}: {original_line.strip()} -> {line.strip()}")
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def main():
    parser = argparse.ArgumentParser(
        description="NeoPaquet Programming Language Compiler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s compile main.np              # Compile main.np
  %(prog)s check main.np                # Check main.np for errors
  %(prog)s auto-fix main.np             # Attempt to auto-fix errors
  %(prog)s --version                    # Show version information
        """
    )
    
    parser.add_argument('command', choices=['compile', 'check', 'auto-fix', 'version'], 
                       help='Command to execute')
    parser.add_argument('file', nargs='?', help='Source file to process')
    parser.add_argument('--output', '-o', help='Output file (for compile command)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--version', action='version', version='NeoPaquet Compiler 0.1.0')
    
    args = parser.parse_args()
    
    if args.command == 'version':
        print("NeoPaquet Programming Language Compiler")
        print("Version 0.1.0")
        print("Copyright (c) 2024 NeoPaquet Development Team")
        return 0
    
    if not args.file:
        print("Error: Source file required for this command")
        return 1
    
    compiler = NeoPaquetCompiler()
    
    if args.command == 'compile':
        success = compiler.compile_file(args.file)
        if not success:
            print("\nErrors:")
            for error in compiler.get_errors():
                print(f"  {error}")
            return 1
        
        if compiler.get_warnings():
            print("\nWarnings:")
            for warning in compiler.get_warnings():
                print(f"  {warning}")
        
        return 0
    
    elif args.command == 'check':
        success = compiler.check_file(args.file)
        if not success:
            print("Code check failed:")
            for error in compiler.get_errors():
                print(f"  {error}")
            return 1
        
        if compiler.get_warnings():
            print("Warnings:")
            for warning in compiler.get_warnings():
                print(f"  {warning}")
        
        print("Code check passed!")
        return 0
    
    elif args.command == 'auto-fix':
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                source = f.read()
            
            print(f"Attempting to auto-fix {args.file}...")
            fixed_source = auto_fix_common_errors(source)
            
            # Check if fixes were applied
            if fixed_source != source:
                # Write fixed version to a new file
                output_file = args.output or (args.file + '.fixed')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_source)
                print(f"Fixed version written to {output_file}")
                
                # Check the fixed version
                success = compiler.compile_source(fixed_source, output_file, check_only=True)
                if success:
                    print("Auto-fix successful! Fixed version compiles without errors.")
                else:
                    print("Auto-fix partially successful, but some errors remain:")
                    for error in compiler.get_errors():
                        print(f"  {error}")
            else:
                print("No common errors found that could be auto-fixed.")
            
            return 0
            
        except IOError as e:
            print(f"Error reading {args.file}: {e}")
            return 1
    
    return 1

if __name__ == "__main__":
    sys.exit(main())