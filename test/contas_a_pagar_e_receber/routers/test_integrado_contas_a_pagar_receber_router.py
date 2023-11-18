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

    client.post("/contas-a-pagar-e-receber", json=conta1)
    client.post("/contas-a-pagar-e-receber", json=conta2)

    response = client.get("/contas-a-pagar-e-receber")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "descricao": "aluguel",
            "valor": 1000.5,
            "tipo": "PAGAR",
            "fornecedor": None,
        },
        {
            "id": 2,
            "descricao": "Salario",
            "valor": 5000,
            "tipo": "RECEBER",
            "fornecedor": None,
        },
    ]


def test_deve_retornar_uma_conta_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    conta_a_pagar_e_receber = {
        "descricao": "aluguel",
        "valor": 1000.5,
        "tipo": "PAGAR",
        "fornecedor": None,
    }

    response_post = client.post(
        "/contas-a-pagar-e-receber", json=conta_a_pagar_e_receber
    )
    id_conta_a_pagar_e_receber = response_post.json()["id"]

    response_get = client.get(f"/contas-a-pagar-e-receber/{id_conta_a_pagar_e_receber}")
    conta_a_pagar_e_receber_copy = conta_a_pagar_e_receber.copy()
    conta_a_pagar_e_receber_copy["id"] = 1

    assert response_get.status_code == 200
    assert response_get.json() == conta_a_pagar_e_receber_copy


def test_deve_retornar_nao_encontrado_para_id_nao_existente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_get = client.get("/contas-a-pagar-e-receber/100")
    assert response_get.status_code == 404


def test_deve_criar_conta_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    nova_conta = {
        "descricao": "Curso de Python",
        "valor": 333,
        "tipo": "PAGAR",
        "fornecedor": None,
    }

    response = client.post(
        "/contas-a-pagar-e-receber",
        json=nova_conta,
    )

    assert response.status_code == 201
    nova_conta_copy = nova_conta.copy()
    nova_conta_copy["id"] = 1
    assert response.json() == nova_conta_copy


def test_deve_atualizar_conta_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response_post = client.post(
        "/contas-a-pagar-e-receber",
        json={"descricao": "Curso de Python", "valor": 333, "tipo": "PAGAR"},
    )
    contas_a_pagar_e_receber_id = response_post.json()["id"]
    response_put = client.put(
        f"/contas-a-pagar-e-receber/{contas_a_pagar_e_receber_id}",
        json={"descricao": "Curso de Python", "valor": 111, "tipo": "PAGAR"},
    )
    assert response_put.status_code == 200
    assert response_put.json()["valor"] == 111


def test_deve_retornar_nao_encontrado_para_id_nao_existente_na_atalizacao():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_get = client.put(
        "/contas-a-pagar-e-receber/100",
        json={"descricao": "Curso de Python", "valor": 333, "tipo": "PAGAR"},
    )
    assert response_get.status_code == 404


def test_deve_apagar_conta_apagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post(
        "/contas-a-pagar-e-receber",
        json={"descricao": "Curso de Python", "valor": 111, "tipo": "PAGAR"},
    )
    contas_a_pagar_e_receber_id = response_post.json()["id"]

    response_delete = client.delete(
        f"/contas-a-pagar-e-receber/{contas_a_pagar_e_receber_id}"
    )
    assert response_delete.status_code == 204


def test_deve_retornar_nao_encontrado_para_id_nao_existente_na_remocao():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_delete = client.delete("/contas-a-pagar-e-receber/100")
    assert response_delete.status_code == 404


def test_deve_retornar_erro_quando_exceder_a_descricao():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    reponse = client.post(
        "/contas-a-pagar-e-receber",
        json={
            "descricao": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum "
                         "has been the industry's standard dummy text ever since the 1500s, when an unknown printer "
                         "took a galley of type and scrambled it to make a type specimen book. ",
            "valor": 333,
            "tipo": "PAGAR",
        },
    )
    assert reponse.status_code == 422


def test_deve_retornar_erro_quando_descricao_for_menor_que_o_necessario():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response = client.post(
        "/contas-a-pagar-e-receber",
        json={"descricao": "ab", "valor": 333, "tipo": "PAGAR"},
    )
    assert response.status_code == 422


def test_deve_retornar_erro_quando_o_valor_for_zero_ou_menor():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response = client.post(
        "/contas-a-pagar-e-receber",
        json={"descricao": "Lorem Ipsum", "valor": 0, "tipo": "PAGAR"},
    )
    assert response.status_code == 422

    response = client.post(
        "/contas-a-pagar-e-receber",
        json={"descricao": "Lorem Ipsum", "valor": -1, "tipo": "PAGAR"},
    )
    assert response.status_code == 422


def test_deve_retornar_erro_quando_o_tipo_for_invalido():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response = client.post(
        "/contas-a-pagar-e-receber",
        json={"descricao": "Test", "valor": 100, "tipo": "INVALIDO"},
    )
    assert response.status_code == 422


def test_deve_criar_conta_a_pagar_e_receber_com_fornedor():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    client.post("/fornecedor-cliente", json={"nome": "CPFL"})
    response_post = client.post(
        "/contas-a-pagar-e-receber",
        json={
            "descricao": "Curso de Python",
            "valor": 111,
            "tipo": "PAGAR",
            "fornecedor_cliente_id": 1
        })
    assert response_post.status_code == 201
    assert response_post.json() == {
        "id": 1,
        "descricao": "Curso de Python",
        "valor": 111,
        "tipo": "PAGAR",
        "fornecedor": {
            "id": 1,
            "nome": "CPFL"
        }
    }


def test_deve_retornar_erro_ao_inserir_uma_nova_conta_com_fornecedor_invalido():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response_post = client.post("/contas-a-pagar-e-receber", json={
        "descricao": "Curso de Python",
        "valor": 111,
        "tipo": "PAGAR",
        "fornecedor_cliente_id": 1000
    })
    assert response_post.status_code == 404


def test_deve_atualizar_conta_a_pagar_com_forncedor_client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    client.post("/fornecedor-cliente", json={"nome": "CPFL"})
    client.post(
        "/contas-a-pagar-e-receber",
        json={
            "descricao": "Curso de Python",
            "valor": 111,
            "tipo": "PAGAR",
            "fornecedor_cliente_id": 1
        })
    response_put = client.put("/contas-a-pagar-e-receber/1", json={
        "descricao": "Curso de Python",
        "valor": 111,
        "tipo": "PAGAR",
        "fornecedor_cliente_id": 1
    })
    assert response_put.status_code == 200
    assert response_put.json() == {
        "id": 1,
        "descricao": "Curso de Python",
        "valor": 111,
        "tipo": "PAGAR",
        "fornecedor": {
            "id": 1,
            "nome": "CPFL"
        }
    }

def test_deve_retornar_erro_ao_atualizar_uma_conta_com_fornecedor_invalido():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    client.post("/contas-a-pagar-e-receber", json={
        "descricao": "Curso de Python",
        "valor": 111,
        "tipo": "PAGAR",
        "fornecedor_cliente_id": None
    })
    response_put = client.put("/contas-a-pagar-e-receber/1", json={
        "descricao": "Curso de Python",
        "valor": 111,
        "tipo": "PAGAR",
        "fornecedor_cliente_id": 1000
    })
    assert response_put.status_code == 404
