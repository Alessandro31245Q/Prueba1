from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas.Schemas_Empleado import Empleado, EmpleadoCreate
from models.Modelos_Empleado_Proyecto import Empleado as DBEmpleado
from config.db import SessionLocal,Base,engine

router = APIRouter()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/empleados/", response_model=Empleado)
def create_empleado(empleado: EmpleadoCreate, db: Session = Depends(get_db)):
    db_empleado = DBEmpleado(**empleado.dict())
    db.add(db_empleado)
    db.commit()
    db.refresh(db_empleado)
    return db_empleado

@router.get("/empleados/{empleado_id}", response_model=Empleado)
def read_empleado(empleado_id: int, db: Session = Depends(get_db)):
    db_empleado = db.query(DBEmpleado).filter(DBEmpleado.id == empleado_id).first()
    if db_empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return db_empleado

@router.get("/empleados/", response_model=List[Empleado])
def read_empleados(db: Session = Depends(get_db)):
    return db.query(DBEmpleado).all()

@router.put("/empleados/{empleado_id}", response_model=Empleado)
def update_empleado(empleado_id: int, empleado: EmpleadoCreate, db: Session = Depends(get_db)):
    db_empleado = db.query(DBEmpleado).filter(DBEmpleado.id == empleado_id).first()
    if db_empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    # Actualizar los atributos del empleado existente con los datos proporcionados
    for key, value in empleado.dict().items():
        setattr(db_empleado, key, value)

    db.commit()
    db.refresh(db_empleado)
    return db_empleado

@router.delete("/empleados/{empleado_id}", response_model=Empleado)
def delete_empleado(empleado_id: int, db: Session = Depends(get_db)):
    db_empleado = db.query(DBEmpleado).filter(DBEmpleado.id == empleado_id).first()
    if db_empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    db.delete(db_empleado)
    db.commit()
    return db_empleado
