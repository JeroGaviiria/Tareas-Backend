from datetime import date
from typing import List
from sqlalchemy.orm import Session
from src.models.tareas import Tarea
from src.schemas.tareas import Tarea as TareaSchema, TareaCreate

class TareaRepository:
    def __init__(self, db) -> None:
        self.db = db

    def get_tareas(
        self, min_valor: float, max_valor: float, offset: int, limit: int, id: int
    ) -> List[TareaSchema]:
        query = self.db.query(Tarea).filter(Tarea.owner_id == id)
        if min_valor is not None:
            query = query.filter(Tarea.valor >= min_valor)
        if max_valor is not None:
            query = query.filter(Tarea.valor < max_valor)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()    
    
    def get_tarea(self, id: int) -> TareaSchema:
        element = self.db.query(Tarea).filter(Tarea.id == id).first()
        return element
        
    def create_tarea(self, tarea: TareaCreate, id: int) -> dict:
        new_tarea = Tarea(**tarea.model_dump())
        new_tarea.owner_id = id
        self.db.add(new_tarea)
        self.db.commit()
        self.db.refresh(new_tarea)
        return new_tarea
    
    def update_tarea(self, id: int, tarea: TareaCreate) -> dict:
        element = self.db.query(Tarea).filter(Tarea.id == id).first()
        element.nombre = tarea.nombre
        element.descripcion = tarea.descripcion
        element.categoria = tarea.categoria
        element.hora = tarea.hora
        element.prioridad = tarea.prioridad
        element.fecha_limite=tarea.fecha_limite
        self.db.commit()
        self.db.refresh(element)
        return element
    def delete_tarea(self, id: int) -> dict:
        element: Tarea = self.db.query(Tarea).filter(Tarea.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element
    ####
    def get_tareas_by_fecha_limite(
        self, fecha_limite: date, id: int
    ) -> List[TareaSchema]:
        query = self.db.query(Tarea).filter(Tarea.owner_id == id, Tarea.fecha_limite == fecha_limite)
        return query.all()    
    
    def get_tareas_by_prioridad(
        self, prioridad: int, id: int
    ) -> List[TareaSchema]:
        query = self.db.query(Tarea).filter(Tarea.owner_id == id, Tarea.prioridad == prioridad)
        return query.all()

    def get_tareas_by_categoria(
        self, categoria: str, id: int
    ) -> List[TareaSchema]:
        query = self.db.query(Tarea).filter(Tarea.owner_id == id, Tarea.categoria == categoria)
        return query.all()

    def marcar_tarea_completa(self, id: int) -> dict:
        element = self.db.query(Tarea).filter(Tarea.id == id).first()
        element.completada = True
        self.db.commit()
        self.db.refresh(element)
        return element
    def get_tareas_no_completadas(self, owner_id: int) -> List[TareaSchema]:
        return self.db.query(Tarea).filter(Tarea.owner_id == owner_id, Tarea.completada == False).all()
    
    def delete_tareas_completadas(self, owner_id: int):
        tareas_completadas = self.db.query(Tarea).filter_by(completada=True, owner_id=owner_id).all()
        for tarea in tareas_completadas:
            self.db.delete(tarea)
        self.db.commit()