"""Regras de negócio, independentes de FastAPI e do armazenamento."""
from .models import Task, TaskCreate
from .storage import MemoryTaskStore, PostgresTaskStore


class TaskNotFound(Exception):
    """RF-03/RF-04: tarefa inexistente, traduzida para HTTP 404."""


class InvalidTransition(Exception):
    """RF-03/RF-04: transição repetida ou concorrente, HTTP 409."""


class TaskService:
    def __init__(self, store: MemoryTaskStore | PostgresTaskStore):
        self.store = store

    def list_tasks(self) -> list[Task]:
        return self.store.all()

    def create(self, data: TaskCreate) -> Task:
        return self.store.insert(data.title, data.description)

    def transition(self, task_id: int, target: str) -> Task:
        """Verifica estado e grava a transição na camada de armazenamento."""
        task = self.store.get(task_id)
        if task is None:
            raise TaskNotFound("Tarefa não encontrada.")
        if task.status == target:
            raise InvalidTransition("A tarefa já se encontra no estado solicitado.")
        updated = self.store.update_status(task_id, task.status, target)
        if updated is None:
            # Uma operação concorrente pode ter alterado o estado entretanto.
            if self.store.get(task_id) is None:
                raise TaskNotFound("Tarefa não encontrada.")
            raise InvalidTransition("O estado da tarefa foi alterado entretanto.")
        return updated
