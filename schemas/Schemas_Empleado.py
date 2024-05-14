from pydantic import BaseModel

class EmpleadoCreate(BaseModel):
    nombre: str
    rol: str
    disponibilidad: bool

class Empleado(EmpleadoCreate):
    id: int

    class Config:
        orm_mode = True
