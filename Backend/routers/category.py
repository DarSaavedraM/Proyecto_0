from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
from models.categoria import Categoria as CategoriaModel
from schemas.categoria import CategoriaCreate, Categoria


category_router = APIRouter()

@category_router.get("/categorias/", tags = ['categorias'], response_model=List[Categoria])
def get_categorias(db: Session = Depends(get_db)):
    categorias = db.query(CategoriaModel).all()
    return categorias

@category_router.post("/categorias/", tags=['categorias'], response_model=Categoria)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    # Verifica si ya existe una categoría con el mismo nombre
    categoria_existente = db.query(CategoriaModel).filter(CategoriaModel.nombre == categoria.nombre).first()
    if categoria_existente:
        raise HTTPException(status_code=400, detail="La categoría ya existe.")
    nueva_categoria = CategoriaModel(nombre=categoria.nombre, descripcion=categoria.descripcion)
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return nueva_categoria

@category_router.delete("/categorias/{id}", tags = ['categorias'], response_model=dict)
def eliminar_categoria(id: int, db: Session = Depends(get_db)):
    categoria = db.query(CategoriaModel).filter(CategoriaModel.id == id).first()
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(categoria)
    db.commit()
    return {"message": "Categoría eliminada exitosamente"}