from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from config.database import get_db
from models.usuario import Usuario as UserModel
from utils.jwt_manager import validate_token, SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/iniciar-sesion")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserModel:
    credentials_exception = HTTPException(status_code=401, detail="Credenciales inválidas")
    try:
        payload = validate_token(token)
        user_id: int = payload.get("user_id")
        # Verifica que user_id sea un entero
        if not isinstance(user_id, int):
            raise HTTPException(status_code=401, detail="El user_id en el token no es válido")
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception