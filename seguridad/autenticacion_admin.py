# fastAPi
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer, HTTPBasic
from fastapi.responses import FileResponse
#funciones
from funciones.funciones_administrador import *
from funciones.funciones_token import *

# base de datos
from datetime import datetime, timedelta
import sqlite3 as sql
#models
from modelos.modelo_administrador import *
from modelos.modelo_token import TokenDB,session_token
#jwt
from jose import jwt, JWTError
from jwt.exceptions import JWTDecodeError
#security
import bcrypt
import secrets
from base_de_datos.sql import conexion_a_base_de_datos
from seguridad.secret import *
from fastapi.staticfiles import StaticFiles


router = APIRouter()


oauth2_administrador = OAuth2PasswordBearer(tokenUrl='/login/administrador')


@router.post('/login/administrador')
async def administrador(administrador:Administrador, conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
   
    try:
        chek_credenciales = chek_credenciales_admin(administrador.nombre, administrador.contraseña, db)
    
        if chek_credenciales:
            expire = datetime.utcnow() + timedelta(minutes=60)
            tiempo_expiracion_str = expire.strftime('%Y-%m-%d %H:%M:%S')
            token = {'sub':administrador.nombre,
                    'expiracion':tiempo_expiracion_str,
                    'rol':'administrador'}
        
            del token['expiracion']
        
            guardar_token(token)
        
            token_encriptado = jwt.encode(token,secret_key,algorithm=ALGORITHM)
            return token_encriptado
            
    except:
        return {'error':'no se encuntra el administrador'}
    
    
@router.post('/nombre/admin/verificacion')
async def admin(token_json:dict):
    token = token_json['token']
    admin_nombre = jwt.decode(token,secret_key,algorithms=ALGORITHM).get('sub')
    nombre = {'nombre':admin_nombre}
    return nombre



def token_auth_admin (conn:Connection = Depends(conexion_a_base_de_datos),token:str = Depends(oauth2_administrador)):
    db = sql.connect(conn)
    admin_nombre = jwt.decode(token,secret_key,algorithms=ALGORITHM).get('sub')
    chek_admin = buscar_administrador(admin_nombre,db,2)
    return chek_admin

    


def verificar_permisos_admin(request: Request, conn: Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    nombre_admin = request.query_params 
    admin = buscar_administrador(nombre_admin,db,2)
    return admin

    