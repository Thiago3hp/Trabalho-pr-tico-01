from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionDep
from app.models import Autor, Livro
from app.schemas import LivroCreate, LivroResponse, LivroUpdate

router = APIRouter(prefix="/livros", tags=["Livros"])


def buscar_livro(db: Session, livro_id: int) -> Livro:
    livro = db.get(Livro, livro_id)
    if livro is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Livro não encontrado")
    return livro


def validar_autor(db: Session, autor_id: int) -> None:
    if db.get(Autor, autor_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Autor informado não existe")


@router.post("", response_model=LivroResponse, status_code=status.HTTP_201_CREATED)
def criar_livro(dados: LivroCreate, db: SessionDep):
    validar_autor(db, dados.autor_id)

    livro = Livro(**dados.model_dump())
    db.add(livro)
    db.commit()
    db.refresh(livro)
    return livro


@router.get("", response_model=list[LivroResponse])
def listar_livros(
    db: SessionDep,
    disponivel: bool | None = None,
    skip: int = 0,
    limit: int = 100,
):
    consulta = select(Livro).order_by(Livro.id).offset(skip).limit(limit)
    if disponivel is not None:
        consulta = consulta.where(Livro.disponivel == disponivel)
    return db.scalars(consulta)


@router.get("/{livro_id}", response_model=LivroResponse)
def obter_livro(livro_id: int, db: SessionDep):
    return buscar_livro(db, livro_id)


@router.patch("/{livro_id}", response_model=LivroResponse)
def atualizar_livro(livro_id: int, dados: LivroUpdate, db: SessionDep):
    livro = buscar_livro(db, livro_id)
    alteracoes = dados.model_dump(exclude_unset=True)

    if "autor_id" in alteracoes:
        validar_autor(db, alteracoes["autor_id"])

    for campo, valor in alteracoes.items():
        setattr(livro, campo, valor)
    db.commit()
    db.refresh(livro)
    return livro


@router.delete("/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_livro(livro_id: int, db: SessionDep):
    db.delete(buscar_livro(db, livro_id))
    db.commit()
