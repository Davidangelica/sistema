from modelos.modelo_token import session_token
from modelos.modelo_token import TokenDB
from datetime import datetime, timedelta

def guardar_token (token:dict):
    
    nuevo_token = TokenDB(**token)
    nuevo_token.fecha_de_ingreso = datetime.now()
    session_token.add(nuevo_token)
    session_token.commit()
    session_token.close()
    