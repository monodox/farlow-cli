import os
from pathlib import Path
from pydantic import BaseModel

class Config(BaseModel):
    models_dir: Path = Path.home() / ".farlow" / "models"
    default_runtime: str = "llama.cpp"

    @classmethod
    def load(cls) -> "Config":
        config_path = Path.home() / ".farlow" / "config.json"
        if config_path.exists():
            with open(config_path, "r") as f:
                return cls.model_validate_json(f.read())
        return cls()

    def save(self):
        config_path = Path.home() / ".farlow" / "config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            f.write(self.model_dump_json(indent=4))

def get_config() -> Config:
    return Config.load()
