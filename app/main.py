"""Camada HTTP e entrega da interface — RF-01 a RF-06."""
from pathlib import Path
from fastapi import FastAPI, HTTPException, Path as PathParam
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .models import Task, TaskCreate
from .service import InvalidTransition, TaskNotFound, TaskService
from .storage import MemoryTaskStore

STATIC = Path(__file__).resolve().parent / "static"

def create_app(store: MemoryTaskStore | None = None) -> FastAPI:
    """Permite injetar um armazenamento novo em cada teste."""
    app = FastAPI(title="SmartTasks", version="1.0.0")
    service = TaskService(store if store is not None else MemoryTaskStore())
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
