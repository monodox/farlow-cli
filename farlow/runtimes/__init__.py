from .mock import MockRuntime
from .llama import LlamaCppRuntime
from .transformers import TransformersRuntime

def get_runtime(name: str):
    if name == "mock":
        return MockRuntime()
    elif name == "llama.cpp":
        return LlamaCppRuntime()
    elif name == "transformers":
        return TransformersRuntime()
    
    # Default fallback or error
    raise ValueError(f"Unknown runtime: {name}")