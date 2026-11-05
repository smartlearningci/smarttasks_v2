# SmartTasks — MVP pedagógico

Aplicação local de gestão de tarefas da empresa fictícia TaskFlow. Permite **listar, criar, concluir e reabrir** tarefas. Estados: **Aberta** e **Concluída**. Sem login nem base de dados; os dados vivem apenas na memória do processo.

## Requisitos prévios

- Git e Docker com suporte a `docker compose` (para execução em container).
- Python 3.12 e pip (apenas se pretender correr testes localmente sem Docker).

## Clonar

```bash
git clone https://github.com/smartlearningci/smarttasks_v2.git
cd smarttasks_v2
```

## Build e arranque

```bash
docker compose build
docker compose up -d
```

Abrir **http://localhost:8080**. A documentação interativa da API está em **http://localhost:8080/docs** e a verificação de saúde em **http://localhost:8080/health**. A porta 8080 está associada apenas a `127.0.0.1` no computador local.

Ver estado e logs:

```bash
docker compose ps
docker compose logs --tail=50 smarttasks
curl http://localhost:8080/health
```

## Testes automatizados

O Dockerfile instala as dependências, incluindo pytest, mas não copia a pasta `tests` para a imagem de execução. Para correr os testes **no computador local**:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v
```

A suite cobre os casos API **T-01 a T-08**, parcialmente T-09/T-10/T-11/T-12. **T-13** e a validação real de Docker/reinício exigem inspeção manual. Ver `docs/05_rastreabilidade_e_testes.md` para os critérios de aceitação e a distinção entre testes automatizados e manuais.

## Paragem

```bash
docker compose down
```

**Importante:** atualizar a página não apaga as tarefas enquanto o processo continua ativo. Reiniciar/recriar o processo perde todas as tarefas; não existem volumes nem persistência. A aplicação usa um único processo Uvicorn para preservar uma lista coerente durante a demonstração.

## Organização

- `app/main.py`: rotas FastAPI e interface HTML.
- `app/models.py`: modelos e validações Pydantic.
- `app/service.py`: regras de negócio.
- `app/storage.py`: armazenamento em memória.
- `app/static/`: HTML, JavaScript e CSS sem serviços externos.
- `tests/`: testes API e verificações estruturais.
- `Dockerfile`, `compose.yaml`, `.dockerignore`: execução Docker.
- `docs/`: requisitos, User Stories e rastreabilidade aprovados.

## Limites do MVP

Sem PostgreSQL, autenticação, edição/remoção de tarefas, atribuições, filas, CI/CD, observabilidade avançada ou serviços externos. Não incluir credenciais no repositório.
