from sqlalchemy import Column, Integer, Numeric, String
from shared.database import Base


class ContaPagarReceber(Base):
    __tablename__ = "conta_a_pagar_e_receber"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(30))
    valor = Column(Numeric)
    tipo = Column(String(30))
