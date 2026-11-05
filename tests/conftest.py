"""Isolamento: cada teste recebe uma aplicação com armazenamento vazio."""
import pytest
from fastapi.testclient import TestClient
from app.main import create_app

@pytest.fixture
def client():
    with TestClient(create_app()) as api:
        yield api
