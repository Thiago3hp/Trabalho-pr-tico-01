from fastapi import FastAPI

from app.routers import autores, livros

app = FastAPI(title="API da Biblioteca", version="1.0.0")

app.include_router(autores.router)
app.include_router(livros.router)

