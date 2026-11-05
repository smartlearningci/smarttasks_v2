# SmartTasks — Requisitos e MVP

## Objetivo e âmbito
Centralizar tarefas internas da TaskFlow numa aplicação pedagógica local, com interface HTML simples e API HTTP. Existem apenas os estados **Aberta** e **Concluída**. Qualquer pessoa com acesso à interface local pode realizar as mesmas operações; as personas não implicam perfis de acesso.

As User Stories constam de [04_user_stories.md](04_user_stories.md). A correspondência requisitos ↔ User Stories ↔ testes consta de [05_rastreabilidade_e_testes.md](05_rastreabilidade_e_testes.md).

## Requisitos funcionais e critérios de aceitação

| ID | Requisito | Critério de aceitação |
| --- | --- | --- |
| RF-01 | Listar tarefas | `GET /api/tasks` devolve HTTP 200 com uma lista de tarefas e estados; quando vazia, devolve `[]`; a interface mostra uma mensagem apropriada. |
| RF-02 | Criar tarefa | `POST /api/tasks` exige título com conteúdo após remoção de espaços nas extremidades, aceita descrição opcional e devolve HTTP 201; a tarefa recebe ID único e estado **Aberta** e aparece na lista. Título ausente, vazio ou apenas espaços é rejeitado com HTTP 422. |
| RF-03 | Concluir tarefa | `PATCH /api/tasks/{id}/complete` muda uma tarefa **Aberta** para **Concluída** e devolve HTTP 200; ID inexistente devolve 404 e conclusão repetida devolve 409. |
| RF-04 | Reabrir tarefa | `PATCH /api/tasks/{id}/reopen` muda uma tarefa **Concluída** para **Aberta** e devolve HTTP 200; ID inexistente devolve 404 e reabertura de tarefa já aberta devolve 409. |
| RF-05 | Disponibilizar API HTTP | Listar, criar, concluir e reabrir usam os endpoints e modelos abaixo; erros previsíveis devolvem JSON compreensível com códigos HTTP coerentes (422, 404 e 409). |
| RF-06 | Verificar saúde | `GET /health` devolve HTTP 200 e `{"status":"ok"}` quando a aplicação responde. Isto não prova a saúde de serviços externos nem a persistência. |

## Modelo de dados mínimo

| Campo | Tipo | Regra |
| --- | --- | --- |
| `id` | inteiro | Gerado pelo servidor, único dentro da execução, positivo. |
| `title` | texto | Obrigatório; remover espaços iniciais/finais; rejeitar vazio após limpeza. |
| `description` | texto ou `null` | Opcional; ausente é interpretado como `null`. |
| `status` | texto | Apenas `Aberta` ou `Concluída`; nova tarefa começa em `Aberta`. |

A criação aceita exclusivamente os campos `title` e `description` como dados de negócio. `id` e `status` são controlados pelo servidor. O cliente não escolhe o estado inicial nem o identificador.

Exemplo de criação: `{"title":"Preparar relatório","description":"Recolher dados da equipa"}`.

Exemplo de tarefa devolvida: `{"id":1,"title":"Preparar relatório","description":"Recolher dados da equipa","status":"Aberta"}`.

## Contrato HTTP do MVP

| Método e rota | Pedido | Resposta de sucesso |
| --- | --- | --- |
| `GET /` | Sem corpo | 200: interface HTML utilizável. |
| `GET /api/tasks` | Sem corpo | 200: array JSON de tarefas (pode ser vazio). |
| `POST /api/tasks` | JSON com `title` e `description` opcional | 201: JSON da tarefa criada. |
| `PATCH /api/tasks/{id}/complete` | ID inteiro positivo, sem corpo | 200: JSON da tarefa atualizada. |
| `PATCH /api/tasks/{id}/reopen` | ID inteiro positivo, sem corpo | 200: JSON da tarefa atualizada. |
| `GET /health` | Sem corpo | 200: `{"status":"ok"}`. |

### Validações, transições e erros

- **422 — pedido inválido:** título em falta, vazio, só espaços ou com tipo incorreto; tipo inválido na descrição; identificador que não seja inteiro positivo; JSON malformado. A resposta identifica o campo ou o problema.
- **404 — tarefa não encontrada:** identificador válido que não corresponde a nenhuma tarefa.
- **409 — transição incompatível:** concluir tarefa já concluída ou reabrir tarefa já aberta. A tarefa conserva o estado anterior.
- Não criar tarefas nem alterar estados quando a validação falha.
- Nas respostas de erro, usar JSON com a propriedade `detail`, em texto ou estrutura explicativa coerente com FastAPI. A interface deve mostrar mensagens claras sem expor detalhes internos.
- Atualizar a página não elimina por si só as tarefas guardadas no processo. Reiniciar ou recriar o processo da aplicação perde os dados; a execução pode começar novamente sem tarefas. Não há garantia de persistência.

## Requisitos não funcionais e critérios verificáveis

| ID | Requisito | Critério de aceitação |
| --- | --- | --- |
| RNF-01 | Acesso local | Interface acessível em `http://localhost:8080` enquanto o serviço está em execução. |
| RNF-02 | Docker | Um único serviço, `Dockerfile` e `compose.yaml`; porta `127.0.0.1:8080:8000` (host → container), sem dependência de serviços pagos. |
| RNF-03 | Simplicidade | HTML simples, navegação compreensível, lista vazia informativa, criação e transições disponíveis sem login ou permissões diferenciadas. |
| RNF-04 | Modularidade | Rotas HTTP separadas da lógica de tarefas e do armazenamento em memória; organização documentada e verificável por inspeção. |
| RNF-05 | Dados temporários | Dados permanecem disponíveis em pedidos sucessivos enquanto o processo corre; recriar o processo elimina tarefas e não existe base de dados nem volume de persistência. |
| RNF-06 | Clareza pedagógica | Código e configuração com comentários explicativos úteis; cada teste identifica ID, objetivo, pré-condições, ação, resultado esperado e ligações a RF/RNF e US; README documenta instalação, execução e testes. |

## Percurso mínimo de aceitação

1. Iniciar o serviço Docker; abrir `http://localhost:8080`.
2. Consultar a lista inicialmente vazia sem erro.
3. Criar uma tarefa válida; verificar título, ID e estado **Aberta**.
4. Concluir a tarefa e observar **Concluída**.
5. Reabri-la e observar **Aberta**.
6. Rejeitar título vazio, ID inexistente e transições repetidas com mensagens compreensíveis.
7. Consultar `GET /health` e confirmar HTTP 200.
8. Atualizar a página e verificar que a lista continua disponível enquanto o processo corre.
9. Reiniciar/recriar o processo de aplicação e explicar a perda de dados em memória.
10. Executar o catálogo de testes de [05_rastreabilidade_e_testes.md](05_rastreabilidade_e_testes.md).

## Fora do MVP

- Login, utilizadores e permissões; apagar/editar tarefas, prazos, prioridades e atribuições.
- Base de dados, PostgreSQL e persistência de tarefas.
- Notificações e serviços cloud pagos.
- Filas, CI/CD e observabilidade avançada.

Estas evoluções podem ser discutidas pedagogicamente, mas não devem ser implementadas nesta fase.
