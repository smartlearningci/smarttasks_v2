"""Verificações automatizadas simples de estrutura, sem simular Docker real."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_t10_modular_files():
    """T-10 (parcial): estrutura modular presente; esperado módulos separados; RNF-04; US-02/03/04."""
    for path in ['app/main.py', 'app/service.py', 'app/storage.py', 'app/models.py']:
        assert (ROOT / path).is_file()


def test_t12_documentation_present():
    """T-12 (parcial): ficheiros pedagógicos presentes; esperado README e comentários; RNF-06; US-01 a US-07."""
    for path in ['README.md', 'Dockerfile', 'compose.yaml', 'tests/test_api.py']:
        assert (ROOT / path).is_file()
    assert 'RF-01' in (ROOT / 'tests/test_api.py').read_text(encoding='utf-8')


def test_t09_compose_configuration():
    """T-09 (parcial): configuração textual; esperado porta local e serviço único; RNF-01/02; US-07."""
    compose = (ROOT / 'compose.yaml').read_text(encoding='utf-8')
    assert '127.0.0.1:8080:8000' in compose
    assert 'smarttasks:' in compose
