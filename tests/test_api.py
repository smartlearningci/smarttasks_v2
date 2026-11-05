# Testes HTTP: cada função corresponde a um caso T-xx da matriz aprovada.
# A fixture client cria uma aplicação nova para não partilhar tarefas.
"""Testes API. Cada teste identifica objetivo, pré-condições, esperado, RF/RNF e US."""
import pytest


def create(client, title="Preparar relatório", description=None):
    return client.post('/api/tasks', json={'title': title, 'description': description})


def test_t01_empty_list(client):
    """Objetivo: verificar 200, [] e página HTML.

    Requisitos: RF-01, RF-05, RNF-03.
    User Stories: US-01, US-05.
    Pré-condições: Lista vazia.
    Ação: GET lista e interface.
    Resultado esperado: 200, [] e página HTML.
    """
    response = client.get('/api/tasks')
    assert response.status_code == 200 and response.json() == []
    page = client.get('/')
    assert page.status_code == 200 and 'SmartTasks' in page.text


def test_t02_create(client):
    """Objetivo: verificar 201, ID único, título limpo e estado Aberta.

    Requisitos: RF-01, RF-02, RF-05.
    User Stories: US-01, US-02.
    Pré-condições: Lista vazia.
    Ação: POST válido, consulta e segundo POST.
    Resultado esperado: 201, ID único, título limpo e estado Aberta.
    """
    response = create(client, '  Preparar relatório  ')
    assert response.status_code == 201
    assert response.json() == {'id': 1, 'title': 'Preparar relatório', 'description': None, 'status': 'Aberta'}
    assert client.get('/api/tasks').json() == [response.json()]
    assert create(client, 'Outra').json()['id'] == 2


@pytest.mark.parametrize('payload', [{}, {'title': ''}, {'title': '   '}, {'title': 123},
                                    {'title': 'Válida', 'description': 123}, {'title': 'Válida', 'status': 'Concluída'},
                                    {'title': 'Válida', 'id': 8}])
def test_t03_invalid_creation(client, payload):
    """Objetivo: verificar 422/detail e lista inalterada.

    Requisitos: RF-02, RF-05.
    User Stories: US-02.
    Pré-condições: Lista vazia.
    Ação: POST com entradas inválidas parametrizadas.
    Resultado esperado: 422/detail e lista inalterada.
    """
    response = client.post('/api/tasks', json=payload)
    assert response.status_code == 422
    assert response.json().get('detail')
    assert client.get('/api/tasks').json() == []


def test_t03_malformed_json(client):
    """Objetivo: verificar 422/detail e lista inalterada.

    Requisitos: RF-02, RF-05.
    User Stories: US-02.
    Pré-condições: Lista vazia.
    Ação: POST com JSON malformado.
    Resultado esperado: 422/detail e lista inalterada.
    """
    response = client.post('/api/tasks', content='{', headers={'Content-Type': 'application/json'})
    assert response.status_code == 422 and response.json().get('detail')
    assert client.get('/api/tasks').json() == []


def test_t04_complete(client):
    """Objetivo: verificar 200 e estado Concluída.

    Requisitos: RF-01, RF-03, RF-05.
    User Stories: US-03, US-05.
    Pré-condições: Tarefa Aberta.
    Ação: PATCH complete e GET lista.
    Resultado esperado: 200 e estado Concluída.
    """
    task_id = create(client).json()['id']
    response = client.patch(f'/api/tasks/{task_id}/complete')
    assert response.status_code == 200 and response.json()['status'] == 'Concluída'
    assert client.get('/api/tasks').json()[0]['status'] == 'Concluída'


def test_t05_reopen(client):
    """Objetivo: verificar 200 e estado Aberta.

    Requisitos: RF-01, RF-04, RF-05.
    User Stories: US-04, US-05.
    Pré-condições: Tarefa Concluída.
    Ação: PATCH reopen e GET lista.
    Resultado esperado: 200 e estado Aberta.
    """
    task_id = create(client).json()['id']
    client.patch(f'/api/tasks/{task_id}/complete')
    response = client.patch(f'/api/tasks/{task_id}/reopen')
    assert response.status_code == 200 and response.json()['status'] == 'Aberta'
    assert client.get('/api/tasks').json()[0]['status'] == 'Aberta'


@pytest.mark.parametrize('action', ['complete', 'reopen'])
@pytest.mark.parametrize('identifier,expected', [('999', 404), ('0', 422), ('-1', 422), ('abc', 422)])
def test_t06_invalid_id(client, action, identifier, expected):
    """Objetivo: verificar 422 ou 404; lista inalterada.

    Requisitos: RF-03, RF-04, RF-05.
    User Stories: US-03, US-04.
    Pré-condições: Sem tarefas.
    Ação: PATCH com ID inválido ou inexistente.
    Resultado esperado: 422 ou 404; lista inalterada.
    """
    response = client.patch(f'/api/tasks/{identifier}/{action}')
    assert response.status_code == expected and response.json().get('detail')
    assert client.get('/api/tasks').json() == []


def test_t07_repeated_transitions(client):
    """Objetivo: verificar 409; estado inalterado.

    Requisitos: RF-03, RF-04, RF-05.
    User Stories: US-03, US-04.
    Pré-condições: Tarefa existente.
    Ação: Reabrir Aberta e concluir Concluída.
    Resultado esperado: 409; estado inalterado.
    """
    task_id = create(client).json()['id']
    assert client.patch(f'/api/tasks/{task_id}/reopen').status_code == 409
    assert client.get('/api/tasks').json()[0]['status'] == 'Aberta'
    assert client.patch(f'/api/tasks/{task_id}/complete').status_code == 200
    conflict = client.patch(f'/api/tasks/{task_id}/complete')
    assert conflict.status_code == 409 and conflict.json().get('detail')
    assert client.get('/api/tasks').json()[0]['status'] == 'Concluída'


def test_t08_health(client):
    """Objetivo: verificar 200 e status ok.

    Requisitos: RF-06.
    User Stories: US-06.
    Pré-condições: Aplicação ativa.
    Ação: GET health.
    Resultado esperado: 200 e status ok.
    """
    response = client.get('/health')
    assert response.status_code == 200 and response.json() == {'status': 'ok'}


def test_t11_process_memory(client):
    """Objetivo: verificar Dados na primeira; segunda vazia; não testa Docker.

    Requisitos: RNF-05.
    User Stories: US-01, US-02, US-07.
    Pré-condições: Instância com tarefa.
    Ação: Consultar e criar instância independente.
    Resultado esperado: Dados na primeira; segunda vazia; não testa Docker.
    """
    create(client)
    assert len(client.get('/api/tasks').json()) == 1
    from fastapi.testclient import TestClient
    from app.main import create_app
    with TestClient(create_app()) as fresh:
        assert fresh.get('/api/tasks').json() == []
