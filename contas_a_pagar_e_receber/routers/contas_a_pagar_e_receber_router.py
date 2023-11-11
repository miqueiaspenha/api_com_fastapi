from decimal import Decimal
from typing import List, Sequence
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, condecimal
from sqlalchemy.orm import Session
from contas_a_pagar_e_receber.models.conta_a_pagar_e_receber_model import (
    ContaPagarReceber,
)
from enum import  Enum

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
