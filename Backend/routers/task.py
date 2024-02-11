from fastapi import Path, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from typing import List

from models.tarea import Tarea as TareaModel
from config.database import get_db
from middlewares.jwt_bearer import JWTBearer
from services.dependencies import get_current_user
from models.usuario import Usuario as UserModel
from models.categoria import Categoria as CategoriaModel
from schemas.tarea import TaskCreate
from schemas.tarea import TaskResponse

task_router = APIRouter()

@task_router.get('/tareas/usuario', tags=['tareas'], response_model=List[TaskResponse], dependencies=[Depends(JWTBearer())])
def get_tarea_usuario(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    try:
        result = db.query(TareaModel).filter(TareaModel.id_usuario == current_user.id).all()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@task_router.get('/tareas/{id}', tags=['tareas'], response_model=TaskCreate, dependencies=[Depends(JWTBearer())])
def get_tareas(id: int = Path(...), db: Session = Depends(get_db)):  # Añadir `id` como argumento de la función
    try:
        result = db.query(TareaModel).filter(TareaModel.id == id).first()
        if result is None:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@task_router.post('/tareas/', tags=['tareas'], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
def create_tarea(tarea: TaskCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):

    if tarea.id_categoria == 0:
        id_categoria_asignada = None
    else:
        categoria = db.query(CategoriaModel).filter(CategoriaModel.id == tarea.id_categoria).first()
        if not categoria:
            raise HTTPException(status_code=400, detail="Categoría inexistente.")
        id_categoria_asignada = tarea.id_categoria

    nueva_tarea = TareaModel(
        texto=tarea.texto,
        fecha_creacion=tarea.fecha_creacion,
        fecha_finalizacion=tarea.fecha_finalizacion,
        estado=tarea.estado,
        id_categoria=id_categoria_asignada,
        id_usuario=current_user.id
    )

    try:
        db.add(nueva_tarea)
        db.commit()
        db.refresh(nueva_tarea)
        return {"message": "Tarea creada exitosamente", "id": nueva_tarea.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@task_router.put('/tareas/{id}', tags=['tareas'], response_model=dict, dependencies=[Depends(JWTBearer())])
def update_tareas(id: int, tarea: TaskCreate, db: Session = Depends(get_db)):
    tarea_db = db.query(TareaModel).filter(TareaModel.id == id).first()
    if not tarea_db:
        raise HTTPException(status_code=404, detail="Tarea no existe")

    try:
        if tarea.texto is not None:
            tarea_db.texto = tarea.texto
        if tarea.fecha_finalizacion is not None:
            tarea_db.fecha_finalizacion = tarea.fecha_finalizacion
        if tarea.estado is not None:
            # No es necesario asignar tarea.estado a sí mismo, directamente actualizamos tarea_db.estado
            tarea_db.estado = TaskCreate.validate_estado(tarea.estado)

        # Añadir la lógica para actualizar id_categoria
        if tarea.id_categoria is not None:
            if tarea.id_categoria == 0:
                tarea_db.id_categoria = None  # Si el id_categoria es 0, se asigna None
            else:
                # Verificar que la nueva categoría exista antes de asignarla
                categoria = db.query(CategoriaModel).filter(CategoriaModel.id == tarea.id_categoria).first()
                if not categoria:
                    raise HTTPException(status_code=400, detail="Categoría inexistente.")
                tarea_db.id_categoria = tarea.id_categoria

        db.commit()
        return {"message": "Tarea modificada exitosamente", "id": tarea_db.id}
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@task_router.delete('/tareas/{id}', tags=['tareas'], response_model=dict, dependencies=[Depends(JWTBearer())])
def delete_tarea(id: int, db: Session = Depends(get_db)):
    tarea = db.query(TareaModel).filter(TareaModel.id == id).first()
    if tarea:
        db.delete(tarea)
        db.commit()
        return {"message": "Tarea eliminada"}
    else:
        raise HTTPException(status_code=404, detail="Tarea no existe")