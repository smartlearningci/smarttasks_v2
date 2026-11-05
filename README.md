# SmartTasks — MVP pedagógico

Aplicação local de gestão de tarefas da empresa fictícia TaskFlow. Permite **listar, criar, concluir e reabrir** tarefas. Estados: **Aberta** e **Concluída**. Sem login. As tarefas continuam exclusivamente na memória do processo FastAPI. Existe também um container PostgreSQL para demonstração, ainda sem ligação à aplicação.

## Requisitos prévios

- Git e Docker com suporte a `docker compose` (para execução em container).
- Python 3.12 e pip (apenas se pretender correr testes localmente sem Docker).

## Clonar

```bash
git clone https://github.com/smartlearningci/smarttasks_v2.git
cd smarttasks_v2
```

## Build e arranque

Antes do primeiro arranque, criar a configuração local a partir do exemplo:

```bash
cp .env.example .env
```

**Editar o ficheiro `.env` e substituir `SUBSTITUIR_LOCALMENTE` por uma password forte.** O ficheiro `.env` está excluído do Git e nunca deve ser publicado. A variável `POSTGRES_PASSWORD` é necessária para o PostgreSQL; a aplicação SmartTasks não a utiliza nesta fase.

Validar a configuração e construir/iniciar os dois serviços:

```bash
docker compose config --quiet
docker compose build
docker compose up -d
```

Os serviços `smarttasks` e `db` partilham automaticamente a rede padrão do Compose. O nome interno do PostgreSQL é `db` e a porta interna é `5432`; **não existe publicação da porta 5432 no host**. A aplicação continua disponível apenas em `127.0.0.1:8080`, sem estabelecer ligação à base de dados.

Abrir **http://localhost:8080**. A documentação interativa da API está em **http://localhost:8080/docs** e a verificação de saúde em **http://localhost:8080/health**. A porta 8080 está associada apenas a `127.0.0.1` no computador local.

Ver estado e logs:

```bash
docker compose ps
docker compose logs --tail=50 smarttasks db
docker compose exec db pg_isready -U smarttasks -d smarttasks
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

**Importante:** atualizar a página não apaga as tarefas enquanto o processo continua ativo. Reiniciar/recriar o processo FastAPI perde todas as tarefas, porque continuam em memória. A aplicação usa um único processo Uvicorn.

O volume nomeado `postgres_data` persiste os **dados do PostgreSQL**, não as tarefas SmartTasks. `docker compose down` para os serviços sem eliminar o volume. **`docker compose down -v` elimina também o volume e os dados da base de dados**; usar apenas quando se pretende essa eliminação.

## Organização

- `app/main.py`: rotas FastAPI e interface HTML.
- `app/models.py`: modelos e validações Pydantic.
- `app/service.py`: regras de negócio.
- `app/storage.py`: armazenamento em memória.
- `app/static/`: HTML, JavaScript e CSS sem serviços externos.
- `tests/`: testes API e verificações estruturais.
- `Dockerfile`, `compose.yaml`, `.dockerignore`: execução Docker e configuração dos serviços.\n- `.env.example`, `.gitignore`: exemplo de variável de ambiente e exclusão de credenciais locais.
- `docs/`: requisitos, User Stories e rastreabilidade aprovados.

## Limites do MVP

PostgreSQL existe apenas como serviço de demonstração no Compose, **sem integração com as tarefas**. Continuam fora do âmbito: autenticação, edição/remoção de tarefas, atribuições, filas, CI/CD, observabilidade avançada e serviços externos. Não incluir credenciais no repositório.
