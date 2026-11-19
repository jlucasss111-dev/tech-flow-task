"""Ponto de entrada da aplicação FastAPI."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app import crud
from app.database import Base, engine, get_db
from app.models import StatusTarefa, Tarefa
from app.schemas import Erro, TarefaAtualizar, TarefaCriar, TarefaLer


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # Cria as tabelas na inicialização (suficiente para o escopo do projeto;
    # em produção o ideal seria usar migrações com Alembic)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="TechFlow Tasks",
    description="API de gerenciamento de tarefas ágeis",
    version="1.0.0",
    lifespan=lifespan,
)


def obter_tarefa_ou_404(tarefa_id: int, db: Session = Depends(get_db)) -> Tarefa:
    """Dependência reutilizada pelas rotas que operam sobre uma tarefa específica."""
    tarefa = crud.obter_tarefa(db, tarefa_id)
    if tarefa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    return tarefa


# --------------------------------------------------------------------------- #
# API REST
# --------------------------------------------------------------------------- #
RESPOSTA_404 = {404: {"model": Erro}}


@app.post(
    "/api/tarefas",
    response_model=TarefaLer,
    status_code=status.HTTP_201_CREATED,
    tags=["tarefas"],
)
def api_criar_tarefa(dados: TarefaCriar, db: Session = Depends(get_db)) -> Tarefa:
    return crud.criar_tarefa(db, dados)


@app.get("/api/tarefas", response_model=list[TarefaLer], tags=["tarefas"])
def api_listar_tarefas(
    filtro_status: StatusTarefa | None = Query(None, alias="status"),
    db: Session = Depends(get_db),
) -> list[Tarefa]:
    return crud.listar_tarefas(db, status=filtro_status)


@app.get(
    "/api/tarefas/{tarefa_id}",
    response_model=TarefaLer,
    responses=RESPOSTA_404,
    tags=["tarefas"],
)
def api_obter_tarefa(tarefa: Tarefa = Depends(obter_tarefa_ou_404)) -> Tarefa:
    return tarefa


@app.patch(
    "/api/tarefas/{tarefa_id}",
    response_model=TarefaLer,
    responses=RESPOSTA_404,
    tags=["tarefas"],
)
def api_atualizar_tarefa(
    dados: TarefaAtualizar,
    tarefa: Tarefa = Depends(obter_tarefa_ou_404),
    db: Session = Depends(get_db),
) -> Tarefa:
    return crud.atualizar_tarefa(db, tarefa, dados)


@app.delete(
    "/api/tarefas/{tarefa_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=RESPOSTA_404,
    tags=["tarefas"],
)
def api_excluir_tarefa(
    tarefa: Tarefa = Depends(obter_tarefa_ou_404), db: Session = Depends(get_db)
) -> Response:
    crud.excluir_tarefa(db, tarefa)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
