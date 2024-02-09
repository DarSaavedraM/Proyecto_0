from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base
from passlib.context import CryptContext



class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String, unique=True, index=True)
    contrasena_hash = Column(String)  
    imagen_perfil = Column(String)
    tareas = relationship('Tarea', back_populates='usuario')
