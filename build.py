import PyInstaller.__main__
import platform
import os
from pathlib import Path

def build():
    system = platform.system().lower()
    dist_path = Path("dist") / system
    
    print(f"Building for {system}...")
    
    PyInstaller.__main__.run([
        'farlow/cli.py',
        '--name=farlow',
        '--onefile',
        f'--distpath={str(dist_path)}',
        '--clean',
        # Add hidden imports that might be missed
        '--hidden-import=typer',
        '--hidden-import=rich',
        '--hidden-import=pydantic',
        '--hidden-import=farlow.runtimes.mock',
        '--hidden-import=farlow.runtimes.llama',
        '--hidden-import=farlow.runtimes.transformers',
        '--hidden-import=farlow.plugins',
    ])
    
    print(f"Build complete. Executable is in {dist_path}")

if __name__ == "__main__":
    build()
