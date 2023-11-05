from decimal import Decimal
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/contas-a-pagar-e-receber")


class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    tipo: str  # PAGAR e RECEBER


class ContaPagarReceberRequest(BaseModel):
    descricao: str
    valor: Decimal
    tipo: str  # PAGAR e RECEBER


@router.get("/", response_model=List[ContaPagarReceberResponse])
def lista_contas():
    return [
        ContaPagarReceberResponse(
            id=1, descricao="aluguel", valor=1000.50, tipo="PAGAR"
        ),
        ContaPagarReceberResponse(
            id=1, descricao="Salario", valor=5000, tipo="RECEBER"
        ),
    ]


@router.post("/", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta: ContaPagarReceberRequest):
    return ContaPagarReceberResponse(
        id=3, descricao=conta.descricao, valor=conta.valor, tipo=conta.tipo
    )
