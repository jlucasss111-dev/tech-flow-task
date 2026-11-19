"""Schemas Pydantic: validação de entrada e formato de saída da API."""

from datetime import datetime
from typing import Annotated, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

from app.models import StatusTarefa

# strip_whitespace remove espaços nas pontas antes de validar o tamanho,
# então um título "   " é rejeitado como vazio
Titulo = Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=120)]
Descricao = Annotated[str, StringConstraints(strip_whitespace=True, max_length=1000)]
Responsavel = Annotated[str, StringConstraints(strip_whitespace=True, max_length=80)]


class TarefaBase(BaseModel):
    titulo: Titulo
    descricao: Descricao | None = None
    responsavel: Responsavel | None = None


class TarefaCriar(TarefaBase):
    status: StatusTarefa = StatusTarefa.A_FAZER


class TarefaAtualizar(BaseModel):
    """Atualização parcial: apenas os campos enviados são alterados."""

    titulo: Titulo | None = None
    descricao: Descricao | None = None
    responsavel: Responsavel | None = None
    status: StatusTarefa | None = None

    @model_validator(mode="after")
    def campos_obrigatorios_nao_nulos(self) -> Self:
        # Omitir o campo é permitido; enviar null explicitamente não
        for campo in ("titulo", "status"):
            if campo in self.model_fields_set and getattr(self, campo) is None:
                raise ValueError(f"O campo '{campo}' não pode ser nulo")
        return self


class TarefaLer(TarefaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: StatusTarefa
    criado_em: datetime
    atualizado_em: datetime


class Erro(BaseModel):
    detail: str = Field(examples=["Tarefa não encontrada"])
