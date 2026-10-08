from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Livro(Base):
    __tablename__ = "livros"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(150))
    ano_publicacao: Mapped[int | None]
    disponivel: Mapped[bool] = mapped_column(default=True)
    autor_id: Mapped[int] = mapped_column(ForeignKey("autores.id"), index=True)

    autor: Mapped["Autor"] = relationship(back_populates="livros", lazy="joined")
