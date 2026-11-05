# SmartTasks — Matriz de rastreabilidade e catálogo de testes

## Objetivo e estado

Esta é a matriz de **especificação** do primeiro MVP: associa os doze requisitos RF/RNF às sete User Stories e a testes previstos. **Ainda não existem testes executáveis nem resultados de execução**; os IDs T-01 a T-13 indicam casos a implementar ou verificar após aprovação da implementação.

Uma ligação a US representa contribuição para um percurso de utilizador; os requisitos técnicos transversais exigem também testes próprios. A matriz abaixo cobre explicitamente todos os requisitos aprovados.

## Matriz RF/RNF ↔ User Stories ↔ Testes

| Requisito | User Stories relacionadas | Testes previstos | Evidência necessária |
| --- | --- | --- | --- |
| RF-01 — Listar tarefas | US-01, US-05 | T-01, T-02, T-04, T-05 | Lista vazia válida e estados corretos |
| RF-02 — Criar tarefa | US-02 | T-02, T-03 | Criada com ID, título e estado corretos; inválida rejeitada |
| RF-03 — Concluir | US-03, US-05 | T-04, T-06, T-07 | Transição, inexistente e conflito |
| RF-04 — Reabrir | US-04, US-05 | T-05, T-06, T-07 | Transição, inexistente e conflito |
| RF-05 — API HTTP | US-01, US-02, US-03, US-04, US-05 | T-01, T-02, T-03, T-04, T-05, T-06, T-07 | Métodos, rotas, modelos, estados HTTP e erros |
| RF-06 — Saúde | US-06 | T-08 | 200 e corpo `{"status":"ok"}` |
| RNF-01 — Acesso local | US-01, US-05, US-07 | T-09 | HTML disponível em localhost:8080 |
| RNF-02 — Docker | US-07 | T-09 | Dockerfile, Compose, um serviço e portas corretas |
| RNF-03 — Simplicidade | US-01, US-02, US-03, US-04, US-05 | T-01, T-13 | Interface compreensível, sem login, com operações básicas |
| RNF-04 — Modularidade | US-02, US-03, US-04 (suporte técnico) | T-10 | Inspeção da separação rotas/regras/armazenamento |
| RNF-05 — Dados temporários | US-01, US-02, US-07 (comportamento operacional) | T-11 | Dados mantidos durante execução; perdidos após reiniciar processo |
| RNF-06 — Clareza pedagógica | US-07 (documentação de operação); US-01 a US-06 (código/testes correspondentes) | T-12 | Inspeção objetiva de comentários, README e descrições de testes |

**Cobertura planeada:** 6/6 RF, 6/6 RNF e 7/7 US possuem pelo menos um teste/associação. Esta cobertura é documental, **não significa testes implementados ou aprovados em execução**.

## Matriz inversa — User Stories ↔ Requisitos e testes

| User Story | Requisitos principais | Testes previstos |
| --- | --- | --- |
| US-01 | RF-01, RF-05, RNF-03 | T-01, T-13 |
| US-02 | RF-02, RF-05, RNF-03 | T-02, T-03, T-13 |
| US-03 | RF-03, RF-05 | T-04, T-06, T-07 |
| US-04 | RF-04, RF-05 | T-05, T-06, T-07 |
| US-05 | RF-01, RF-03, RF-04, RNF-03 | T-01, T-04, T-05, T-13 |
| US-06 | RF-06 | T-08 |
| US-07 | RNF-01, RNF-02, RNF-05, RNF-06 | T-09, T-11, T-12 |

RNF-04 e RNF-06 são também verificações de qualidade da implementação inteira, independentemente de uma US individual.

## Catálogo de testes previstos

Os casos seguintes especificam **objetivo, pré-condições, ação, resultado esperado e rastreabilidade**; nenhuma linha representa execução real.

