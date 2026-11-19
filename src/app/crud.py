"""Operações de acesso a dados (Create, Read, Update, Delete).

As funções recebem a sessão como parâmetro para ficarem desacopladas
do FastAPI e poderem ser testadas isoladamente.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import StatusTarefa, Tarefa
from app.schemas import TarefaAtualizar, TarefaCriar


def criar_tarefa(db: Session, dados: TarefaCriar) -> Tarefa:
    tarefa = Tarefa(**dados.model_dump())
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)
    return tarefa


def listar_tarefas(db: Session, status: StatusTarefa | None = None) -> list[Tarefa]:
    consulta = select(Tarefa)
    if status is not None:
        consulta = consulta.where(Tarefa.status == status)
    consulta = consulta.order_by(Tarefa.criado_em.desc(), Tarefa.id.desc())
    return list(db.scalars(consulta))


def obter_tarefa(db: Session, tarefa_id: int) -> Tarefa | None:
    return db.get(Tarefa, tarefa_id)


def atualizar_tarefa(db: Session, tarefa: Tarefa, dados: TarefaAtualizar) -> Tarefa:
    # exclude_unset: ignora campos que o cliente não enviou (atualização parcial)
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(tarefa, campo, valor)
    db.commit()
    db.refresh(tarefa)
    return tarefa


def excluir_tarefa(db: Session, tarefa: Tarefa) -> None:
    db.delete(tarefa)
    db.commit()
