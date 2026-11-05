"""Regras de negócio independentes das rotas HTTP — RF-02 a RF-04."""
from .models import Task, TaskCreate
from .storage import MemoryTaskStore

class TaskNotFound(Exception):
    pass

class InvalidTransition(Exception):
    pass

class TaskService:
    def __init__(self, store: MemoryTaskStore):
        self.store = store

    def list_tasks(self) -> list[Task]:
        return self.store.all()

    def create(self, data: TaskCreate) -> Task:
        return self.store.insert(data.title, data.description)

    def transition(self, task_id: int, target: str) -> Task:
        task = self.store.get(task_id)
        if task is None:
            raise TaskNotFound("Tarefa não encontrada.")
        if task.status == target:
            raise InvalidTransition("A tarefa já se encontra no estado solicitado.")
        task.status = target
        return task
