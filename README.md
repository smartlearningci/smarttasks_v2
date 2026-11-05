# SmartTasks — MVP com PostgreSQL

Aplicação pedagógica TaskFlow: listar, criar, concluir e reabrir tarefas.
A interface HTML e a API original são mantidas. No Docker Compose, as tarefas
e os estados são guardados em PostgreSQL 17, no volume `postgres_data`.

## Pré-requisitos e configuração

Git e Docker Compose. Python 3.12 é necessário apenas para testes locais.

```bash
git clone https://github.com/smartlearningci/smarttasks_v2.git
cd smarttasks_v2
cp .env.example .env
```

**Editar `.env` e substituir `SUBSTITUIR_LOCALMENTE` por uma password forte.**
O ficheiro é ignorado pelo Git. Não publicar credenciais ou saídas completas
de `docker compose config`, que podem conter a password.

## Arranque

```bash
docker compose config --quiet
docker compose up -d --build
docker compose ps
docker compose exec db pg_isready -U smarttasks -d smarttasks
docker compose exec db psql -U smarttasks -d smarttasks -c '\d tasks'
curl http://localhost:8080/health
```

Aceder a **http://localhost:8080**; documentação da API em
**http://localhost:8080/docs**. Só a porta `127.0.0.1:8080` é publicada.
A porta 5432 da BD é interna à rede padrão do Compose, pelo nome `db`.

O serviço `smarttasks` aguarda o healthcheck da BD. No arranque, a função
`initialize_schema` executa `CREATE TABLE IF NOT EXISTS tasks`: cria a
tabela apenas se faltar, sem apagar registos. **Não é uma ferramenta de
migração de esquemas existentes incompatíveis.** Falhas de ligação ou de
esquema impedem o arranque, sem regressar silenciosamente a memória.

## Contrato preservado

- `GET /`: HTML.
- `GET /api/tasks`: lista JSON.
- `POST /api/tasks`: cria tarefa, HTTP 201.
- `PATCH /api/tasks/{id}/complete`: conclui, HTTP 200.
- `PATCH /api/tasks/{id}/reopen`: reabre, HTTP 200.
- `GET /health`: `{"status":"ok"}`, HTTP 200 (não testa a BD).
- Entradas inválidas: 422; tarefa inexistente: 404; transição repetida: 409.

Os dados e estados persistem depois de reiniciar o serviço FastAPI.

## Testes

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v
```

T-01 a T-13 usam memória isolada ou verificações estáticas. T-14 a T-20
precisam de PostgreSQL e de `TEST_DATABASE_URL` apontando para uma
**base de testes exclusiva**, nunca para a base `smarttasks` de utilização.
O utilizador de testes precisa de permissão para criar e eliminar esquemas.
A fixture cria um esquema aleatório por teste e elimina apenas esse esquema.

```bash
# Exemplo de execução depois de configurar uma BD de testes isolada:
TEST_DATABASE_URL='postgresql://UTILIZADOR:PASSWORD@HOST:5432/BASE_DE_TESTES' \
  python -m pytest -v tests/test_postgres.py
```

A verificação T-18 automatizada usa uma nova instância FastAPI ligada à
mesma BD; **não substitui um reinício real Docker**.

## Validação manual da persistência

1. Abrir http://localhost:8080, criar uma tarefa e concluí-la.
2. Executar `docker compose restart smarttasks`.
3. Atualizar a página: a tarefa deve continuar no estado `Concluída`.
4. Confirmar no PostgreSQL: `docker compose exec db psql -U smarttasks -d smarttasks -c 'SELECT id, title, status FROM tasks ORDER BY id;'`.
5. Reabrir a tarefa e repetir a consulta.

## Diagnóstico e recuperação

```bash
docker compose ps
docker compose logs --tail=100 db
docker compose logs --tail=100 smarttasks
docker compose exec db pg_isready -U smarttasks -d smarttasks
```

- **Password/variável em falta:** verificar `.env`; não colar passwords nos logs ou pedidos de suporte.
- **BD não saudável:** consultar logs, confirmar volume e aguardar o healthcheck.
- **Ligação recusada:** confirmar `DB_HOST=db` e a rede padrão do Compose.
- **Erro de esquema:** consultar logs; não apagar nem recriar tabelas para contornar incompatibilidades. Fazer cópia de segurança e preparar migração explícita.
- **Credenciais alteradas após a primeira inicialização:** o volume mantém as credenciais anteriores; repor a password correta ou alterá-la de forma controlada no PostgreSQL.
- **Recuperação:** corrigir a causa e executar `docker compose up -d --build`, sem eliminar o volume.

Para parar sem apagar dados:

```bash
docker compose down
```

**Não executar `docker compose down -v` como procedimento normal:** elimina
o volume `postgres_data` e os dados guardados. Fazer backup antes de
qualquer operação destrutiva.

## Organização

- `app/main.py`: rotas FastAPI e seleção do armazenamento.
- `app/models.py`: modelos Pydantic.
- `app/service.py`: regras e transições.
- `app/storage.py`: armazenamento em memória e PostgreSQL.
- `app/db.py`: ligação e inicialização não destrutiva.
- `app/static/`: interface HTML/CSS/JavaScript inalterada.
- `tests/test_postgres.py`: T-14 a T-20.
- `docs/`: requisitos, User Stories e rastreabilidade.

Fora do âmbito: autenticação, apagar/editar tarefas, filas, CI/CD, serviços
cloud pagos e migrações complexas.
