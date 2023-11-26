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


def test_deve_listar_contas_de_um_fornecdor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    client.post("/fornecedor-cliente", json={"nome": "CPFL"})
    client.post(
        "/contas-a-pagar-e-receber",
        json={
            "descricao": "Curso de Python",
            "valor": 111,
            "tipo": "PAGAR",
            "fornecedor_cliente_id": 1,
            "valor_baixa": None,
            "data_baixa": None,
            "esta_baixada": False,
            "data_previsao": "2022-11-29",
        },
    )
    client.post(
        "/contas-a-pagar-e-receber",
        json={
            "descricao": "Curso de Java",
            "valor": 112,
            "tipo": "PAGAR",
            "fornecedor_cliente_id": 1,
            "valor_baixa": None,
            "data_baixa": None,
            "esta_baixada": False,
            "data_previsao": "2022-11-29",
        },
    )

    response_get = client.get("/fornecedor-cliente/1/contas-a-pagar-e-receber")
    assert response_get.status_code == 200
    assert len(response_get.json()) == 2


def test_deve_retornar_uma_lista_vazia_de_contas_de_um_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    client.post("/fornecedor-cliente", json={"nome": "CPFL"})
    response_get = client.get("/fornecedor-cliente/1/contas-a-pagar-e-receber")
    assert response_get.status_code == 200
    assert len(response_get.json()) == 0
