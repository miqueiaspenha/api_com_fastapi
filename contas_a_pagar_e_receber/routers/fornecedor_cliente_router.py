from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from contas_a_pagar_e_receber.models.fornecedor_client import FornecedorCliente
from shared.dependencies import get_db
from shared.exceptions import NotFound

router = APIRouter(prefix="/fornecedor-cliente")


class FornecedorClienteResponse(BaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True


class FornecedorClienteRequest(BaseModel):
    nome: str = Field(min_length=3, max_length=255)


@router.get("", response_model=List[FornecedorClienteResponse])
def listar_fornecedor_client(
    db: Session = Depends(get_db),
) -> List[FornecedorClienteResponse]:
    return db.query(FornecedorCliente).all()


@router.get(
    "/{fornecedor_cliente_id}",
    response_model=FornecedorClienteResponse,
    status_code=200,
)
def obter_fornecedor_cliente_por_id(
    fornecedor_cliente_id: int, db: Session = Depends(get_db)
) -> List[FornecedorClienteResponse]:
    return buscar_fornecedor_cliente_por_id(fornecedor_cliente_id, db)


@router.post("", response_model=FornecedorClienteResponse, status_code=201)
def criar_fornecedor_cliente(
    fornecedor_cliente_request: FornecedorClienteRequest, db: Session = Depends(get_db)
) -> FornecedorClienteResponse:
    fornecedor_cliente: FornecedorCliente = FornecedorCliente(
        **fornecedor_cliente_request.dict()
    )

    db.add(fornecedor_cliente)
    db.commit()
    db.refresh(fornecedor_cliente)

    return fornecedor_cliente


@router.put(
    "/{fornecedor_cliente_id}",
    response_model=FornecedorClienteResponse,
    status_code=200,
)
def atualizar_forncedor_cliente(
    fornecedor_cliente_id: int,
    fornecedor_cliente_request: FornecedorClienteRequest,
    db: Session = Depends(get_db),
) -> FornecedorClienteResponse:
    fornecedor_cliente = buscar_fornecedor_cliente_por_id(fornecedor_cliente_id, db)

    fornecedor_cliente.nome = fornecedor_cliente_request.nome

    db.add(fornecedor_cliente)
    db.commit()
    db.refresh(fornecedor_cliente)

    return fornecedor_cliente


@router.delete("/{fornecedor_cliente_id}", status_code=204)
def deletar_fornecedor_cliente(
    fornecedor_cliente_id: int, db: Session = Depends(get_db)
) -> None:
    fornecedor_cliente = buscar_fornecedor_cliente_por_id(fornecedor_cliente_id, db)

    db.delete(fornecedor_cliente)
    db.commit()


def buscar_fornecedor_cliente_por_id(fornecedor_cliente_id: int, db: Session):
    fornecedor_cliente = db.query(FornecedorCliente).get(fornecedor_cliente_id)

    if fornecedor_cliente is None:
        raise NotFound("Fornecedor Cliente")

    return fornecedor_cliente
