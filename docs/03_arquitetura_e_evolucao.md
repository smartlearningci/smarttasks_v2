# SmartTasks — Arquitetura inicial e evolução

## Arquitetura prevista para o MVP
- **Linguagem/framework:** Python e FastAPI.
- **Interface:** HTML simples servido por `GET /`.
- **API:** `GET /api/tasks`, `POST /api/tasks`, `PATCH /api/tasks/{id}/complete`, `PATCH /api/tasks/{id}/reopen` e `GET /health`.
- **Separação lógica:** camada HTTP/interface → regras de tarefas → armazenamento em memória.
- **Estado:** memória de um único processo da aplicação; sem base de dados nem persistência.
- **Execução prevista:** um container Docker, construído por `Dockerfile` e iniciado por `compose.yaml`.
- **Portas:** `127.0.0.1:8080:8000` (host 8080 → container 8000), para acesso limitado ao computador local.

## Diagrama textual

```text
Browser do formando — http://localhost:8080
                    |
         HTTP (127.0.0.1:8080 -> 8000)
                    v
+-------------------------------------------+
| Docker: um serviço SmartTasks              |
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
|     Armazenamento temporário em memória   |
+-------------------------------------------+
        Dockerfile + compose.yaml
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
app/                 # a implementar
tests/               # a implementar
requirements.txt     # a implementar
Dockerfile           # a implementar
compose.yaml         # a implementar
.dockerignore        # a implementar
```

**Atenção:** nesta fase só existe documentação. Nenhum dos ficheiros de aplicação, testes ou Docker acima foi implementado.

## Princípios para a futura implementação
1. Não alterar os requisitos aprovados sem nova decisão.
2. Identificadores e estados são atribuídos/controlados pelo servidor.
3. Separar rotas, lógica de negócio e armazenamento; comentar decisões menos óbvias.
4. Validar dados e devolver erros claros conforme [02_requisitos_e_mvp.md](02_requisitos_e_mvp.md).
5. Associar testes aos requisitos e User Stories conforme [05_rastreabilidade_e_testes.md](05_rastreabilidade_e_testes.md).
6. Não guardar credenciais no código nem depender de serviços pagos.
7. Não interpretar `GET /health` como observabilidade avançada; apenas confirma resposta da aplicação.

## Evolução possível — não incluída no MVP

| Tema | Possível evolução | Conceito pedagógico |
| --- | --- | --- |
| PostgreSQL | Substituir dados em memória por base de dados | Persistência e separação de responsabilidades |
| Volumes | Guardar dados da base de dados fora do ciclo de vida do container | Persistência em Docker |
| Redes internas | Comunicar entre containers sem expor a base ao host | Redes e isolamento |
| Filas | Processamento assíncrono de tarefas técnicas futuras | Desacoplamento |
| CI/CD | Automatizar testes e construção de imagens | Integração e entrega contínuas |
| Observabilidade | Logs estruturados, métricas e monitorização | Diagnóstico e operação |

Qualquer evolução exige decisão e aprovação próprias.
