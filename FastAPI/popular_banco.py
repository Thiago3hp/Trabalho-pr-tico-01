"""Popula o banco com autores e livros de exemplo para demonstrar a API.

Uso (dentro da pasta FastAPI/, depois de `alembic upgrade head`):
    python popular_banco.py
"""

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models import Autor, Livro

ACERVO = {
    ("Machado de Assis", "Brasileira"): [
        ("Dom Casmurro", 1899, True),
        ("Memórias Póstumas de Brás Cubas", 1881, False),
    ],
    ("Clarice Lispector", "Brasileira"): [
        ("A Hora da Estrela", 1977, True),
    ],
    ("Graciliano Ramos", "Brasileira"): [
        ("Vidas Secas", 1938, True),
    ],
    ("George Orwell", "Britânica"): [
        ("1984", 1949, False),
        ("A Revolução dos Bichos", 1945, True),
    ],
}


def popular() -> None:
    with SessionLocal() as db:
        if db.scalar(select(Autor).limit(1)) is not None:
            print("O banco já possui autores cadastrados. Nada foi alterado.")
            return

        for (nome, nacionalidade), livros in ACERVO.items():
            autor = Autor(nome=nome, nacionalidade=nacionalidade)
            autor.livros = [
                Livro(titulo=titulo, ano_publicacao=ano, disponivel=disponivel)
                for titulo, ano, disponivel in livros
            ]
            db.add(autor)

        db.commit()
        total_livros = sum(len(livros) for livros in ACERVO.values())
        print(f"{len(ACERVO)} autores e {total_livros} livros cadastrados.")


if __name__ == "__main__":
    popular()
