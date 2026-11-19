"""Rotas da interface web (HTML renderizado com Jinja2).

Segue o padrão Post/Redirect/Get: toda ação via formulário termina em um
redirect 303, evitando reenvio do formulário ao atualizar a página.
"""

from pathlib import Path

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.dependencies import obter_tarefa_ou_404
from app.models import StatusTarefa, Tarefa
from app.schemas import TarefaAtualizar, TarefaCriar

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter(include_in_schema=False)


def mensagens_de_erro(erro: ValidationError) -> list[str]:
    """Converte os erros do Pydantic em mensagens legíveis para o usuário."""
    return [f"{e['loc'][-1]}: {e['msg']}" if e["loc"] else e["msg"] for e in erro.errors()]


def campo_opcional(valor: str) -> str | None:
    """Campos de formulário vazios chegam como string vazia; tratamos como None."""
    return valor.strip() or None


def redirecionar_para_quadro() -> RedirectResponse:
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


def renderizar_quadro(
    request: Request, db: Session, erros: list[str] | None = None, codigo: int = 200
) -> HTMLResponse:
    tarefas = crud.listar_tarefas(db)
    colunas = {s: [t for t in tarefas if t.status == s] for s in StatusTarefa}
    return templates.TemplateResponse(
        request,
        "index.html",
        {"colunas": colunas, "status_lista": list(StatusTarefa), "erros": erros or []},
        status_code=codigo,
    )


def renderizar_edicao(
    request: Request, tarefa: Tarefa, erros: list[str] | None = None, codigo: int = 200
) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "editar.html",
        {"tarefa": tarefa, "status_lista": list(StatusTarefa), "erros": erros or []},
        status_code=codigo,
    )


@router.get("/", response_class=HTMLResponse)
def quadro(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    return renderizar_quadro(request, db)


@router.post("/tarefas", response_class=HTMLResponse, response_model=None)
def criar(
    request: Request,
    titulo: str = Form(...),
    descricao: str = Form(""),
    responsavel: str = Form(""),
    db: Session = Depends(get_db),
) -> HTMLResponse | RedirectResponse:
    try:
        dados = TarefaCriar(
            titulo=titulo,
            descricao=campo_opcional(descricao),
            responsavel=campo_opcional(responsavel),
        )
    except ValidationError as erro:
        return renderizar_quadro(request, db, mensagens_de_erro(erro), codigo=422)
    crud.criar_tarefa(db, dados)
    return redirecionar_para_quadro()


@router.post("/tarefas/{tarefa_id}/status")
def mover(
    novo_status: StatusTarefa = Form(...),
    tarefa: Tarefa = Depends(obter_tarefa_ou_404),
    db: Session = Depends(get_db),
) -> RedirectResponse:
    crud.atualizar_tarefa(db, tarefa, TarefaAtualizar(status=novo_status))
    return redirecionar_para_quadro()


@router.get("/tarefas/{tarefa_id}/editar", response_class=HTMLResponse)
def formulario_edicao(
    request: Request, tarefa: Tarefa = Depends(obter_tarefa_ou_404)
) -> HTMLResponse:
    return renderizar_edicao(request, tarefa)


@router.post("/tarefas/{tarefa_id}/editar", response_class=HTMLResponse, response_model=None)
def editar(
    request: Request,
    titulo: str = Form(...),
    descricao: str = Form(""),
    responsavel: str = Form(""),
    novo_status: StatusTarefa = Form(..., alias="status"),
    tarefa: Tarefa = Depends(obter_tarefa_ou_404),
    db: Session = Depends(get_db),
) -> HTMLResponse | RedirectResponse:
    try:
        dados = TarefaAtualizar(
            titulo=titulo,
            descricao=campo_opcional(descricao),
            responsavel=campo_opcional(responsavel),
            status=novo_status,
        )
    except ValidationError as erro:
        return renderizar_edicao(request, tarefa, mensagens_de_erro(erro), codigo=422)
    crud.atualizar_tarefa(db, tarefa, dados)
    return redirecionar_para_quadro()


@router.post("/tarefas/{tarefa_id}/excluir")
def excluir(
    tarefa: Tarefa = Depends(obter_tarefa_ou_404), db: Session = Depends(get_db)
) -> RedirectResponse:
    crud.excluir_tarefa(db, tarefa)
    return redirecionar_para_quadro()
