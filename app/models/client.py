import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, String, func

from app.core.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    tipo_solicitacao = Column(String(100), nullable=False)
    valor_patrimonio = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), nullable=False, default="Aguardando Analise")
    prioridade = Column(String(20), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<Client(id={self.id}, nome={self.nome})>"
