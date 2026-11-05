"""Modelos de entrada e saída — RF-02, RF-05 / US-02."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, field_validator

class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    description: str | None = None

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("O título não pode estar vazio.")
        return value

class Task(BaseModel):
    id: int
    title: str
    description: str | None
    status: Literal["Aberta", "Concluída"]
