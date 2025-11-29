from pathlib import Path
from typing import Generator
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
    import torch
    from threading import Thread
except ImportError:
    AutoModelForCausalLM = None

from .base import BaseRuntime

class TransformersRuntime(BaseRuntime):
    def __init__(self):
        self.model = None
        self.tokenizer = None

    def load_model(self, model_path: Path, **kwargs):
        if AutoModelForCausalLM is None:
            raise ImportError("transformers/torch is not installed. Please install them to use this runtime.")
        
        print(f"TransformersRuntime: Loading model from {model_path}...")
        # model_path should be a directory containing the model files
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path, 
            device_map="auto", 
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        print("TransformersRuntime: Model loaded.")

    def generate(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        if not self.model or not self.tokenizer:
            raise RuntimeError("Model not loaded.")

        inputs = self.tokenizer([prompt], return_tensors="pt").to(self.model.device)
        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)
        generation_kwargs = dict(inputs, streamer=streamer, max_new_tokens=kwargs.get("max_new_tokens", 128))
        
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()
        
        for new_text in streamer:
            yield new_text

    def unload(self):
        if self.model:
            del self.model
            del self.tokenizer
            self.model = None
            self.tokenizer = None
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        print("TransformersRuntime: Unloaded.")
