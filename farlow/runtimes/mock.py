from pathlib import Path
from typing import Generator
import time
from .base import BaseRuntime

class MockRuntime(BaseRuntime):
    def load_model(self, model_path: Path, **kwargs):
        print(f"MockRuntime: Loading model from {model_path}...")
        time.sleep(1) # Simulate loading
        print("MockRuntime: Model loaded.")

    def generate(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        print(f"MockRuntime: Generating response for prompt: '{prompt}'")
        response = f"This is a mock response to: {prompt}"
        for word in response.split():
            yield word + " "
            time.sleep(0.1) # Simulate generation

    def unload(self):
        print("MockRuntime: Unloading model.")
