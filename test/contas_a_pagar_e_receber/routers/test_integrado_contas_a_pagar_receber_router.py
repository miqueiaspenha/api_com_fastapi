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


def test_deve_listar_contas_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    conta1 = {"descricao": "aluguel", "valor": "1000.5", "tipo": "PAGAR"}
    conta2 = {"descricao": "Salario", "valor": "5000", "tipo": "RECEBER"}

    client.post(url="/contas-a-pagar-e-receber", json=conta1)
    client.post(url="/contas-a-pagar-e-receber", json=conta2)

    response = client.get("/contas-a-pagar-e-receber")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "descricao": "aluguel", "valor": 1000.5, "tipo": "PAGAR"},
        {"id": 2, "descricao": "Salario", "valor": 5000, "tipo": "RECEBER"},
    ]


def test_deve_criar_conta_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    nova_conta = {"descricao": "Curso de Python", "valor": 333, "tipo": "PAGAR"}

    response = client.post(
        "/contas-a-pagar-e-receber",
        json=nova_conta,
    )

    assert response.status_code == 201
    nova_conta_copy = nova_conta.copy()
    nova_conta_copy["id"] = 1
    assert response.json() == nova_conta_copy


def test_deve_retornar_erro_quando_exceder_a_descricao():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    reponse = client.post(
        "/contas-a-pagar-e-receber",
        json={"descricao": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum "
                           "has been the industry's standard dummy text ever since the 1500s, when an unknown printer "
                           "took a galley of type and scrambled it to make a type specimen book. ", "valor": 333,
              "tipo": "PAGAR"}
    )
    assert reponse.status_code == 422


def test_deve_retornar_erro_quando_descricao_for_menor_que_o_necessario():
    response = client.post("/contas-a-pagar-e-receber", json={
        "descricao": "ab",
        "valor": 333,
        "tipo": "PAGAR"
    })
    assert response.status_code == 422


def test_deve_retornar_erro_quando_o_valor_for_zero_ou_menor():
    response = client.post("/contas-a-pagar-e-receber", json={
        "descricao": "Lorem Ipsum",
        "valor": 0,
        "tipo": "PAGAR"
    })
    assert response.status_code == 422

    response = client.post("/contas-a-pagar-e-receber", json={
        "descricao": "Lorem Ipsum",
        "valor": -1,
        "tipo": "PAGAR"
    })
    assert response.status_code == 422


def test_deve_retornar_erro_quando_o_tipo_for_invalido():
    response = client.post("/contas-a-pagar-e-receber", json={
        "descricao": "Test",
        "valor": 100,
        "tipo": "INVALIDO"
    })
    assert response.status_code == 422
