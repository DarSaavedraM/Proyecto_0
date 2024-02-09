from pydantic import BaseModel, Field
from typing import Optional
from fastapi import UploadFile

class UsuarioCreate(BaseModel):

    nombre_usuario : str = Field(max_length=300,description="Nombre de usuario")
    contrasena_hash : str  
    imagen_perfil: Optional[UploadFile] = None

    class Config:
        json_schema_extra = {
            "example": {
                "nombre_usuario": "username",
                "contrasena_hash": "hashed_password",
                "imagen_perfil": "profile_picture.jpg",
            }
        }
