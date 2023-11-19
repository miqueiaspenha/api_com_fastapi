from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from shared.database import Base


class ContaPagarReceber(Base):
    __tablename__ = "conta_a_pagar_e_receber"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(30))
    valor = Column(Numeric())
    tipo = Column(String(30))
    data_baixa = Column(DateTime())
    valor_baixa = Column(Numeric())
    esta_baixada = Column(Boolean, default=False)

    fornecedor_cliente_id = Column(Integer, ForeignKey("fonecedor_cliente.id"))
    fornecedor = relationship("FornecedorCliente")
