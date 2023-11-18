from sqlalchemy import Column, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship

from shared.database import Base


class ContaPagarReceber(Base):
    __tablename__ = "conta_a_pagar_e_receber"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(30))
    valor = Column(Numeric)
    tipo = Column(String(30))

    fornecedor_cliente_id = Column(Integer, ForeignKey("fonecedor_cliente.id"))
    fornecedor = relationship("FornecedorCliente")

    def update(self, **kwargs):
        print(kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)
