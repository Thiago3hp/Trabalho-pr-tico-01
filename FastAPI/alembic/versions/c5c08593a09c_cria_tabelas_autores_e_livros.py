"""cria tabelas autores e livros

Revision ID: c5c08593a09c
Revises:
"""
import sqlalchemy as sa
from alembic import op

revision = "c5c08593a09c"
down_revision = None


def upgrade() -> None:
    op.create_table(
        "autores",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("nacionalidade", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "livros",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("titulo", sa.String(length=150), nullable=False),
        sa.Column("ano_publicacao", sa.Integer(), nullable=True),
        sa.Column("disponivel", sa.Boolean(), nullable=False),
        sa.Column("autor_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["autor_id"], ["autores.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_livros_autor_id", "livros", ["autor_id"])


def downgrade() -> None:
    op.drop_index("ix_livros_autor_id", table_name="livros")
    op.drop_table("livros")
    op.drop_table("autores")
