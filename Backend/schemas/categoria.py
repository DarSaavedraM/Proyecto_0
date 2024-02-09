from pydantic import BaseModel

class CategoriaCreate(BaseModel):

    nombre:str
    descripcion: str

class Categoria(BaseModel):
    id: int
    nombre: str
    descripcion: str