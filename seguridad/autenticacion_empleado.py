# fastAPi
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#funciones
from funciones.funciones_administrador import *

# base de datos
from datetime import datetime, timedelta
import sqlite3 as sql
#models
from modelos.modelo_administrador import *
#jwt
from jose import jwt, JWTError
from jwt.exceptions import JWTDecodeError
#security
import bcrypt
import secrets
from base_de_datos.sql import conexion_a_base_de_datos
from seguridad.secret import *
from modelos.modelo_empleado import Empleado
from funciones.funciones_empleado import *


router = APIRouter()

oauth2_empleado = OAuth2PasswordBearer(tokenUrl='/login/empleado')


@router.post('/login/empleado')
async def empleado(form:OAuth2PasswordRequestForm = Depends(), conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    
    try:
        chek_credenciales = chek_credenciales_empleado(form.username,form.password,db)
        if not chek_credenciales:
            raise Exception
   
    except Exception as e:
        return e
        
    expire = datetime.utcnow() + timedelta(minutes=2)
    
    token = {'sub':form.username,
             'exp':expire,
             'rol':'empleado'}
    
    token_encriptado = jwt.encode(token,secret_key,algorithm=ALGORITHM)
    
    return token_encriptado



def token_auth_empleado (conn:Connection = Depends(conexion_a_base_de_datos),token:str = Depends(oauth2_empleado)):
    db = sql.connect(conn)
    empleado_nombre = jwt.decode(token,secret_key,algorithms=ALGORITHM).get('sub')
    chek_empleado = buscar_empleado(empleado_nombre,db,2)
    return chek_empleado