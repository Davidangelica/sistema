from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from seguridad.autenticacion_admin import  token_auth_admin
from seguridad.autenticacion_empleado import token_auth_empleado
from base_de_datos.sql import conexion_a_base_de_datos
from funciones.funciones_del_sistema import *
from datetime import datetime
from sqlite3 import Connection
import sqlite3 as sql
from modelos.modelo_producto import Productos,ProductosDB,session_producto
from funciones.funciones_productos import *

router = APIRouter()

# opciones de admin

#añadir productos
@router.post('/productos/admin/añadir')
async def producto(producto:Productos, auth = Depends(token_auth_admin)):
    producto_dict = dict(producto)
    nuevo_producto = ProductosDB(**producto_dict)
    nuevo_producto.fecha_de_actualizacion = datetime.now()
    session_producto.add(nuevo_producto)
    session_producto.commit()
    return nuevo_producto

# actualizar productos 
@router.put('/productos/admin/actualizar')
async def producto(producto : Productos,  conn : Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    return actualizar_producto(producto,db)

# buscar por id
@router.get('/productos/admin/id/{id}')
async def producto (id:int, auth = Depends(token_auth_admin), conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    return buscar_producto(id,'id',db)

# buscar por nombre
@router.get('/productos/admin/nombre/{nombre}')
async def producto(nombre:str, auth = Depends(token_auth_admin), conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    return buscar_producto(nombre,'nombre',db)

# buscar por precio
@router.get('/productos/admin/precio/{precio}')
async def producto(precio:int,auth = Depends(token_auth_empleado),  conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    return buscar_producto(precio,'precio',db)

# buscar por cantidad en stock
@router.get('/productos/admin/precio/{stock}')
async def producto(stock:int, auth = Depends(token_auth_admin), conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    return buscar_producto(stock,'stock',db)


"""# buscar por fecha de actualizacion
@router.get('/productos/admin/precio/{fecha}')
async def producto(precio:int, auth = Depends(token_auth_admin), conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    return buscar_producto(precio,'precio',db)
"""


# buscar por id
@router.get('/productos/empleado/id/{id}')
async def producto (id:int, auth = Depends(token_auth_empleado), conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    return buscar_producto(id,'id',db)

# buscar por nombre
@router.get('/productos/empleado/nombre/{nombre}')
async def producto(nombre:str, auth = Depends(token_auth_empleado), conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    return buscar_producto(nombre,'nombre',db)

# buscar por precio
@router.get('/productos/empleado/precio/{precio}')
async def producto(precio:int, auth = Depends(token_auth_empleado) ,conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    return buscar_producto(precio,'precio',db)

# buscar por cantidad en stock
@router.get('/productos/empleado/precio/{stock}')
async def producto(stock:int, auth = Depends(token_auth_empleado), conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    return buscar_producto(stock,'stock',db)
