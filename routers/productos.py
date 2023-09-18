from fastapi import APIRouter,Depends
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from seguridad.autenticacion_admin import  token_auth_admin,verificar_permisos_admin
from seguridad.autenticacion_empleado import token_auth_empleado
from base_de_datos.sql import conexion_a_base_de_datos
from funciones.funciones_del_sistema import *
from datetime import datetime
from sqlite3 import Connection
import sqlite3 as sql
from modelos.modelo_producto import Productos,ProductosDB,session_producto
from funciones.funciones_productos import *

router = APIRouter()

# cargar elementos estaticos

@router.get('/menuPrincipal/admin/productos/{nombre}')
async def productos(nombre:str, auth = Depends(verificar_permisos_admin)):
    return FileResponse("front/productos/productos.html")
 


# opciones de admin
#añadir productos
@router.post('/productos/admin/añadir')
async def producto(producto_json:Productos, auth = Depends(token_auth_admin)):
    nombre = producto_json.nombre
    precio = int(producto_json.precio)
    cantidad_en_stock = int(producto_json.cantidad_en_stock)
    
    producto = ProductosDB(nombre=nombre,
                           precio=precio,
                           cantidad_en_stock=cantidad_en_stock,
                           fecha_de_actualizacion=datetime.now())
   
    session_producto.add(producto)
    session_producto.commit()

# actualizar productos 
@router.put('/productos/admin/actualizar')
async def producto(producto_json: Productos, auth = Depends(token_auth_admin), conn : Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    return actualizar_producto(producto_json,db)


#todos los productos
@router.get('/productos/admin/total/{nombre}')
async def productos (nombre:str, auth = Depends(verificar_permisos_admin), conn:Connection = Depends (conexion_a_base_de_datos)):
    db = sql.connect(conn)
    return buscar_producto(busqueda=None,atributo='total',conn=db)


# buscar por id
@router.get('/productos/admin/id/{id}')
async def producto (id:int,auth = Depends(verificar_permisos_admin),conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    return buscar_producto(id,'id',db)

# buscar por nombre
@router.get('/productos/admin/nombre/{nombre}')
async def producto(nombre:str, auth = Depends(verificar_permisos_admin), conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    return buscar_producto(nombre,'nombre',db)

# buscar por precio
@router.get('/productos/admin/precio/{precio}')
async def producto(precio:int,auth = Depends(verificar_permisos_admin),  conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    return buscar_producto(precio,'precio',db)

# buscar por cantidad en stock
@router.get('/productos/admin/precio/{stock}')
async def producto(stock:int, auth = Depends(verificar_permisos_admin), conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    return buscar_producto(stock,'stock',db)

#eliminar productos
@router.delete('/productos/admin/eliminar')
async def producto (id_json:dict,auth = Depends(token_auth_admin),conn:Connection = Depends(conexion_a_base_de_datos)):
    db = sql.connect(conn)
    id = id_json['id']
    elimiar_productos(id,db)
    

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
