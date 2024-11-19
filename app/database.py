from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# URL de conexão do PostgreSQL
DATABASE_URL = "postgresql+asyncpg://gilson:admin123456789@localhost:5432/db_prompts"

# Criação do motor de conexão
engine = create_async_engine(DATABASE_URL, echo=True)

# Criando uma fábrica de sessões para gerenciar as transações com o banco
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)


Base = declarative_base()
metadata = Base.metadata