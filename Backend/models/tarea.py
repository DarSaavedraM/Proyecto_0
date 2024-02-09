from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from config.database import Base

class Tarea(Base):
    __tablename__ = 'tareas'
    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String, index=True)
    fecha_creacion = Column(String, index=True)  # Considera usar DateTime en lugar de String
    fecha_finalizacion = Column(String, index=True)  # Considera usar DateTime
    estado = Column(String, index=True)
    id_categoria = Column(Integer, ForeignKey('categorias.id'))  # Verifica que esto sea correcto
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))  # Asegúrate de que este modelo exista

    usuario = relationship('Usuario', back_populates='tareas')  # Verifica relación con Usuario
    categoria = relationship('Categoria', back_populates='tareas')
