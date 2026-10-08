from pydantic import BaseModel, ConfigDict, Field

from app.schemas.autor import AutorResponse


class LivroCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=150)
    ano_publicacao: int | None = Field(default=None, ge=0, le=2100)
    disponivel: bool = True
    autor_id: int


class LivroUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=150)
    ano_publicacao: int | None = Field(default=None, ge=0, le=2100)
    disponivel: bool | None = None
    autor_id: int | None = None


class LivroResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    ano_publicacao: int | None
    disponivel: bool
    autor_id: int
    autor: AutorResponse
