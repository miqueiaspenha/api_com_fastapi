from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from shared.database import Base
from shared.dependencies import get_db

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_deve_listar_fornecdor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post("/fornecedor-cliente", json={"nome": "CPFL"})
    client.post("/fornecedor-cliente", json={"nome": "Sanasa"})

    response_get = client.get("/fornecedor-cliente")
    assert response_get.status_code == 200
    assert response_get.json() == [
        {"id": 1, "nome": "CPFL"},
        {"id": 2, "nome": "Sanasa"}
    ]


def test_deve_retornar_por_id_um_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post("/fornecedor-cliente", json={"nome": "CPFL"})
    id_fornecedor_cliente = response_post.json()["id"]

    response_get = client.get(f"/fornecedor-cliente/{id_fornecedor_cliente}")
    assert response_get.status_code == 200
    assert response_get.json()["nome"] == "CPFL"


def test_deve_retornar_nao_encontrado_para_id_fornecedor_clinete_nao_existente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_get = client.get(f"/fornecedor-cliente/100")
    assert response_get.status_code == 404


def test_deve_criar_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post("/fornecedor-cliente", json={
        "nome": "CPFL"
    })

    assert response_post.status_code == 201
    assert response_post.json() == {"id": 1, "nome": "CPFL"}


def test_deve_atualizar_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post("/fornecedor-cliente/", json={"nome": "CPFL"})

    id_fornecedor_cliente = response_post.json()["id"]

    response_put = client.put(f"/fornecedor-cliente/{id_fornecedor_cliente}", json={
        "nome": "Sanasa"
    })

    assert response_put.status_code == 200
    assert response_put.json()["nome"] == "Sanasa"


def test_deve_retornar_nao_encontrado_para_id_fornecedor_cliente_nao_existente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_get = client.put("/fornecedor-cliente/100", json={
        "nome": "CPFL"
    })

    assert response_get.status_code == 404


def test_deve_apagar_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post("/fornecedor-cliente", json={
        "nome": "CPFL"
    })
    id_cliente_fornecedor = response_post.json()["id"]

    response_delete = client.delete(f"/fornecedor-cliente/{id_cliente_fornecedor}")
    assert response_delete.status_code == 204

    response_get_all = client.get("/fornecedor-cliente")

    assert len(response_get_all.json()) == 0


def test_deve_retornar_nao_encontrado_para_id_fornecedor_cliente_na_remocao():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_delete = client.delete("/fornecedor-cliente/100")
    assert response_delete.status_code == 404


def test_deve_retornar_erro_quando_o_nome_for_menor_que_o_solicitado():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post("/fornecedor-cliente", json={
        "nome": "a"
    })
    assert response_post.status_code == 422


def test_deve_retornar_erro_quando_o_nome_for_meno_que_o_solicitado():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post("/fornecedor-cliente", json={
        "nome": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the "
                "industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type "
                "and scrambled it to make a type specimen book. It has survived not only five centuries, but also the "
                "leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s "
                "with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop "
                "publishing software like Aldus PageMaker including versions of Lorem Ipsum."
    })

    assert response_post.status_code == 422
