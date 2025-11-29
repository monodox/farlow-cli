from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .runtimes import get_runtime
from .config import get_config
from .models import ModelRegistry

app = FastAPI(title="Farlow Model Server")

class GenerateRequest(BaseModel):
    model: str
    prompt: str
    max_tokens: int = 128

@app.post("/v1/completions")
async def generate(request: GenerateRequest):
    config = get_config()
    registry = ModelRegistry(config.models_dir)
    
    # Find model
    models = registry.list_models()
    model = next((m for m in models if m.name == request.model), None)
    
    if not model:
        raise HTTPException(status_code=404, detail=f"Model {request.model} not found")

    # Initialize runtime (Note: In a real server, we'd keep this loaded)
    try:
        runtime = get_runtime(model.runtime)
        runtime.load_model(model.path)
        
        response_text = ""
        for chunk in runtime.generate(request.prompt, max_tokens=request.max_tokens):
            response_text += chunk
            
        runtime.unload()
        
        return {
            "id": "cmpl-123",
            "object": "text_completion",
            "created": 1234567890,
            "model": request.model,
            "choices": [
                {
                    "text": response_text,
                    "index": 0,
                    "logprobs": None,
                    "finish_reason": "length"
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/models")
async def list_models():
    config = get_config()
    registry = ModelRegistry(config.models_dir)
    models = registry.list_models()
    return {
        "object": "list",
        "data": [
            {
                "id": m.name,
                "object": "model",
                "owned_by": "user",
                "permission": []
            } for m in models
        ]
    }
