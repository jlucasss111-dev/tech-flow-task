"""Modelos ORM (tabelas do banco de dados)."""

import enum
from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def agora_utc() -> datetime:
    return datetime.now(UTC)


class StatusTarefa(enum.StrEnum):
    """Etapas do fluxo Kanban."""

    A_FAZER = "a_fazer"
    EM_PROGRESSO = "em_progresso"
    CONCLUIDO = "concluido"

    @property
    def rotulo(self) -> str:
        return {
            StatusTarefa.A_FAZER: "A Fazer",
            StatusTarefa.EM_PROGRESSO: "Em Progresso",
            StatusTarefa.CONCLUIDO: "Concluído",
        }[self]


class Tarefa(Base):
    __tablename__ = "tarefas"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(120))
    descricao: Mapped[str | None] = mapped_column(Text, default=None)
    responsavel: Mapped[str | None] = mapped_column(String(80), default=None)
    status: Mapped[StatusTarefa] = mapped_column(
        # values_callable: grava o valor ("a_fazer") e não o nome do membro ("A_FAZER")
        Enum(
            StatusTarefa,
            native_enum=False,
            length=20,
            values_callable=lambda e: [m.value for m in e],
        ),
        default=StatusTarefa.A_FAZER,
    )
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora_utc)
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=agora_utc, onupdate=agora_utc
    )

    def __repr__(self) -> str:
        return f"<Tarefa id={self.id} titulo={self.titulo!r} status={self.status.value}>"
