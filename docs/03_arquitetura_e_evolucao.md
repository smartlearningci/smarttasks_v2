# SmartTasks — Arquitetura inicial e evolução

## Arquitetura prevista para o MVP
- **Linguagem/framework:** Python e FastAPI.
- **Interface:** HTML simples servido por `GET /`.
- **API:** `GET /api/tasks`, `POST /api/tasks`, `PATCH /api/tasks/{id}/complete`, `PATCH /api/tasks/{id}/reopen` e `GET /health`.
- **Separação lógica:** camada HTTP/interface → regras de tarefas → armazenamento PostgreSQL (memória apenas nos testes isolados).
- **Estado:** PostgreSQL 17 com volume nomeado postgres_data; tarefas persistentes.
- **Execução prevista:** dois serviços Docker Compose, smarttasks e db, na rede padrão.
- **Portas:** `127.0.0.1:8080:8000` (host 8080 → container 8000), para acesso limitado ao computador local.

## Diagrama textual

```text
Browser do formando — http://localhost:8080
                    |
         HTTP (127.0.0.1:8080 -> 8000)
                    v
+-------------------------------------------+
| Docker: serviço SmartTasks              |
|                                           |
| FastAPI — interface HTML e rotas HTTP      |
|  |-- GET /                                |
|  |-- GET/POST /api/tasks                  |
|  |-- PATCH /api/tasks/{id}/complete       |
|  |-- PATCH /api/tasks/{id}/reopen         |
|  |-- GET /health                          |
|               |                           |
|               v                           |
|     Regras de tarefas e validações        |
|               |                           |
|               v                           |
|     PostgresTaskStore -> db:5432   |
+-------------------------------------------+
        db -> volume postgres_data\n        Dockerfile + compose.yaml
```

## Organização prevista

```text
README.md
docs/
  01_contexto_e_personas.md
  02_requisitos_e_mvp.md
  03_arquitetura_e_evolucao.md
  04_user_stories.md
  05_rastreabilidade_e_testes.md
app/                 # implementação FastAPI e armazenamento
tests/               # testes HTTP e PostgreSQL
requirements.txt     # dependências fixadas
Dockerfile           # imagem FastAPI
compose.yaml         # dois serviços
.dockerignore        # exclusões de build
```

**Estado atual:** aplicação implementada; PostgreSQL integrado na camada de armazenamento e inicialização não destrutiva da tabela no arranque.

## Princípios para a futura implementação
1. Não alterar os requisitos aprovados sem nova decisão.
2. Identificadores e estados são atribuídos/controlados pelo servidor.
3. Separar rotas, lógica de negócio e armazenamento; comentar decisões menos óbvias.
4. Validar dados e devolver erros claros conforme [02_requisitos_e_mvp.md](02_requisitos_e_mvp.md).
5. Associar testes aos requisitos e User Stories conforme [05_rastreabilidade_e_testes.md](05_rastreabilidade_e_testes.md).
6. Não guardar credenciais no código nem depender de serviços pagos.
7. Não interpretar `GET /health` como observabilidade avançada; apenas confirma resposta da aplicação.

## Outras evoluções possíveis — não incluídas nesta etapa

| Tema | Possível evolução | Conceito pedagógico |
| --- | --- | --- |
| PostgreSQL | Implementado nesta evolução | Persistência e separação de responsabilidades |
| Volumes | Volume postgres_data implementado | Persistência em Docker |
| Redes internas | Rede padrão do Compose implementada | Redes e isolamento |
| Filas | Processamento assíncrono de tarefas técnicas futuras | Desacoplamento |
| CI/CD | Automatizar testes e construção de imagens | Integração e entrega contínuas |
| Observabilidade | Logs estruturados, métricas e monitorização | Diagnóstico e operação |

Qualquer evolução exige decisão e aprovação próprias.
