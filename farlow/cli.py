import typer
from rich.console import Console

app = typer.Typer(
    name="farlow",
    help="Farlow: Open-source, CLI-first conversational AI platform",
    add_completion=False,
)
console = Console()

from .config import get_config

@app.callback()
def main():
    """
    Farlow CLI - Manage and run open-weight LLMs locally.
    """
    # Ensure config is loaded/created
    config = get_config()
    config.save() # Ensure directory exists

from .models import ModelRegistry

@app.command()
def version():
    """
    Show the current version of Farlow.
    """
    console.print("Farlow CLI v0.1.0")

@app.command()
def list():
    """
    List installed models.
    """
    config = get_config()
    registry = ModelRegistry(config.models_dir)
    models = registry.list_models()
    
    if not models:
        console.print("No models found.")
        return

    for model in models:
        console.print(f"- {model.name} ({model.runtime})")

@app.command()
def pull(model_name: str):
    """
    Download a model.
    """
    config = get_config()
    registry = ModelRegistry(config.models_dir)
    
    console.print(f"Pulling model: {model_name}...")
    # TODO: Implement actual download logic
    registry.register_model(model_name, config.models_dir / model_name, "mock")
    console.print(f"Successfully pulled {model_name}")

from .runtimes import get_runtime

@app.command()
def run(model_name: str, prompt: str):
    """
    Run a model with a prompt.
    """
    config = get_config()
    registry = ModelRegistry(config.models_dir)
    
    # Find model
    models = registry.list_models()
    model = next((m for m in models if m.name == model_name), None)
    
    if not model:
        console.print(f"[red]Model {model_name} not found. Run 'farlow pull {model_name}' first.[/red]")
        return

    # Initialize runtime
    runtime = get_runtime(model.runtime)
    runtime.load_model(model.path)
    
    try:
        console.print("[bold green]Farlow:[/bold green]", end=" ")
        for chunk in runtime.generate(prompt):
            console.print(chunk, end="")
        console.print() # Newline
    finally:
        runtime.unload()

@app.command()
def serve(host: str = "127.0.0.1", port: int = 8000):
    """
    Start the Farlow Model Server (OpenAI compatible-ish).
    """
    import uvicorn
    console.print(f"Starting server at http://{host}:{port}")
    uvicorn.run("farlow.server:app", host=host, port=port, reload=False)

if __name__ == "__main__":
    from .plugins import load_plugins
    load_plugins()
    app()
