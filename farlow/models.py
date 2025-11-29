from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel

class Model(BaseModel):
    name: str
    path: Path
    runtime: str

class ModelRegistry:
    def __init__(self, models_dir: Path):
        self.models_dir = models_dir

    def list_models(self) -> List[Model]:
        models = []
        if not self.models_dir.exists():
            return models
        
        # Scan for model directories
        for path in self.models_dir.iterdir():
            if path.is_dir():
                # Check for a metadata file or just assume it's a model
                # For now, we'll assume directory name is model name
                # and default runtime is llama.cpp
                models.append(Model(name=path.name, path=path, runtime="llama.cpp"))
        return models

    def register_model(self, name: str, path: Path, runtime: str):
        # In a real implementation, we might move files or create symlinks
        # For now, we'll just ensure the directory exists
        target_dir = self.models_dir / name
        target_dir.mkdir(parents=True, exist_ok=True)
        # TODO: Copy/Move files logic
        pass
