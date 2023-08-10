import bcrypt
import sqlite3 as sql
from fastapi import Depends
from base_de_datos.sql import conexion_a_base_de_datos
from jose import jwt, JWTError
from jwt.exceptions import JWTDecodeError
from seguridad.secret import secret_key,ALGORITHM
from funciones.funciones_administrador import *
from funciones.funciones_empleado import *
from funciones.funciones_del_sistema import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer, HTTPBasic, HTTPBasicCredentials

def hash_contraseña (password:str):
    salt = bcrypt.gensalt()
    try:
        hash_password = bcrypt.hashpw(password.encode('utf-8'),salt)
    except Exception:
        return {'error':'the password could not hashed'}
    
    return hash_password

def chequear_contraseña (pw1,pw2):
    try:
        chek = bcrypt.checkpw(pw1.encode('utf-8'),pw2.encode('utf-8'))
        return 'hola'
    except:
        return False


seguridad = HTTPBasic()

def auth_basica(token:str, credenciales:HTTPBasicCredentials = Depends(seguridad) ,conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    try:
        token = jwt.decode(token,secret_key,algorithms=ALGORITHM).get('rol')
        nombre = jwt.decode(token,secret_key,algorithms=ALGORITHM).get('sub') 
        
    except JWTDecodeError as e:
        return e
    
    if token == 'administrador':
       credenciales.username = nombre
       return credenciales.username

    if token == 'empleado':
        credenciales.username = nombre
        return credenciales.username