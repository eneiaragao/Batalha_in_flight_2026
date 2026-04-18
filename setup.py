import sys
import os
from cx_Freeze import setup, Executable

# Garante que as pastas asset e code sejam incluídas
files = ["asset/", "code/"]

build_exe_options = {
    "packages": ["os", "pygame", "sqlite3"],
    "include_files": files,
}

setup(
    name = "Battle In Flight 2026",
    version = "1.0",
    description = "Battle In Flight 2026",
    options = {"build_exe": build_exe_options},
    executables = [Executable("Main.py", base=None)] # Deixe None para testar
)