# SmartTasks — Requisitos e MVP

## Funcionalidades incluídas
| ID | Requisito funcional | Critério de aceitação |
| --- | --- | --- |
| RF-01 | Listar tarefas | Ao abrir a interface, são apresentadas as tarefas existentes e o seu estado; uma lista vazia é apresentada sem erro. |
| RF-02 | Criar tarefa | Um título não vazio é obrigatório; a descrição é opcional; uma tarefa válida surge na lista com estado **Aberta**. |
| RF-03 | Concluir tarefa | Uma tarefa aberta pode passar ao estado **Concluída**, refletindo-se na lista. |
| RF-04 | Reabrir tarefa | Uma tarefa concluída pode voltar ao estado **Aberta**, refletindo-se na lista. |
| RF-05 | Disponibilizar API HTTP | A API permite listar, criar, concluir e reabrir tarefas, com respostas HTTP apropriadas. |
| RF-06 | Verificar saúde | `GET /health` devolve HTTP 200 enquanto a aplicação estiver operacional. |

## Requisitos não funcionais
| ID | Requisito | Critério de aceitação |
| --- | --- | --- |
| RNF-01 | Acesso local | Interface acessível em `http://localhost:8080` com a aplicação em execução. |
| RNF-02 | Docker | Um único serviço definido em `Dockerfile` e `compose.yaml`, com porta do host 8080 ligada à porta 8000 do container, preferencialmente em `127.0.0.1`. |
| RNF-03 | Simplicidade | Interface HTML simples, sem autenticação. |
| RNF-04 | Modularidade | Organização do código que separe as operações sobre tarefas da exposição HTTP, facilitando evolução posterior. |
| RNF-05 | Dados temporários | Tarefas mantidas em memória durante a execução, sem garantia de conservação após reinício. |
| RNF-06 | Clareza pedagógica | Código e testes documentados; cada teste identifica o objetivo e os requisitos verificados. |

## Percurso mínimo de aceitação
1. Iniciar o serviço Docker e abrir `http://localhost:8080`.
2. Consultar a lista de tarefas.
3. Criar uma tarefa com título e sem descrição; confirmar que aparece como **Aberta**.
4. Concluir a tarefa; confirmar o estado **Concluída**.
5. Reabrir a tarefa; confirmar o estado **Aberta**.
6. Consultar `GET /health` e confirmar HTTP 200.
7. Reiniciar a aplicação e explicar que os dados em memória não são persistentes.

## Fora do MVP
- Login, gestão de utilizadores e permissões.
- Base de dados e persistência de tarefas.
- Notificações e serviços cloud pagos.
- Filas, CI/CD e observabilidade avançada.

Estas exclusões não impedem a discussão de evoluções futuras; não devem ser implementadas nesta fase.
