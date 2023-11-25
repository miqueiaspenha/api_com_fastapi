from datetime import datetime

from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship

from shared.database import Base


class ContaPagarReceber(Base):
    __tablename__ = "conta_a_pagar_e_receber"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(30))
    valor = Column(Numeric())
    tipo = Column(String(30))
    data_previsao = Column(Date())
    data_baixa = Column(Date())
    valor_baixa = Column(Numeric())
    esta_baixada = Column(Boolean, default=False)

    fornecedor_cliente_id = Column(Integer, ForeignKey("fonecedor_cliente.id"))
    fornecedor = relationship("FornecedorCliente")
