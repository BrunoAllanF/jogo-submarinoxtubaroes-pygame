import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "gui"

opcoes = {
    "build_exe": {
        "packages": ["pygame"],
        "include_files": ["images/", "fontes/"]
        }
    }

setup(
    name="Submarino vs Tubaroes",
    version="1.0",
    description="Demo do Jogo - Trabalho Prático LPA",
    options=opcoes,
    executables=[Executable("main.py", base=base)]
    
    )