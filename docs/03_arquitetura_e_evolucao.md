# SmartTasks — Arquitetura inicial e evolução

## Arquitetura do MVP
- **Linguagem e framework:** Python e FastAPI.
- **Interface:** HTML simples servido pela aplicação.
- **API:** HTTP para operações sobre tarefas e `GET /health`.
- **Estado:** armazenamento em memória do processo da aplicação.
- **Execução:** um container Docker, construído por `Dockerfile` e iniciado por `compose.yaml`.
- **Portas:** `127.0.0.1:8080:8000` (host 8080 → container 8000), para acesso preferencialmente limitado ao computador local.

## Diagrama textual
```text
Browser do formando
http://localhost:8080
         |
         | HTTP (127.0.0.1:8080 -> 8000)
         v
+-----------------------------------+
| Docker: serviço SmartTasks         |
|                                   |
| FastAPI                            |
|  |-- Interface HTML               |
|  |-- API HTTP                     |
|  |-- GET /health                  |
|  |                                |
|  +-- Lógica de tarefas            |
|        |                          |
|        v                          |
|    Dados em memória               |
+-----------------------------------+

Dockerfile + compose.yaml
```

## Organização prevista do repositório
```text
README.md
docs/
  01_contexto_e_personas.md
  02_requisitos_e_mvp.md
  03_arquitetura_e_evolucao.md
app/
tests/
requirements.txt
Dockerfile
compose.yaml
.dockerignore
```
A documentação é a primeira entrega. Os ficheiros de aplicação, testes e Docker serão criados apenas após aprovação específica do plano de implementação.

## Possibilidades de evolução (não incluídas no MVP)
| Tema | Possível evolução | Conceito pedagógico |
| --- | --- | --- |
| PostgreSQL | Substituir dados em memória por base de dados | Persistência e separação de responsabilidades |
| Volumes | Guardar os dados da base de dados fora do ciclo de vida do container | Persistência de dados em Docker |
| Redes internas | Comunicar entre containers de aplicação e base de dados sem expor a base ao host | Redes e isolamento |
| Filas | Introduzir processamento assíncrono em tarefas técnicas futuras | Desacoplamento e processamento assíncrono |
| CI/CD | Automatizar testes e construção de imagens | Integração e entrega contínuas |
| Observabilidade | Adicionar logs estruturados, métricas e monitorização | Diagnóstico e operação |

## Princípios de implementação futura
Manter módulos claros, testes associados aos requisitos e ficheiros de configuração explicados para fins didáticos. Não guardar credenciais no código e não depender de serviços pagos. Qualquer evolução exige nova decisão e aprovação.
