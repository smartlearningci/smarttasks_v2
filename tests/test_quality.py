# Verificações estáticas: não equivalem a construir Docker ou abrir browser.
"""Verificações automatizadas simples de estrutura, sem simular Docker real."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_t10_modular_files():
    """Verificação parcial: Módulos presentes; arquitetura exige revisão manual.\n\n    Requisitos: RNF-04.\n    User Stories: US-02, US-03, US-04.\n    Pré-condições: Código presente.\n    Ação: Inspecionar existência dos módulos.\n    Resultado esperado: Módulos presentes; arquitetura exige revisão manual.\n    """
    for path in ['app/main.py', 'app/service.py', 'app/storage.py', 'app/models.py']:
        assert (ROOT / path).is_file()


def test_t12_documentation_present():
    """Verificação parcial: Ficheiros presentes; qualidade dos comentários exige leitura.\n\n    Requisitos: RNF-06.\n    User Stories: US-01 a US-07.\n    Pré-condições: Ficheiros presentes.\n    Ação: Inspecionar documentação e referências.\n    Resultado esperado: Ficheiros presentes; qualidade dos comentários exige leitura.\n    """
    for path in ['README.md', 'Dockerfile', 'compose.yaml', 'tests/test_api.py']:
        assert (ROOT / path).is_file()
    assert 'RF-01' in (ROOT / 'tests/test_api.py').read_text(encoding='utf-8')


def test_t09_compose_configuration():
    """Verificação parcial: Porta e serviço definidos; Docker não executado.\n\n    Requisitos: RNF-01, RNF-02.\n    User Stories: US-07.\n    Pré-condições: Compose presente.\n    Ação: Verificar texto da configuração.\n    Resultado esperado: Porta e serviço definidos; Docker não executado.\n    """
    compose = (ROOT / 'compose.yaml').read_text(encoding='utf-8')
    assert '127.0.0.1:8080:8000' in compose
    assert 'smarttasks:' in compose
