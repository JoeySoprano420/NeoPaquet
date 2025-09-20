#!/usr/bin/env python3
"""
NeoPaquet Language Server and Development Tools

This module provides development tools including:
- Language server protocol support
- Real-time error checking
- Auto-completion
- Code formatting
"""

import threading
import time
from pathlib import Path
from typing import List, Dict, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from compiler import NeoPaquetCompiler

class NeoPaquetFileWatcher(FileSystemEventHandler):
    """Watches NeoPaquet files for changes and automatically checks them for errors."""
    
    def __init__(self, compiler: NeoPaquetCompiler):
        self.compiler = compiler
        self.last_check = {}
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        if file_path.suffix == '.np':
            # Debounce: only check if file hasn't been checked recently
            current_time = time.time()
            if file_path in self.last_check:
                if current_time - self.last_check[file_path] < 1.0:  # 1 second debounce
                    return
            
            self.last_check[file_path] = current_time
            print(f"\nFile changed: {file_path}")
            self.check_file(str(file_path))
    
    def check_file(self, file_path: str):
        """Check a single file for errors."""
        success = self.compiler.check_file(file_path)
        
        if success:
            if self.compiler.get_warnings():
                print(f"✓ {file_path} - OK with warnings:")
                for warning in self.compiler.get_warnings():
                    print(f"  {warning}")
            else:
                print(f"✓ {file_path} - OK")
        else:
            print(f"✗ {file_path} - ERRORS:")
            for error in self.compiler.get_errors():
                print(f"  {error}")

class DevServer:
    """Development server that provides real-time error checking."""
    
    def __init__(self, watch_dirs: List[str] = None):
        self.watch_dirs = watch_dirs or ['.']
        self.compiler = NeoPaquetCompiler()
        self.observer = Observer()
        self.running = False
    
    def start(self):
        """Start the development server."""
        print("NeoPaquet Development Server Starting...")
        print("Watching directories:", ', '.join(self.watch_dirs))
        print("Watching for .np files...")
        
        # Set up file watchers
        event_handler = NeoPaquetFileWatcher(self.compiler)
        
        for watch_dir in self.watch_dirs:
            if Path(watch_dir).exists():
                self.observer.schedule(event_handler, watch_dir, recursive=True)
                print(f"Watching: {watch_dir}")
        
        self.observer.start()
        self.running = True
        
        # Initial check of all .np files
        self.initial_check()
        
        print("\nDevelopment server is running. Press Ctrl+C to stop.")
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the development server."""
        print("\nStopping development server...")
        self.observer.stop()
        self.observer.join()
        self.running = False
        print("Development server stopped.")
    
    def initial_check(self):
        """Perform initial check of all NeoPaquet files."""
        print("\nPerforming initial check of all .np files...")
        
        for watch_dir in self.watch_dirs:
            watch_path = Path(watch_dir)
            if watch_path.exists():
                for np_file in watch_path.rglob('*.np'):
                    print(f"\nChecking: {np_file}")
                    success = self.compiler.check_file(str(np_file))
                    
                    if success:
                        if self.compiler.get_warnings():
                            print(f"✓ OK with warnings")
                            for warning in self.compiler.get_warnings():
                                print(f"  {warning}")
                        else:
                            print(f"✓ OK")
                    else:
                        print(f"✗ ERRORS:")
                        for error in self.compiler.get_errors():
                            print(f"  {error}")
        
        print("\nInitial check complete.")

def format_neopaquet_code(source: str) -> str:
    """
    Format NeoPaquet source code with consistent style.
    This is a basic formatter - a real implementation would be more sophisticated.
    """
    lines = source.split('\n')
    formatted_lines = []
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        
        if not stripped or stripped.startswith('//'):
            formatted_lines.append(stripped)
            continue
        
        # Decrease indent for closing braces
        if stripped.startswith('}'):
            indent_level = max(0, indent_level - 1)
        
        # Add proper indentation
        formatted_line = '    ' * indent_level + stripped
        formatted_lines.append(formatted_line)
        
        # Increase indent for opening braces
        if stripped.endswith('{'):
            indent_level += 1
    
    return '\n'.join(formatted_lines)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="NeoPaquet Development Tools")
    parser.add_argument('command', choices=['watch', 'format'], help='Command to run')
    parser.add_argument('--dir', action='append', help='Directory to watch (can be used multiple times)')
    parser.add_argument('file', nargs='?', help='File to format (for format command)')
    
    args = parser.parse_args()
    
    if args.command == 'watch':
        watch_dirs = args.dir or ['.']
        server = DevServer(watch_dirs)
        
        try:
            server.start()
        except ImportError:
            print("Error: watchdog package required for file watching")
            print("Install with: pip install watchdog")
    
    elif args.command == 'format':
        if not args.file:
            print("Error: file argument required for format command")
            exit(1)
        
        try:
            with open(args.file, 'r') as f:
                source = f.read()
            
            formatted = format_neopaquet_code(source)
            
            with open(args.file, 'w') as f:
                f.write(formatted)
            
            print(f"Formatted {args.file}")
        
        except IOError as e:
            print(f"Error: {e}")
            exit(1)