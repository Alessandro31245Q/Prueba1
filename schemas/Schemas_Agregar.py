from pydantic import BaseModel

class EmpleadoProyectoCreate(BaseModel):
    proyectos_id: int
    empleados_id: int

class EmpleadoProyecto(EmpleadoProyectoCreate):
    id: int

    class Config:
        orm_mode = True
