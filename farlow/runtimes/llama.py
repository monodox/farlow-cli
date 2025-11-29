from pathlib import Path
from typing import Generator
try:
    from llama_cpp import Llama
except ImportError:
    Llama = None

from .base import BaseRuntime

class LlamaCppRuntime(BaseRuntime):
    def __init__(self):
        self.llm = None

    def load_model(self, model_path: Path, **kwargs):
        if Llama is None:
            raise ImportError("llama-cpp-python is not installed. Please install it to use this runtime.")
        
        print(f"LlamaCppRuntime: Loading model from {model_path}...")
        # Assuming model_path points to a GGUF file
        # If it points to a directory, we might need to find the .gguf file
        if model_path.is_dir():
            files = list(model_path.glob("*.gguf"))
            if not files:
                raise FileNotFoundError(f"No .gguf files found in {model_path}")
            model_file = str(files[0])
        else:
            model_file = str(model_path)

        self.llm = Llama(model_path=model_file, verbose=False, **kwargs)
        print("LlamaCppRuntime: Model loaded.")

    def generate(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        if not self.llm:
            raise RuntimeError("Model not loaded.")
        
        stream = self.llm(
            prompt,
            max_tokens=kwargs.get("max_tokens", 128),
            stop=kwargs.get("stop", ["User:", "\n"]),
            stream=True,
            echo=False
        )
        
        for output in stream:
            yield output["choices"][0]["text"]

    def unload(self):
        if self.llm:
            del self.llm
            self.llm = None
        print("LlamaCppRuntime: Unloaded.")
