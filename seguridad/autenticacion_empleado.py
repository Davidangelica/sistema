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

router = APIRouter()

router.post('/login/empleado')
async def empleado():
    pass
    