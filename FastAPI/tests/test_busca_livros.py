"""Testes dos filtros de busca de GET /livros (título e nome do autor)."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Sessao = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    def get_db_teste():
        with Sessao() as db:
            yield db

    app.dependency_overrides[get_db] = get_db_teste
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def acervo(client):
    machado = client.post("/autores", json={"nome": "Machado de Assis"}).json()
    clarice = client.post("/autores", json={"nome": "Clarice Lispector"}).json()
    livros = [
        ("Dom Casmurro", machado["id"], True),
        ("Memórias Póstumas de Brás Cubas", machado["id"], False),
        ("A Hora da Estrela", clarice["id"], True),
        ("Perto do Coração Selvagem", clarice["id"], True),
    ]
    for titulo, autor_id, disponivel in livros:
        r = client.post(
            "/livros",
            json={"titulo": titulo, "autor_id": autor_id, "disponivel": disponivel},
        )
        assert r.status_code == 201
    return client


def titulos(resposta):
    assert resposta.status_code == 200
    return [l["titulo"] for l in resposta.json()]


def test_sem_filtros_retorna_tudo(acervo):
    assert len(titulos(acervo.get("/livros"))) == 4


def test_busca_por_titulo(acervo):
    assert titulos(acervo.get("/livros", params={"titulo": "casmurro"})) == ["Dom Casmurro"]


def test_busca_por_titulo_parcial_ignora_maiusculas(acervo):
    assert len(titulos(acervo.get("/livros", params={"titulo": "DA"}))) >= 1


def test_busca_por_autor(acervo):
    r = acervo.get("/livros", params={"autor": "clarice"})
    assert titulos(r) == ["A Hora da Estrela", "Perto do Coração Selvagem"]
    assert all(l["autor"]["nome"] == "Clarice Lispector" for l in r.json())


def test_busca_por_parte_do_nome_do_autor(acervo):
    assert len(titulos(acervo.get("/livros", params={"autor": "assis"}))) == 2


def test_titulo_e_autor_combinados(acervo):
    r = acervo.get("/livros", params={"titulo": "hora", "autor": "clarice"})
    assert titulos(r) == ["A Hora da Estrela"]


def test_titulo_e_autor_incompativeis_retorna_vazio(acervo):
    r = acervo.get("/livros", params={"titulo": "casmurro", "autor": "clarice"})
    assert titulos(r) == []


def test_combina_com_disponibilidade(acervo):
    r = acervo.get("/livros", params={"autor": "machado", "disponivel": "false"})
    assert titulos(r) == ["Memórias Póstumas de Brás Cubas"]


def test_combina_com_paginacao(acervo):
    r = acervo.get("/livros", params={"autor": "clarice", "skip": 1, "limit": 1})
    assert titulos(r) == ["Perto do Coração Selvagem"]


def test_busca_vazia_ou_so_espacos_nao_filtra(acervo):
    assert len(titulos(acervo.get("/livros", params={"titulo": "  ", "autor": ""}))) == 4


def test_percentual_e_tratado_como_texto_literal(acervo):
    # '%' não pode virar curinga e casar com tudo
    assert titulos(acervo.get("/livros", params={"titulo": "%"})) == []


def test_sem_resultado_retorna_lista_vazia(acervo):
    assert titulos(acervo.get("/livros", params={"titulo": "inexistente"})) == []
