from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers import autores, livros

app = FastAPI(title="API da Biblioteca", version="1.0.0")

STATIC_DIR = Path(__file__).parent / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def interface():
    return FileResponse(STATIC_DIR / "index.html")

app.include_router(autores.router)
app.include_router(livros.router)
