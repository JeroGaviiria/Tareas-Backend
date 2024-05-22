from sqlalchemy import Column, ForeignKey, Integer, String, Date,  Boolean
from sqlalchemy.orm import relationship
from src.config.database import Base


class Tarea(Base):
    __tablename__ = 'tareas'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String)
    descripcion = Column(String)
    prioridad = Column(Integer)
    fecha_limite = Column(Date)
    hora = Column(String)  # Nuevo campo para la hora
    completada = Column(Boolean, default=False)
    categoria = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tareas")




