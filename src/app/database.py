"""Configuração da conexão com o banco de dados."""

import os
from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# A URL pode ser sobrescrita por variável de ambiente (ex.: PostgreSQL em produção)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tarefas.db")

# check_same_thread=False é necessário no SQLite porque o FastAPI
# pode atender requisições em threads diferentes
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Classe base de todos os modelos ORM."""


def get_db() -> Iterator[Session]:
    """Dependência do FastAPI: abre uma sessão por requisição e garante o fechamento."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
