# TechFlow Tasks

Sistema web de gerenciamento de tarefas desenvolvido pela **TechFlow Solutions** (empresa fictícia) para uma startup de logística. Projeto acadêmico da disciplina de Engenharia de Software.

## Objetivo

Permitir que a equipe do cliente acompanhe o fluxo de trabalho em tempo real, registrando tarefas e movendo-as entre as etapas **A Fazer → Em Progresso → Concluído**.

## Escopo inicial

**Dentro do escopo (v1):**

- Cadastro de tarefas (título, descrição, responsável)
- Listagem de tarefas com filtro por status
- Edição de tarefas e alteração de status
- Exclusão de tarefas
- API REST documentada (Swagger em `/docs`)
- Interface web simples
- Testes automatizados e integração contínua

**Fora do escopo (v1):**

- Autenticação e controle de acesso por usuário
- Notificações em tempo real
- Relatórios de desempenho da equipe

## Metodologia

Adotamos um modelo **híbrido (Scrumban)**:

- **Kanban** no GitHub Projects para visualizar o fluxo de trabalho, com as colunas *To Do*, *In Progress* e *Done*. Cada card corresponde a uma entrega pequena e verificável.
- **Sprints curtas** (1 semana) com uma revisão ao final, em que o cliente valida o que foi entregue e pode solicitar mudanças de escopo.
- **Integração contínua**: todo push e pull request executa lint e testes automatizados no GitHub Actions.
- **Commits semânticos** ([Conventional Commits](https://www.conventionalcommits.org/pt-br/)): `feat`, `fix`, `test`, `docs`, `ci`, `chore`, `refactor`.

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.11+ |
| Framework web / API | FastAPI |
| Templates | Jinja2 |
| Banco de dados | SQLite + SQLAlchemy 2 |
| Testes | Pytest + HTTPX (TestClient) |
| Qualidade de código | Ruff (lint e formatação) |
| CI | GitHub Actions |

## Estrutura do repositório

```
├── .github/workflows/   # pipeline de CI
├── docs/                # diagramas UML e documentação
├── src/app/             # código-fonte da aplicação
└── tests/               # testes automatizados
```

## Como executar

```bash
# 1. Criar e ativar um ambiente virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# 2. Instalar as dependências
pip install -r requirements-dev.txt

# 3. Subir o servidor
uvicorn app.main:app --app-dir src --reload
```

- Interface web: http://127.0.0.1:8000
- Documentação da API: http://127.0.0.1:8000/docs
