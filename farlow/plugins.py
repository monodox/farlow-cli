import importlib.util
import sys
from pathlib import Path
from .config import get_config

def load_plugins():
    config = get_config()
    plugins_dir = config.models_dir.parent / "plugins"
    
    if not plugins_dir.exists():
        return

    print(f"Loading plugins from {plugins_dir}...")
    for plugin_file in plugins_dir.glob("*.py"):
        if plugin_file.name == "__init__.py":
            continue
            
        try:
            spec = importlib.util.spec_from_file_location(plugin_file.stem, plugin_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[plugin_file.stem] = module
                spec.loader.exec_module(module)
                print(f"Loaded plugin: {plugin_file.name}")
        except Exception as e:
            print(f"Failed to load plugin {plugin_file.name}: {e}")
