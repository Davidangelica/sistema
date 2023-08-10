# fastAPi
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer, HTTPBasic
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


router = APIRouter()

oauth2_administrador = OAuth2PasswordBearer(tokenUrl='/login/administrador')


@router.post('/login/administrador')
async def administrador(administrador:Administrador,conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
   
    try:
         chek_credenciales = chek_credenciales_admin(administrador.nombre, administrador.contraseña, db)
    
    except:
        return {'error':'no se encuntra el administrador'}
    
    if chek_credenciales:
        expire = datetime.utcnow() + timedelta(minutes=2)
        token = {'sub':administrador.nombre,
                 'exp':expire,
                 'rol':'administrasdor'}
        token_encode = jwt.encode(token,secret_key,algorithm=ALGORITHM)
        return token_encode
    


def token_auth_admin (conn:Connection = Depends(conexion_a_base_de_datos),token:str = Depends(oauth2_administrador)):
    db = sql.connect(conn)
    admin_nombre = jwt.decode(token,secret_key,algorithms=ALGORITHM).get('sub')
    chek_admin = buscar_administrador(admin_nombre,db,2)
    return chek_admin
