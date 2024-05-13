from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
}

setup(
    name="Descryption",
    version="0.1.0-alpha",
    description="An MS-DOS inspired demake of Inscryption",
    options={"build_exe": build_exe_options},
    executables=[Executable("duel.py", base="console")],
)