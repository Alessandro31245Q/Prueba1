from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas.Schemas_Agregar import EmpleadoProyecto, EmpleadoProyectoCreate
from models.Modelos_Empleado_Proyecto import empleadosProyectos as DBEmpleadoProyecto
from config.db import SessionLocal

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/empleadosproyectos/", tags=["Proyecto_Empleado"])
def create_empleado_proyecto(proyecto_id: int, empleado_id: int, db: Session = Depends(get_db)):
    db_empleado_proyecto = DBEmpleadoProyecto.insert().values(proyectos_id=proyecto_id, empleados_id=empleado_id)
    db.execute(db_empleado_proyecto)
    db.commit()
    return {"message": "Empleado-Proyecto creado exitosamente"}

@router.delete("/empleadosproyectos/{proyecto_id}/{empleado_id}", tags=["Proyecto_Empleado"])
def delete_empleado_proyecto(proyecto_id: int, empleado_id: int, db: Session = Depends(get_db)):
    db_empleado_proyecto = db.query(DBEmpleadoProyecto).filter(DBEmpleadoProyecto.c.proyectos_id == proyecto_id, DBEmpleadoProyecto.c.empleados_id == empleado_id).first()
    if db_empleado_proyecto is None:
        raise HTTPException(status_code=404, detail="Empleado-Proyecto no encontrado")
    db.execute(DBEmpleadoProyecto.delete().where(DBEmpleadoProyecto.c.proyectos_id == proyecto_id).where(DBEmpleadoProyecto.c.empleados_id == empleado_id))
    db.commit()
    return {"message": "Empleado-Proyecto eliminado exitosamente"}

@router.get("/empleadosproyectos/todos", tags=["Proyecto_Empleado"])
def get_todos_empleados_proyectos(db: Session = Depends(get_db)):
    query = db.query(DBEmpleadoProyecto).all()
    results = [{"proyectos_id": row.proyectos_id, "empleados_id": row.empleados_id} for row in query]
    return results

