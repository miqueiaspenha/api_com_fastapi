from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Sequence

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from contas_a_pagar_e_receber.models.conta_a_pagar_e_receber_model import (
    ContaPagarReceber,
)
from contas_a_pagar_e_receber.models.fornecedor_client import FornecedorCliente
from contas_a_pagar_e_receber.routers.fornecedor_cliente_router import (
    FornecedorClienteResponse,
)
from shared.dependencies import get_db
from shared.exceptions import NotFound

router = APIRouter(prefix="/contas-a-pagar-e-receber")


class ContaPagarReceberTipoEnum(str, Enum):
    PAGAR = "PAGAR"
    RECEBER = "RECEBER"


class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    tipo: str
    data_baixa: datetime | None = None
    valor_baixa: Decimal | None = None
    esta_baixada: bool | None = None
    fornecedor: FornecedorClienteResponse | None = None

    class Config:
        orm_mode = True


class ContaPagarReceberRequest(BaseModel):
    descricao: str = Field(min_length=3, max_length=30)
    valor: Decimal = Field(gt=0)
    tipo: ContaPagarReceberTipoEnum
    fornecedor_cliente_id: int | None = None


@router.get("/", response_model=List[ContaPagarReceberResponse])
def lista_contas(db: Session = Depends(get_db)) -> Sequence[ContaPagarReceberResponse]:
    return db.query(ContaPagarReceber).all()


@router.get(
    "/{id_conta_a_pagar_e_receber}",
    response_model=ContaPagarReceberResponse,
    status_code=200,
)
def listar_conta(
    id_conta_a_pagar_e_receber: int, db: Session = Depends(get_db)
) -> ContaPagarReceber:
    conta_a_pagar_e_receber: ContaPagarReceber = busca_conta_por_id(
        id_conta_a_pagar_e_receber, db
    )
    return conta_a_pagar_e_receber


@router.post("/", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(
    conta_a_pagar_e_receber_request: ContaPagarReceberRequest,
    db: Session = Depends(get_db),
) -> ContaPagarReceber:
    valida_fornecedor(conta_a_pagar_e_receber_request.fornecedor_cliente_id, db)
    contas_a_pagar_e_receber: ContaPagarReceber = ContaPagarReceber(
        **conta_a_pagar_e_receber_request.dict()
    )
    db.add(contas_a_pagar_e_receber)
    db.commit()
    db.refresh(contas_a_pagar_e_receber)
    # return ContaPagarReceberResponse(**contas_a_pagar_e_receber.__dict__)
    return contas_a_pagar_e_receber


@router.post("/{id_conta_a_pagar_e_receber}/baixar", response_model=ContaPagarReceberResponse, status_code=200)
def baixar_conta(id_conta_a_pagar_e_receber: int, db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    conta_a_pagar_e_receber: ContaPagarReceber = busca_conta_por_id(
        id_conta_a_pagar_e_receber, db
    )
    if conta_a_pagar_e_receber.esta_baixada and conta_a_pagar_e_receber.valor == conta_a_pagar_e_receber.valor_baixa:
        return conta_a_pagar_e_receber
    conta_a_pagar_e_receber.data_baixa = datetime.now()
    conta_a_pagar_e_receber.esta_baixada = True
    conta_a_pagar_e_receber.valor_baixa = conta_a_pagar_e_receber.valor
    db.add(conta_a_pagar_e_receber)
    db.commit()
    db.refresh(conta_a_pagar_e_receber)
    return conta_a_pagar_e_receber


@router.put(
    "/{id_conta_a_pagar_e_receber}",
    response_model=ContaPagarReceberResponse,
    status_code=200,
)
def atualizar_conta(
    id_conta_a_pagar_e_receber: int,
    conta_a_pagar_e_receber_request: ContaPagarReceberRequest,
    db: Session = Depends(get_db),
) -> ContaPagarReceber:
    valida_fornecedor(conta_a_pagar_e_receber_request.fornecedor_cliente_id, db)
    conta_a_pagar_e_receber: ContaPagarReceber = busca_conta_por_id(
        id_conta_a_pagar_e_receber, db
    )
    for key, value in conta_a_pagar_e_receber_request.__dict__.items():
        setattr(conta_a_pagar_e_receber, key, value)
    db.add(conta_a_pagar_e_receber)
    db.commit()
    db.refresh(conta_a_pagar_e_receber)

    return conta_a_pagar_e_receber  # type: ignore


@router.delete("/{id_conta_a_pagar_e_receber}", status_code=204)
def deletar_conta(
    id_conta_a_pagar_e_receber: int, db: Session = Depends(get_db)
) -> None:
    conta_a_pagar_e_receber: ContaPagarReceber = busca_conta_por_id(
        id_conta_a_pagar_e_receber, db
    )
    db.delete(conta_a_pagar_e_receber)
    db.commit()


def busca_conta_por_id(
    id_conta_a_pagar_e_receber: int, db: Session
) -> ContaPagarReceber:
    conta_a_pagar_e_receber: ContaPagarReceber = db.query(ContaPagarReceber).get(
        id_conta_a_pagar_e_receber
    )

    if conta_a_pagar_e_receber is None:
        raise NotFound(name="Conta a Pagar e Receber")

    return conta_a_pagar_e_receber


def valida_fornecedor(fornecedor_cliente_id: int, db: Session) -> None:
    if fornecedor_cliente_id is not None:
        fornecedor_cliente: FornecedorCliente = db.query(FornecedorCliente).get(
            fornecedor_cliente_id
        )
        if fornecedor_cliente is None:
            raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
