# basemodel
from pydantic import BaseModel
#datetime
from datetime import datetime,date
#sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker


class Administrador (BaseModel):
    id: int | None
    nombre:str
    email : str | None
    contraseña : str
    fecha_de_creacion : datetime | None
    
    @property 
    def adminstrador(self):
        return True
    
#url de la base de datos
db_url = 'sqlite:///C:/programa_distribudora/base_de_datos/distribuidora.db'
engine = create_engine(db_url)
base = declarative_base()

class AdministradorDB (base):
    __tablename__ = 'administrador'
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(),unique=True)
    email = Column(String(),nullable=False,unique=True)
    contraseña = Column(String(), nullable=False,unique=False)
    fecha_de_creacion = Column(DateTime(),nullable=False)
    
base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session_admin = Session()

