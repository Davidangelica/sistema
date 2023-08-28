# fastAPi
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
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
async def empleado(empleado:Empleado, conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    
    try:
        chek_credenciales = chek_credenciales_empleado(empleado.nombre_de_usuario,empleado.contraseña,db)
        if not chek_credenciales:
            raise Exception
   
    except Exception as e:
        return e
        
    expire = datetime.utcnow() + timedelta(minutes=2)
    
    token = {'sub':empleado.nombre_de_usuario,
             'exp':expire,
             'rol':'empleado'}
    
    token_encriptado = jwt.encode(token,secret_key,algorithm=ALGORITHM)
    
    return token_encriptado

@router.post('/nombre/empleado/verificacion')
async def admin(token_json:dict):
    token = token_json['token']
    admin_nombre = jwt.decode(token,secret_key,algorithms=ALGORITHM).get('sub')
    nombre = {'nombre':admin_nombre}
    return nombre





def token_auth_empleado (conn:Connection = Depends(conexion_a_base_de_datos),token:str = Depends(oauth2_empleado)):
    db = sql.connect(conn)
    empleado_nombre = jwt.decode(token,secret_key,algorithms=ALGORITHM).get('sub')
    chek_empleado = buscar_empleado(empleado_nombre,db,2)
    return chek_empleado


def verificar_permisos_empleado(request: Request, conn:Connection = Depends (conexion_a_base_de_datos)):
    db = sql.connect(conn)
    nombre_empelado = request.query_params
    empleado = buscar_empleado(nombre_empelado,db,2)
    return empleado