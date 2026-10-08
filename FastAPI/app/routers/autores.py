from fastapi import APIRouter, HTTPException, status
from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from app.core.database import SessionDep
from app.models import Autor, Livro
from app.schemas import (
    AutorCreate,
    AutorResponse,
    AutorUpdate,
    LivroResponse,
)

router = APIRouter(prefix="/autores", tags=["Autores"])


def buscar_autor(db: Session, autor_id: int) -> Autor:
    autor = db.get(Autor, autor_id)
    if autor is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Autor não encontrado")
    return autor


@router.post("", response_model=AutorResponse, status_code=status.HTTP_201_CREATED)
def criar_autor(dados: AutorCreate, db: SessionDep):
    autor = Autor(**dados.model_dump())
    db.add(autor)
    db.commit()
    return autor


@router.get("", response_model=list[AutorResponse])
def listar_autores(db: SessionDep, skip: int = 0, limit: int = 100):
    consulta = select(Autor).order_by(Autor.id).offset(skip).limit(limit)
    return db.scalars(consulta)


@router.get("/{autor_id}", response_model=AutorResponse)
def obter_autor(autor_id: int, db: SessionDep):
    return buscar_autor(db, autor_id)


@router.get("/{autor_id}/livros", response_model=list[LivroResponse])
def listar_livros_do_autor(autor_id: int, db: SessionDep):
    buscar_autor(db, autor_id)
    consulta = select(Livro).where(Livro.autor_id == autor_id).order_by(Livro.id)
    return db.scalars(consulta)


@router.patch("/{autor_id}", response_model=AutorResponse)
def atualizar_autor(autor_id: int, dados: AutorUpdate, db: SessionDep):
    autor = buscar_autor(db, autor_id)
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(autor, campo, valor)
    db.commit()
    return autor


@router.delete("/{autor_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_autor(autor_id: int, db: SessionDep):
    autor = buscar_autor(db, autor_id)
    possui_livros = db.scalar(select(exists().where(Livro.autor_id == autor_id)))

    if possui_livros:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Não é possível remover um autor que possui livros cadastrados",
        )
    db.delete(autor)
    db.commit()
