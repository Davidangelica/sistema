from pydantic import BaseModel
from datetime import datetime,date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine, func, Float, Boolean
from sqlalchemy.orm import sessionmaker

class Productos (BaseModel):
    id : int | None
    nombre : str
    precio : int
    cantidad_en_stock : int | None
    fecha_de_actualizacion : datetime | None
     
    @property
    def chek_stock(self):
        if Productos.cantidad_en_stock >= 1:
            return True
        else:
            return False



db_url = 'sqlite:///C:/programa_distribudora/base_de_datos/distribuidora.db'
engine = create_engine(db_url)
base = declarative_base()

class ProductosDB (base):
    __tablename__ = 'productos'
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(),nullable=False,unique=True)
    precio = Column(Integer(), nullable=False, unique=False)
    cantidad_en_stock = Column(Integer(), nullable=False, unique=False)
    fecha_de_actualizacion = Column(DateTime(),nullable=False)
    
    
base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session_producto = Session()

