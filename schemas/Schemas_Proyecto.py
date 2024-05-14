from pydantic import BaseModel
from datetime import datetime

class ProyectoCreate(BaseModel):
    Nombre_Proyecto: str
    Fecha_Inicio: datetime
    Fecha_Fin: datetime
    Estado: bool

class Proyecto(ProyectoCreate):
    Id_Proyecto: int
    class Config:
        orm_mode = True
