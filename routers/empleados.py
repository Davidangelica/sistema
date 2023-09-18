#fast api
from fastapi import APIRouter,Depends
from fastapi.responses import FileResponse
#seguridad
from seguridad.autenticacion_admin import oauth2_administrador, token_auth_admin, verificar_permisos_admin
#modelos
from modelos.modelo_empleado import Empleado,EmpleadoDB,session_empleado
#base de datos
from base_de_datos.sql import conexion_a_base_de_datos
from sqlite3 import Connection
import sqlite3 as sql
#funciones
from funciones.funciones_del_sistema import *
from funciones.funciones_empleado import *

#router
router = APIRouter()

#cargamos los archivos esticos de la la tabla de empleados
@router.get('/menuPrincipal/admin/empleados/{nombre}')
async def empleados(nombre:str,auth = Depends(verificar_permisos_admin)):
     return FileResponse('front/empleados/empleados.html')


#añadir empleado
@router.post('/empleados/admin/añadir/empleado')
async def empleado(empleado:Empleado,auth_admin = Depends(token_auth_admin)):
   añadir_empleados(empleado)  

#actulizar empleado   
@router.put('/actualizar/empleado')
async def empleado(empleado:Empleado, conn:Connection = Depends(conexion_a_base_de_datos), auth_admin = Depends(token_auth_admin)):
     db = sql.connect(conn)
     actualizar_empleados(empleado,db)

#elimiar empleado
@router.delete('empleados/admin/eliminar/empleado')
async def empleado(id:str, auth_admin = Depends(token_auth_admin), conn:Connection = Depends(conexion_a_base_de_datos)):
     db = sql.connect(conn)
     elimiar_empleado(id,db)




@router.get('/empleados/total/administrador/{nombre}')
async def empleado(nombre:str, auth = Depends(verificar_permisos_admin),  conn:Connection = Depends(conexion_a_base_de_datos)):
     db = sql.connect(conn)
     empleados = total_empleados(db)
     return empleados
     


    