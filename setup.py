import sys
from cx_Freeze import setup, Executable

# Dependências
build_exe_options = {
    "packages": ["tkinter", "babel.numbers"],  # Adicione quaisquer outros pacotes necessários aqui
}

# Configuração do executável
executables = [
    Executable("gui.py", base="Win32GUI", icon='grupo_toctao_logo.ico')
]

# Configuração do setup
setup(
    name="Gerador de Relatorios",
    version="1.0",
    description="Aplicativo para gerar relatorio de obras",
    options={"build_exe": build_exe_options},
    executables=executables
)