| ID | Objetivo | Pré-condições | Ação / entrada | Resultado esperado | RF/RNF | US |
| --- | --- | --- | --- | --- | --- | --- |
| T-01 | Listar sem tarefas | Processo iniciado, lista vazia | `GET /api/tasks`; abrir interface | HTTP 200 e `[]`; HTML indica ausência de tarefas | RF-01, RF-05, RNF-03 | US-01, US-05 |
| T-02 | Criar tarefa válida | Serviço ativo | `POST /api/tasks` com título válido, sem descrição; listar | HTTP 201; ID positivo, descrição `null`, estado `Aberta`; tarefa na lista | RF-01, RF-02, RF-05 | US-01, US-02 |
| T-03 | Validar criação inválida | Serviço ativo | Criar sem título, com título `""`, `"   "` e tipos incorretos (casos parametrizados) | HTTP 422 com `detail` compreensível; nenhuma tarefa criada | RF-02, RF-05 | US-02 |
| T-04 | Concluir tarefa | Uma tarefa `Aberta` existente | `PATCH /api/tasks/{id}/complete`; listar | HTTP 200, estado `Concluída` na resposta e na lista | RF-01, RF-03, RF-05 | US-03, US-05 |
| T-05 | Reabrir tarefa | Uma tarefa `Concluída` existente | `PATCH /api/tasks/{id}/reopen`; listar | HTTP 200, estado `Aberta` na resposta e na lista | RF-01, RF-04, RF-05 | US-04, US-05 |
| T-06 | Rejeitar ID inexistente/inválido | Serviço ativo; ID válido mas inexistente | Concluir e reabrir ID inexistente; testar ID não positivo ou não inteiro em separado | 404 para inexistente; 422 para ID inválido; sem alteração de dados | RF-03, RF-04, RF-05 | US-03, US-04 |
| T-07 | Rejeitar transições repetidas | Uma tarefa concluída e outra aberta | Concluir a já concluída; reabrir a já aberta | HTTP 409 com `detail`; estados inalterados | RF-03, RF-04, RF-05 | US-03, US-04 |
| T-08 | Verificar saúde HTTP | Serviço ativo | `GET /health` | HTTP 200 e `{"status":"ok"}` | RF-06 | US-06 |
| T-09 | Validar execução local e Docker | Docker instalado e ficheiros Docker presentes | Construir/iniciar Compose; visitar `http://localhost:8080` | Um serviço, porta `127.0.0.1:8080:8000`, HTML responde e instruções reprodutíveis | RNF-01, RNF-02 | US-07 |
| T-10 | Inspecionar modularidade | Código implementado | Rever módulos e dependências | Rotas isoladas das regras de tarefa e do armazenamento; estrutura explicada | RNF-04 | US-02, US-03, US-04 |
| T-11 | Verificar volatilidade dos dados | Tarefa criada; processo ativo | Consultar repetidamente e atualizar browser; reiniciar/recriar processo; listar novamente | Tarefa persiste durante o mesmo processo; após reinício/recriação lista inicia vazia | RNF-05 | US-01, US-02, US-07 |
| T-12 | Verificar documentação pedagógica | Código, testes, Dockerfile, Compose e README disponíveis | Inspecionar código e documentação | Comentários úteis; cada teste com ID, objetivo, pré-condições, ação, esperado, RF/RNF e US; README explica executar/testar | RNF-06 | US-01 a US-07 |
| T-13 | Verificar interface utilizável sem autenticação | Serviço ativo | Abrir HTML; listar, criar, concluir e reabrir via interface sem login | Operações identificáveis, feedback visível, sem autenticação nem perfis de acesso | RNF-03 | US-01, US-02, US-03, US-04, US-05 |

### Critérios para o futuro relatório de testes

Cada teste implementado ou executado deve registar: ID, objetivo, requisitos, User Stories, pré-condições, entradas/ação, resultado esperado, resultado observado e estado (`Passou`, `Falhou` ou `Não executado`). O relatório global deve contabilizar totais por estado, destacar falhas de forma acessível (texto e, opcionalmente, cores) e identificar requisitos sem cobertura.

Para verificações de inspeção manual (por exemplo, modularidade e clareza pedagógica), registar os ficheiros analisados e as evidências concretas; não apresentar inspeções previstas como testes automatizados.

## Limites e lacunas residuais

- Não foram identificados requisitos aprovados sem associação a testes previstos.
- Cobertura por matriz não garante cobertura real: exige código, testes e execução futura.
- Desempenho, segurança de produção, durabilidade de dados, controlo de concorrência e acessibilidade avançada não são objetivos do primeiro MVP. A ausência de testes desses aspetos não deve ser apresentada como falha face ao âmbito aprovado.
- Qualquer alteração aos requisitos, estados, endpoints ou critérios de aceitação depende de aprovação adicional.
