from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from contas_a_pagar_e_receber.models.conta_a_pagar_e_receber_model import ContaPagarReceber
from contas_a_pagar_e_receber.routers.contas_a_pagar_e_receber_router import ContaPagarReceberResponse
from shared.dependencies import get_db

router = APIRouter(prefix="/fornecedor-cliente")


@router.get("/{fornecedor_cliente_id}/contas-a-pagar-e-receber", response_model=List[ContaPagarReceberResponse])
def obter_fornecedor_cliente_por_id(
    fornecedor_cliente_id: int,
    db: Session = Depends(get_db)
) -> List[ContaPagarReceberResponse]:
    return db.query(ContaPagarReceber).filter_by(fornecedor_cliente_id=fornecedor_cliente_id).all()
