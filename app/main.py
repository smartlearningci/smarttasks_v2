"""API e HTML originais; seleção do armazenamento na inicialização.

O Compose define STORAGE_BACKEND=postgres. Testes antigos injetam memória.
Nunca regressar silenciosamente à memória se a configuração falhar.
"""
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Path as PathParam
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .db import connection_kwargs, initialize_schema
from .models import Task, TaskCreate
from .service import InvalidTransition, TaskNotFound, TaskService
from .storage import MemoryTaskStore, PostgresTaskStore

STATIC = Path(__file__).resolve().parent / "static"


def create_app(store: MemoryTaskStore | PostgresTaskStore | None = None) -> FastAPI:
    """Preserva a API e permite injetar armazenamento isolado nos testes."""
    if store is None:
        backend = os.environ.get("STORAGE_BACKEND", "memory")
        if backend == "postgres":
            store = PostgresTaskStore(connection_kwargs())
        elif backend == "memory":
            store = MemoryTaskStore()
        else:
            raise RuntimeError("STORAGE_BACKEND inválido: usar memory ou postgres")

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # A tabela é criada antes do primeiro pedido; falhas impedem arranque.
        if isinstance(store, PostgresTaskStore):
            initialize_schema(store.connect_kwargs)
        yield

    app = FastAPI(title="SmartTasks", version="1.0.0", lifespan=lifespan)
    service = TaskService(store)
    app.mount("/static", StaticFiles(directory=STATIC), name="static")

    @app.get("/", include_in_schema=False)
    def home():
        return FileResponse(STATIC / "index.html")

    @app.get("/health", tags=["Operação"])
    def health():
        return {"status": "ok"}

    @app.get("/api/tasks", response_model=list[Task], tags=["Tarefas"])
    def list_tasks():
        return service.list_tasks()

    @app.post("/api/tasks", response_model=Task, status_code=201, tags=["Tarefas"])
    def create_task(data: TaskCreate):
        return service.create(data)

    def change_state(task_id: int, target: str) -> Task:
        try:
            return service.transition(task_id, target)
        except TaskNotFound as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except InvalidTransition as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @app.patch("/api/tasks/{task_id}/complete", response_model=Task, tags=["Tarefas"])
    def complete_task(task_id: int = PathParam(gt=0)):
        return change_state(task_id, "Concluída")

    @app.patch("/api/tasks/{task_id}/reopen", response_model=Task, tags=["Tarefas"])
    def reopen_task(task_id: int = PathParam(gt=0)):
        return change_state(task_id, "Aberta")

    return app


app = create_app()
