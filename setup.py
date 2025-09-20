#!/usr/bin/env python3
"""
NeoPaquet setup and build script
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is suitable."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required Python dependencies."""
    print("Installing dependencies...")
    
    # For now, NeoPaquet has minimal dependencies
    # In the future, this might install packages like:
    # - llvmlite (for code generation)
    # - watchdog (for file watching)
    # - requests (for package management)
    
    try:
        # Check if watchdog is available for dev tools
        subprocess.run([sys.executable, "-c", "import watchdog"], 
                      check=True, capture_output=True)
        print("✓ watchdog available for development tools")
    except subprocess.CalledProcessError:
        print("ℹ watchdog not available - file watching disabled")
        print("  Install with: pip install watchdog")
    
    return True

def run_tests():
    """Run the test suite."""
    print("Running tests...")
    test_path = Path("tests/test_compiler.py")
    
    if not test_path.exists():
        print("✗ Test file not found")
        return False
    
    try:
        result = subprocess.run([sys.executable, str(test_path)], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ All tests passed")
            return True
        else:
            print("✗ Some tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    
    except Exception as e:
        print(f"✗ Error running tests: {e}")
        return False

def create_executable_script():
    """Create executable script for the compiler."""
    script_content = '''#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_dir))

from compiler import main

if __name__ == "__main__":
    main()
'''
    
    script_path = Path("neo")
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # Make executable on Unix systems
    if os.name != 'nt':
        os.chmod(script_path, 0o755)
    
    print(f"✓ Created executable script: {script_path}")
    return True

def build_distribution():
    """Build distribution package."""
    print("Building distribution...")
    
    dist_dir = Path("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    dist_dir.mkdir()
    
    # Copy source files
    src_dist = dist_dir / "neopaquet"
    src_dist.mkdir()
    
    src_files = Path("src").glob("*.py")
    for src_file in src_files:
        shutil.copy2(src_file, src_dist)
    
    # Copy configuration and documentation
    for file in ["README.md", "paquet.toml"]:
        if Path(file).exists():
            shutil.copy2(file, dist_dir)
    
    # Copy examples
    examples_src = Path("examples")
    if examples_src.exists():
        examples_dist = dist_dir / "examples"
        shutil.copytree(examples_src, examples_dist)
    
    print(f"✓ Distribution built in {dist_dir}")
    return True

def main():
    """Main setup function."""
    print("NeoPaquet Setup and Build Script")
    print("=" * 40)
    
    if len(sys.argv) < 2:
        print("Usage: python setup.py <command>")
        print()
        print("Commands:")
        print("  install    - Install dependencies and set up development environment")
        print("  test       - Run the test suite")
        print("  build      - Build distribution package")
        print("  clean      - Clean build artifacts")
        print("  dev        - Set up for development (install + create executable)")
        return 1
    
    command = sys.argv[1]
    
    if not check_python_version():
        return 1
    
    if command == "install":
        if install_dependencies():
            print("\n✓ Installation complete!")
            return 0
        else:
            print("\n✗ Installation failed")
            return 1
    
    elif command == "test":
        if run_tests():
            return 0
        else:
            return 1
    
    elif command == "build":
        if build_distribution():
            print("\n✓ Build complete!")
            return 0
        else:
            print("\n✗ Build failed")
            return 1
    
    elif command == "clean":
        print("Cleaning build artifacts...")
        
        # Remove build directories
        for dir_name in ["dist", "__pycache__", "build", ".pytest_cache"]:
            for path in Path(".").rglob(dir_name):
                if path.is_dir():
                    shutil.rmtree(path)
                    print(f"  Removed {path}")
        
        # Remove compiled Python files
        for pyc_file in Path(".").rglob("*.pyc"):
            pyc_file.unlink()
            print(f"  Removed {pyc_file}")
        
        # Remove executable script
        if Path("neo").exists():
            Path("neo").unlink()
            print("  Removed neo executable")
        
        print("✓ Clean complete!")
        return 0
    
    elif command == "dev":
        print("Setting up development environment...")
        
        if not install_dependencies():
            return 1
        
        if not create_executable_script():
            return 1
        
        if not run_tests():
            print("⚠ Tests failed, but development setup continues")
        
        print("\n✓ Development setup complete!")
        print("\nYou can now use:")
        print("  ./neo compile examples/simple.np")
        print("  ./neo check examples/simple.np")
        print("  python src/dev_tools.py watch")
        return 0
    
    else:
        print(f"Unknown command: {command}")
        return 1

if __name__ == "__main__":
    sys.exit(main())