from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generator

class BaseRuntime(ABC):
    @abstractmethod
    def load_model(self, model_path: Path, **kwargs):
        """Load the model into memory."""
        pass

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """Generate text from the model."""
        pass

    @abstractmethod
    def unload(self):
        """Unload the model to free resources."""
        pass
