"""Dependências compartilhadas entre as rotas da API e da interface web."""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.models import Tarefa


def obter_tarefa_ou_404(tarefa_id: int, db: Session = Depends(get_db)) -> Tarefa:
    """Busca a tarefa pelo id da rota ou responde 404 se ela não existir."""
    tarefa = crud.obter_tarefa(db, tarefa_id)
    if tarefa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    return tarefa
