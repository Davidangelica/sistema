from pydantic import BaseModel
from datetime import datetime,date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine, func, Float, Boolean
from sqlalchemy.orm import sessionmaker



db_url = 'sqlite:///C:/programa_distribudora/base_de_datos/distribuidora.db'
engine = create_engine(db_url)
base = declarative_base()


class TokenDB (base):
    __tablename__ = 'historial de ingreso'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    sub = Column(String())
    rol = Column(String())
    fecha_de_ingreso = Column(DateTime())
    


    
base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session_token = Session()

