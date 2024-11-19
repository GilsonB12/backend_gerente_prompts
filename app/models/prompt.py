from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # Nome do prompt
    content = Column(String, nullable=False)           # Conteúdo do prompt
    version = Column(Integer, default=1, nullable=False)  # Controle de versão
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # Usuário que criou
    created_at = Column(DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de atualização

    creator = relationship("User")  # Relacionamento com a tabela de usuários


class PromptVersion(Base):
    __tablename__ = "prompt_versions"

    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"), nullable=False)
    name = Column(String, nullable=False)
    content = Column(String, nullable=False)
    version = Column(Integer, nullable=False)
    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
