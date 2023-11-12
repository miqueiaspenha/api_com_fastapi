from sqlalchemy import Column, Integer, String

from shared.database import Base


class FornecedorCliente(Base):
    __tablename__ = "fonecedor_client"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255))
