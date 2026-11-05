"""Testes API. Cada teste identifica objetivo, pré-condições, esperado, RF/RNF e US."""
import pytest


def create(client, title="Preparar relatório", description=None):
    return client.post('/api/tasks', json={'title': title, 'description': description})


def test_t01_empty_list(client):
    """T-01: sem tarefas; GET lista e HTML; esperado 200/[] e interface; RF-01, RF-05, RNF-03; US-01, US-05."""
    response = client.get('/api/tasks')
    assert response.status_code == 200 and response.json() == []
    page = client.get('/')
    assert page.status_code == 200 and 'SmartTasks' in page.text


def test_t02_create(client):
    """T-02: lista vazia; POST válido sem descrição; esperado 201, ID, Aberta e listagem; RF-01/02/05; US-01/02."""
    response = create(client, '  Preparar relatório  ')
    assert response.status_code == 201
    assert response.json() == {'id': 1, 'title': 'Preparar relatório', 'description': None, 'status': 'Aberta'}
    assert client.get('/api/tasks').json() == [response.json()]
    assert create(client, 'Outra').json()['id'] == 2


@pytest.mark.parametrize('payload', [{}, {'title': ''}, {'title': '   '}, {'title': 123},
                                    {'title': 'Válida', 'description': 123}, {'title': 'Válida', 'status': 'Concluída'},
                                    {'title': 'Válida', 'id': 8}])
def test_t03_invalid_creation(client, payload):
    """T-03: lista vazia; POST inválido; esperado 422/detail e sem alterações; RF-02/05; US-02."""
    response = client.post('/api/tasks', json=payload)
    assert response.status_code == 422
    assert response.json().get('detail')
    assert client.get('/api/tasks').json() == []


def test_t03_malformed_json(client):
    """T-03: JSON malformado; esperado 422/detail e sem tarefas; RF-02/05; US-02."""
    response = client.post('/api/tasks', content='{', headers={'Content-Type': 'application/json'})
    assert response.status_code == 422 and response.json().get('detail')
    assert client.get('/api/tasks').json() == []


def test_t04_complete(client):
    """T-04: tarefa Aberta; PATCH complete; esperado 200/Concluída na lista; RF-01/03/05; US-03/05."""
    task_id = create(client).json()['id']
    response = client.patch(f'/api/tasks/{task_id}/complete')
    assert response.status_code == 200 and response.json()['status'] == 'Concluída'
    assert client.get('/api/tasks').json()[0]['status'] == 'Concluída'


def test_t05_reopen(client):
    """T-05: tarefa Concluída; PATCH reopen; esperado 200/Aberta na lista; RF-01/04/05; US-04/05."""
    task_id = create(client).json()['id']
    client.patch(f'/api/tasks/{task_id}/complete')
    response = client.patch(f'/api/tasks/{task_id}/reopen')
    assert response.status_code == 200 and response.json()['status'] == 'Aberta'
    assert client.get('/api/tasks').json()[0]['status'] == 'Aberta'


@pytest.mark.parametrize('action', ['complete', 'reopen'])
@pytest.mark.parametrize('identifier,expected', [('999', 404), ('0', 422), ('-1', 422), ('abc', 422)])
def test_t06_invalid_id(client, action, identifier, expected):
    """T-06: ID ausente/inválido; PATCH; esperado 404 ou 422 sem alteração; RF-03/04/05; US-03/04."""
    response = client.patch(f'/api/tasks/{identifier}/{action}')
    assert response.status_code == expected and response.json().get('detail')
    assert client.get('/api/tasks').json() == []


def test_t07_repeated_transitions(client):
    """T-07: tarefa em estado destino; PATCH repetido; esperado 409 e estado intacto; RF-03/04/05; US-03/04."""
    task_id = create(client).json()['id']
    assert client.patch(f'/api/tasks/{task_id}/reopen').status_code == 409
    assert client.get('/api/tasks').json()[0]['status'] == 'Aberta'
    assert client.patch(f'/api/tasks/{task_id}/complete').status_code == 200
    conflict = client.patch(f'/api/tasks/{task_id}/complete')
    assert conflict.status_code == 409 and conflict.json().get('detail')
    assert client.get('/api/tasks').json()[0]['status'] == 'Concluída'


def test_t08_health(client):
    """T-08: serviço ativo; GET /health; esperado 200/status ok; RF-06; US-06."""
    response = client.get('/health')
    assert response.status_code == 200 and response.json() == {'status': 'ok'}


def test_t11_process_memory(client):
    """T-11 (parcial): mesma instância retém dados; nova instância começa vazia; RNF-05; US-01/02/07."""
    create(client)
    assert len(client.get('/api/tasks').json()) == 1
    from fastapi.testclient import TestClient
    from app.main import create_app
    with TestClient(create_app()) as fresh:
        assert fresh.get('/api/tasks').json() == []
