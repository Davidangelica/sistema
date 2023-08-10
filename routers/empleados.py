from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm
from seguridad.autenticacion_admin import oauth2_administrador, token_auth_admin
from modelos.modelo_empleado import Empleado,EmpleadoDB,session_empleado
from base_de_datos.sql import conexion_a_base_de_datos
from funciones.funciones_del_sistema import *
from funciones.funciones_empleado import *
from datetime import datetime
from sqlite3 import Connection
import sqlite3 as sql

router = APIRouter()

@router.post('/añadir/empleado')
async def empleado(empleado:Empleado,auth_admin = Depends(token_auth_admin)):
     if auth_admin:
          salt = bcrypt.gensalt()
          empleado_dict = dict(empleado)
          del empleado_dict['id']
          contraseña_hash = bcrypt.hashpw(empleado.contraseña.encode('utf-8'),salt)
          empleado_dict['contraseña'] = contraseña_hash
          
          try:
               nuevo_empleado = EmpleadoDB(**empleado_dict)
               nuevo_empleado.fecha_de_creacion = datetime.now()
               session_empleado.add(nuevo_empleado)
               session_empleado.commit()
               session_empleado.close()
               return 'empleado añadido de forma exitosa'
          
          except Exception as e:
               return e
               
     else:
          return 'no se pudo verificar el administrador'     
     
@router.put('/actualizar/empleado')
async def empleado(empleado:Empleado, conn:Connection = Depends(conexion_a_base_de_datos), auth_admin = Depends(token_auth_admin)):
     
     db = sql.connect(conn)
     cursor = db.cursor()

     
     if auth_admin:
          empleado_db = buscar_empleado(empleado.nombre_de_usuario,db)
          
          if empleado_db.email != empleado.email:
               try:
                    cursor.execute(f"UPDATE empleados set email = '{empleado.email}' WHERE empleados.nombre_de_usuario = '{empleado_db.nombre_de_usuario}'")
                    db.commit() 
                    
               except Exception as e:
                    return e

          salt = bcrypt.gensalt()
          encode_contraseña_empleado = bcrypt.hashpw(empleado.contraseña.encode('utf-8'),salt) 
          encode_contraseña_empleado_db = bcrypt.hashpw(empleado_db.contraseña.encode('utf-8'),salt)
          
          if not bcrypt.checkpw(encode_contraseña_empleado,encode_contraseña_empleado_db):
               try:
                    query = "UPDATE empleados set contraseña = ? WHERE empleados.nombre_de_usuario = ?"
                    cursor.execute(query,(encode_contraseña_empleado,empleado_db.nombre_de_usuario))
                    db.commit()
               except Exception as e:
                    return e
               
               
          
     return "accion completada"


@router.delete('/eliminar/empleado/{username}')
async def empleado(username:str, auth_admin = Depends(token_auth_admin), conn:Connection = Depends(conexion_a_base_de_datos)):
     db = sql.connect(conn)
     cursor = db.cursor()
     if auth_admin:
          try:
               query = "DELETE FROM empleados WHERE empleados.nombre_de_usuario = ?"
               cursor.execute(query,(username,))
               db.commit()
          except Exception as e:
               return e
          
     return 'eliminado con exito'


@router.get('/empleado/{username}')
async def empleado(username:str, auth_admin = Depends(token_auth_admin), conn:Connection = Depends(conexion_a_base_de_datos)):
     db = sql.connect(conn)
     if auth_admin:
          try:
               empleado = buscar_empleado(username,db)
               return empleado
          except Exception as e:
               return e