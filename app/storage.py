# RNF-05: dicionário em memória; sem ficheiros, volumes ou base de dados.
# O conteúdo e o contador de IDs desaparecem quando o processo reinicia.
"""Armazenamento volátil, isolado da API — RNF-04, RNF-05."""
from .models import Task

class MemoryTaskStore:
    """RNF-04/RNF-05: armazenamento temporário substituível."""
    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self.next_id = 1

    def all(self) -> list[Task]:
        return list(self.tasks.values())

    def insert(self, title: str, description: str | None) -> Task:
        """RF-02: cria a tarefa Aberta e atribui ID sequencial."""
        task = Task(id=self.next_id, title=title, description=description, status="Aberta")
        self.tasks[task.id] = task
        self.next_id += 1
        return task

    def get(self, task_id: int) -> Task | None:
        return self.tasks.get(task_id)
