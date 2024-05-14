from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas.Schemas_Proyecto import Proyecto, ProyectoCreate
from models.Modelos_Empleado_Proyecto import Proyecto as DBProyecto
from config.db import SessionLocal,Base,engine
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/proyectos/", response_model=Proyecto)
def create_proyecto(proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    db_proyecto = DBProyecto(**proyecto.dict())
    db.add(db_proyecto)
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

@router.get("/proyectos/{proyecto_id}", response_model=Proyecto)
def read_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    db_proyecto = db.query(DBProyecto).filter(DBProyecto.Id_Proyecto == proyecto_id).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return db_proyecto

@router.get("/proyectos/", response_model=List[Proyecto])
def read_proyectos(db: Session = Depends(get_db)):
    return db.query(DBProyecto)

@router.put("/proyectos/{proyecto_id}", response_model=Proyecto)
def update_proyecto(proyecto_id: int, proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    db_proyecto = db.query(DBProyecto).filter(DBProyecto.Id_Proyecto == proyecto_id).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    # Actualizar los atributos del proyecto existente con los datos proporcionados
    for key, value in proyecto.dict().items():
        setattr(db_proyecto, key, value)

    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto


@router.delete("/proyectos/{proyecto_id}", response_model=Proyecto)
def delete_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    db_proyecto = db.query(DBProyecto).filter(DBProyecto.Id_Proyecto == proyecto_id).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    db.delete(db_proyecto)
    db.commit()
    return db_proyecto
