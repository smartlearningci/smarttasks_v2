# SmartTasks — User Stories do MVP

Estas sete histórias concretizam as necessidades das três personas descritas em [01_contexto_e_personas.md](01_contexto_e_personas.md). Os papéis são ilustrativos: o primeiro MVP **não implementa autenticação ou autorização**.

| ID | Persona | User Story | Critérios de aceitação |
| --- | --- | --- | --- |
| US-01 | Ana Martins — colaboradora | Como colaboradora, quero consultar todas as tarefas e respetivos estados para identificar o trabalho pendente. | Lista reflete tarefas persistidas no PostgreSQL e os respetivos estados; lista vazia não provoca erro e é apresentada com mensagem informativa. |
| US-02 | Ana Martins — colaboradora | Como colaboradora, quero criar uma tarefa com título e descrição opcional para registar trabalho a realizar. | Título válido cria tarefa **Aberta** com ID único; descrição pode faltar; título vazio ou só com espaços é rejeitado sem criar tarefa. |
| US-03 | Ana Martins — colaboradora | Como colaboradora, quero concluir uma tarefa aberta para indicar que o trabalho terminou. | Tarefa aberta passa a **Concluída**; ID inexistente e conclusão repetida produzem erros claros sem alterar o estado. |
| US-04 | Ana Martins — colaboradora | Como colaboradora, quero reabrir uma tarefa concluída para indicar que exige mais trabalho. | Tarefa concluída passa a **Aberta**; ID inexistente e reabertura repetida produzem erros claros sem alterar o estado. |
| US-05 | Miguel Costa — responsável de equipa | Como responsável de equipa, quero acompanhar os estados das tarefas para perceber o progresso do trabalho. | A listagem mostra estados atualizados depois de criar, concluir e reabrir; não é necessário painel ou papel de gestão separado. |
| US-06 | Sofia Almeida — responsável de TI | Como responsável de TI, quero verificar a resposta de saúde da aplicação para confirmar que está operacional ao nível HTTP. | `GET /health` devolve 200 e `{"status":"ok"}`; não se exige monitorização avançada. |
| US-07 | Sofia Almeida — responsável de TI | Como responsável de TI, quero iniciar o SmartTasks através de Docker para disponibilizar a aplicação localmente aos formandos. | Construção e arranque com Docker Compose, dois serviços, interface em `http://localhost:8080` e porta do container 8000; documentação dos passos. |

## Regras transversais
- Um utilizador não autenticado com acesso à interface local pode realizar as operações de tarefas; as personas não estabelecem permissões.
- Os erros da API são refletidos na interface por mensagens compreensíveis.
- Os dados e estados persistem no PostgreSQL e sobrevivem ao reinício da aplicação enquanto o volume for mantido.
- Cada US liga-se a RF/RNF e testes em [05_rastreabilidade_e_testes.md](05_rastreabilidade_e_testes.md).
- Qualidades técnicas (modularidade, persistência PostgreSQL e clareza pedagógica) podem ser transversais a várias histórias e exigem verificações específicas; não se considera suficiente uma ligação nominal a uma US.
