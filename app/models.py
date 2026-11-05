# TaskCreate valida o JSON de entrada; Task descreve o objeto de resposta.
# O cliente não pode escolher id ou status: são definidos pelo servidor.
"""Modelos de entrada e saída — RF-02, RF-05 / US-02."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, field_validator

class TaskCreate(BaseModel):\n    """RF-02/RF-05: dados aceites ao criar uma tarefa."""
    # Rejeita campos extra, incluindo ID e estado enviados pelo cliente.\n    model_config = ConfigDict(extra="forbid")
    title: str
    description: str | None = None

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str) -> str:\n        """Remove espaços nas extremidades e impede título vazio."""
        value = value.strip()
        if not value:
            raise ValueError("O título não pode estar vazio.")
        return value

class Task(BaseModel):\n    """RF-01: dados devolvidos, com apenas dois estados possíveis."""
    id: int
    title: str
    description: str | None
    status: Literal["Aberta", "Concluída"]
