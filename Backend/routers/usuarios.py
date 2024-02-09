from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.usuario import Usuario as UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.security import OAuth2PasswordRequestForm
from utils.jwt_manager import create_token
from fastapi import UploadFile, File, Form



usuario_router = APIRouter()


@usuario_router.post('/usuarios', tags=['usuario'], response_model=dict, status_code=201)
async def create_usuario(nombre_usuario: str = Form(...), contrasena_hash: str = Form(...), imagen_perfil: UploadFile = File(None), db: Session = Depends(get_db)):
    hashed_password = generate_password_hash(contrasena_hash)
    file_location = "static/profile_images/default_icon.webp"
    if imagen_perfil:
        filename = f"{nombre_usuario}_{imagen_perfil.filename}"
        file_location = f"static/profile_images/{filename}"  # Cambia la ubicación para imágenes subidas
        with open(file_location, "wb+") as file_object:
            file_object.write(imagen_perfil.file.read())
    
    nuevo_usuario = UserModel(
        nombre_usuario=nombre_usuario,
        contrasena_hash=hashed_password,
        imagen_perfil=file_location,
    )
    try:
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return {"message": "Usuario creado exitosamente", "id": nuevo_usuario.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@usuario_router.post('/usuarios/iniciar-sesion', tags=['usuario'])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario_db = db.query(UserModel).filter(UserModel.nombre_usuario == form_data.username).first()
    if not usuario_db or not check_password_hash(usuario_db.contrasena_hash, form_data.password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    token = create_token(user_id=usuario_db.id)
    return {"access_token": token, "token_type": "bearer"}