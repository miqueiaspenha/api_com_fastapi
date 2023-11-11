from decimal import Decimal
from enum import Enum
from typing import List, Sequence

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from contas_a_pagar_e_receber.models.conta_a_pagar_e_receber_model import (
    ContaPagarReceber,
)
from shared.dependencies import get_db

router = APIRouter(prefix="/contas-a-pagar-e-receber")


class ContaPagarReceberTipoEnum(str, Enum):
    PAGAR = 'PAGAR'
    RECEBER = 'RECEBER'


class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    tipo: str  # PAGAR e RECEBER

    class Config:
        orm_mode = True


class ContaPagarReceberRequest(BaseModel):
    descricao: str = Field(min_length=3, max_length=30)
    valor: Decimal = Field(gt=0)
    tipo: ContaPagarReceberTipoEnum


@router.get("/", response_model=List[ContaPagarReceberResponse])
def lista_contas(db: Session = Depends(get_db)) -> Sequence[ContaPagarReceberResponse]:
    return db.query(ContaPagarReceber).all()


@router.get("/{id_conta_a_pagar_e_receber}", response_model=ContaPagarReceberResponse, status_code=200)
def listar_conta(id_conta_a_pagar_e_receber: int, db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    contas_a_pagar_e_receber: ContaPagarReceber = db.query(ContaPagarReceber).get(id_conta_a_pagar_e_receber)
    return contas_a_pagar_e_receber


@router.post("/", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(
    conta_a_pagar_e_receber_request: ContaPagarReceberRequest,
    db: Session = Depends(get_db),
) -> ContaPagarReceberResponse:
    contas_a_pagar_e_receber = ContaPagarReceber(
        **conta_a_pagar_e_receber_request.dict()
    )
    db.add(contas_a_pagar_e_receber)
    db.commit()
    db.refresh(contas_a_pagar_e_receber)
    # return ContaPagarReceberResponse(**contas_a_pagar_e_receber.__dict__)
    return contas_a_pagar_e_receber


@router.put("/{id_conta_a_pagar_e_receber}", response_model=ContaPagarReceberResponse, status_code=200)
def atualizar_conta(id_conta_a_pagar_e_receber: int, conta_a_pagar_e_receber_request: ContaPagarReceberRequest,
                    db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    contas_a_pagar_e_receber: ContaPagarReceber = db.query(ContaPagarReceber).get(id_conta_a_pagar_e_receber)
    contas_a_pagar_e_receber.tipo = conta_a_pagar_e_receber_request.tipo
    contas_a_pagar_e_receber.valor = conta_a_pagar_e_receber_request.valor
    contas_a_pagar_e_receber.descricao = conta_a_pagar_e_receber_request.descricao

    db.add(contas_a_pagar_e_receber)
    db.commit()
    db.refresh(contas_a_pagar_e_receber)

    return contas_a_pagar_e_receber


@router.delete("/{id_conta_a_pagar_e_receber}", status_code=204)
def deletar_conta(id_conta_a_pagar_e_receber: int,
                  db: Session = Depends(get_db)) -> None:
    contas_a_pagar_e_receber = db.query(ContaPagarReceber).get(id_conta_a_pagar_e_receber)
    db.delete(contas_a_pagar_e_receber)
    db.commit()
