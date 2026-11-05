"""T-14 a T-20: testes PostgreSQL com esquemas isolados.

TEST_DATABASE_URL deve apontar EXCLUSIVAMENTE para uma BD de testes.
A fixture cria e remove somente um esquema aleatório test_smarttasks_*.
Sem driver/servidor, os testes são ignorados, não simulados.
"""
import os
import uuid

import pytest
from fastapi.testclient import TestClient

from app.db import initialize_schema
from app.main import create_app
from app.storage import PostgresTaskStore


@pytest.fixture
def postgres_store():
    """Isola os testes e nunca apaga a tabela de tarefas da aplicação."""
    psycopg = pytest.importorskip("psycopg", reason="Driver psycopg não instalado")
    dsn = os.environ.get("TEST_DATABASE_URL")
    if not dsn:
        pytest.skip("TEST_DATABASE_URL não definida")
    from psycopg import sql

    schema = "test_smarttasks_" + uuid.uuid4().hex
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))
    kwargs = {"conninfo": dsn, "options": f"-c search_path={schema}"}
    try:
        initialize_schema(kwargs)
        yield PostgresTaskStore(kwargs)
    finally:
        # Limpa apenas o esquema único criado por este teste.
        with psycopg.connect(dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))


@pytest.fixture
def pg_client(postgres_store):
    with TestClient(create_app(store=postgres_store)) as client:
        yield client


def test_t14_create_persisted(pg_client, postgres_store):
    """T-14 | RF-02, RF-05 | US-02.
    Objetivo: criar; pré-condição: tabela vazia; ação: POST válido.
    Esperado: 201 e linha persistida com ID positivo e estado Aberta.
    """
    response = pg_client.post("/api/tasks", json={"title": "Relatório"})
    assert response.status_code == 201
    task = response.json()
    assert task["id"] > 0 and task["status"] == "Aberta"
    assert postgres_store.get(task["id"]).title == "Relatório"


def test_t15_list_persisted(pg_client):
    """T-15 | RF-01, RF-05 | US-01, US-05.
    Objetivo: listar; pré-condição: duas tarefas; ação: GET.
    Esperado: 200 e tarefas ordenadas por ID.
    """
    for title in ("Primeira", "Segunda"):
        assert pg_client.post("/api/tasks", json={"title": title}).status_code == 201
    response = pg_client.get("/api/tasks")
    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["Primeira", "Segunda"]


def test_t16_complete_persisted(pg_client, postgres_store):
    """T-16 | RF-03, RF-05 | US-03, US-05.
    Objetivo: concluir; pré-condição: Aberta; ação: PATCH complete.
    Esperado: 200 e estado Concluída gravado na BD.
    """
    task_id = pg_client.post("/api/tasks", json={"title": "Teste"}).json()["id"]
    assert pg_client.patch(f"/api/tasks/{task_id}/complete").status_code == 200
    assert postgres_store.get(task_id).status == "Concluída"


def test_t17_reopen_persisted(pg_client, postgres_store):
    """T-17 | RF-04, RF-05 | US-04, US-05.
    Objetivo: reabrir; pré-condição: Concluída; ação: PATCH reopen.
    Esperado: 200 e estado Aberta gravado na BD.
    """
    task_id = pg_client.post("/api/tasks", json={"title": "Teste"}).json()["id"]
    pg_client.patch(f"/api/tasks/{task_id}/complete")
    assert pg_client.patch(f"/api/tasks/{task_id}/reopen").status_code == 200
    assert postgres_store.get(task_id).status == "Aberta"


def test_t18_new_app_same_database(pg_client, postgres_store):
    """T-18 (parcial) | RNF-05 | US-01, US-07.
    Objetivo: persistência; ação: criar e abrir outra instância FastAPI.
    Esperado: tarefa presente; reinício Docker requer teste manual.
    """
    task_id = pg_client.post("/api/tasks", json={"title": "Persistente"}).json()["id"]
    with TestClient(create_app(store=PostgresTaskStore(postgres_store.connect_kwargs))) as fresh:
        assert any(t["id"] == task_id for t in fresh.get("/api/tasks").json())


def test_t19_duplicate_transition(pg_client, postgres_store):
    """T-19 | RF-03, RF-04, RF-05 | US-03, US-04.
    Objetivo: recusar transição repetida; ação: concluir duas vezes.
    Esperado: HTTP 409 e estado Concluída inalterado.
    """
    task_id = pg_client.post("/api/tasks", json={"title": "Teste"}).json()["id"]
    assert pg_client.patch(f"/api/tasks/{task_id}/complete").status_code == 200
    assert pg_client.patch(f"/api/tasks/{task_id}/complete").status_code == 409
    assert postgres_store.get(task_id).status == "Concluída"


def test_t20_schema_idempotent(pg_client, postgres_store):
    """T-20 | RNF-05 | US-07.
    Objetivo: inicialização não destrutiva; ação: repetir CREATE TABLE.
    Esperado: tarefa e ID preservados.
    """
    task_id = pg_client.post("/api/tasks", json={"title": "Conservar"}).json()["id"]
    initialize_schema(postgres_store.connect_kwargs)
    assert postgres_store.get(task_id).title == "Conservar"
