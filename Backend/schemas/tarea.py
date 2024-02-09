from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):

    texto: str = Field(max_length=300, description="Descripción de la tarea")
    fecha_creacion: datetime = Field(default_factory=datetime.now, description="Fecha de creación de la tarea")
    fecha_finalizacion: Optional[datetime] = Field(description="Fecha tentativa de finalización de la tarea")
    estado: str = Field(default="Sin Empezar", description="Estado de la tarea")
    id_categoria: int = Field(default=0, description="Id de la categoría asociada a la tarea")

    @validator('estado')
    def validate_estado(cls, value):
        estados_validos = ["Sin Empezar", "Empezada", "Finalizada"]
        if value not in estados_validos:
            raise ValueError(f"Estado inválido. Debe ser uno de: {estados_validos}")
        return value
        
    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "texto": "Descripción de la tarea",
                "fecha_creacion": "2023-01-01",
                "fecha_finalizacion": "2023-01-02",
                "id_categoria": 0,
                "estado": "Sin Empezar",
            }
        }