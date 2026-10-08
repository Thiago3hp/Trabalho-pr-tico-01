from pydantic import BaseModel, ConfigDict, Field


class AutorCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    nacionalidade: str | None = Field(default=None, max_length=50)


class AutorUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=1, max_length=100)
    nacionalidade: str | None = Field(default=None, max_length=50)


class AutorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    nacionalidade: str | None
