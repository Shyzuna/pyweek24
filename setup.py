from cx_Freeze import setup, Executable

buildOptions = dict(include_files = ['data/'])

setup(
    name = "Beyond the game",
    version = "0.0.1",
    description = '',
    options = dict(build_exe = buildOptions),
    executables = [Executable("main.py")]
)