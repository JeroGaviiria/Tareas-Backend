import re
from pydantic import BaseModel, Field, validator
from datetime import date

class Tarea(BaseModel):
    id: int = Field(default=None, primary_key=True)
    nombre: str = Field(..., title="Nombre de la tarea")
    descripcion: str = Field(..., title="Descripción de la tarea")
    prioridad: int = Field(..., ge=1, le=3, title="Prioridad de la tarea (1, 2, o 3)")
    fecha_limite: date = Field(..., title="Fecha límite de la tarea")
    hora: str = Field(..., title="Hora de la tarea en formato HH:MM")
    completada: bool = Field(False, title="Indica si la tarea está completada o no")
    categoria: str = Field(..., title="Categoría de la tarea")
    owner_id: int = Field(..., ge=1, title="Owner of the ingreso")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Hacer la compra",
                "descripcion": "Ir al supermercado y comprar leche y pan.",
                "prioridad": 2,
                "fecha_limite": "2024-05-31",
                "hora": "12:00",
                "completada": False,
                "categoria": "Compras",
                "owner_id": 1
            }
        }


    @validator("prioridad")
    def validate_prioridad(cls, v):
        if v not in {1, 2, 3}:
            raise ValueError("La prioridad de la tarea debe ser 1, 2 o 3")
        return v

    @validator("hora")
    def validate_hora(cls, v):
        if not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", v):
            raise ValueError("La hora debe estar en formato HH:MM y ser válida")
        return v

class TareaCreate(BaseModel):
    nombre: str = Field(..., title="Nombre de la tarea")
    descripcion: str = Field(..., title="Descripción de la tarea")
    prioridad: int = Field(..., ge=1, le=3, title="Prioridad de la tarea (1, 2, o 3)")
    fecha_limite: date = Field(..., title="Fecha límite de la tarea")
    hora: str = Field(..., title="Hora de la tarea en formato HH:MM")
    completada: bool = Field(False, title="Indica si la tarea está completada o no")
    categoria: str = Field(..., title="Categoría de la tarea")
