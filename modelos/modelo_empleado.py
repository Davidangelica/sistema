from pydantic import BaseModel
from datetime import datetime,date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine, func, Float, Boolean
from sqlalchemy.orm import sessionmaker


class Empleado (BaseModel):
    id:int | None
    nombre : str
    apellido : str
    email : str
    dni : int
    contraseña : str
    fecha_de_creacion : datetime | None
    


db_url = 'sqlite:///C:/programa_distribudora/base_de_datos/distribuidora.db'
engine = create_engine(db_url)
base = declarative_base()

class EmpleadoDB (base):
    __tablename__ = 'empleados'
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(),nullable=False,unique=False)
    apellido = Column(String(),nullable=False,unique=False)
    email = Column(String(),nullable=False,unique=True)
    dni = Column(Integer(), nullable=False, unique=True)
    contraseña = Column(String(), nullable=False,unique=False)
    fecha_de_creacion = Column(DateTime(),nullable=False)
    
base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session_empleado = Session()