from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String,Table
from sqlalchemy.ext.declarative import declarative_base
from config.db import Base
from sqlalchemy.orm import relationship
Base = declarative_base()

empleadosProyectos = Table(
    "empleadosproyectos",
    Base.metadata,
    Column("proyectos_id", Integer, ForeignKey("proyectos.Id_Proyecto")),
    Column("empleados_id", Integer, ForeignKey("empleados.id"))
)

class Empleado(Base):
    __tablename__ = "empleados"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    rol = Column(String)
    disponibilidad = Column(Boolean)
    proyectos = relationship("Proyecto",secondary=empleadosProyectos,back_populates="empleados")
    
    
class Proyecto(Base):
    __tablename__ = "proyectos"
    Id_Proyecto = Column(Integer, primary_key=True, index=True)
    Nombre_Proyecto = Column(String)
    Fecha_Inicio = Column(DateTime)
    Fecha_Fin = Column(DateTime)
    Estado = Column(Boolean)
    empleados = relationship("Empleado", secondary=empleadosProyectos, back_populates="proyectos")
