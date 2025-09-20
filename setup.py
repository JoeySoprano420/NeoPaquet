from setuptools import setup, find_packages

setup(
    name="npaquetc",
    version="1.0.0",
    description="NeoPaquet Compiler (AOT → LLVM IR → NASM → Native Executable)",
    author="NeoPaquet Project",
    license="S.U.E.T.",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "npaquetc=npaquetc.main:main",
        ],
    },
    python_requires=">=3.9",
    install_requires=[
        "llvmlite>=0.42.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Compilers",
        "License :: OSI Approved :: S.U.E.T. License",
    ],
)
