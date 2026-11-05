"""Armazenamento: memória para testes e PostgreSQL para Docker (RNF-04/05).

all, insert, get e update_status têm o mesmo contrato nas duas classes.
As consultas SQL parametrizadas não interpolam dados enviados pelo cliente.
"""
from .models import Task


class MemoryTaskStore:
    """Armazenamento original, preservado para testes HTTP isolados."""

    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self.next_id = 1

    def all(self) -> list[Task]:
        return list(self.tasks.values())

    def insert(self, title: str, description: str | None) -> Task:
        task = Task(id=self.next_id, title=title, description=description, status="Aberta")
        self.tasks[task.id] = task
        self.next_id += 1
        return task

    def get(self, task_id: int) -> Task | None:
        return self.tasks.get(task_id)

    def update_status(self, task_id: int, expected: str, target: str) -> Task | None:
        """Só altera quando o estado anterior corresponde ao esperado."""
        task = self.get(task_id)
        if task is None or task.status != expected:
            return None
        task.status = target
        return task


class PostgresTaskStore:
    """RF-01 a RF-04: persiste tarefas no PostgreSQL com psycopg 3."""

    def __init__(self, connect_kwargs: dict):
        self.connect_kwargs = connect_kwargs

    def _connect(self):
        import psycopg
        return psycopg.connect(**self.connect_kwargs)

    @staticmethod
    def _task(row) -> Task:
        return Task(id=row[0], title=row[1], description=row[2], status=row[3])

    def all(self) -> list[Task]:
        """RF-01: ordenação estável pelo identificador da BD."""
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, description, status FROM tasks ORDER BY id")
                return [self._task(row) for row in cur.fetchall()]

    def insert(self, title: str, description: str | None) -> Task:
        """RF-02: INSERT transacional; a BD atribui o ID."""
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tasks (title, description) VALUES (%s, %s) "
                    "RETURNING id, title, description, status",
                    (title, description),
                )
                return self._task(cur.fetchone())

    def get(self, task_id: int) -> Task | None:
        """RF-03/RF-04: None se a tarefa não existir."""
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, title, description, status FROM tasks WHERE id = %s",
                    (task_id,),
                )
                row = cur.fetchone()
                return self._task(row) if row else None

    def update_status(self, task_id: int, expected: str, target: str) -> Task | None:
        """RF-03/RF-04: UPDATE condicional para evitar conflitos concorrentes.

        Se outra operação alterou o estado, nenhuma linha é atualizada.
        O serviço converte essa situação em HTTP 409 (ou 404 se inexistente).
        """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE tasks SET status = %s WHERE id = %s AND status = %s "
                    "RETURNING id, title, description, status",
                    (target, task_id, expected),
                )
                row = cur.fetchone()
                return self._task(row) if row else None
