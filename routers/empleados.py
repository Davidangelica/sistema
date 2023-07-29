from fastapi import APIRouter,Depends
from seguridad.autenticacion_admin import oauth2_administrador, token_auth
from modelos.modelo_empleado import Empleado,EmpleadoDB,session_empleado
from base_de_datos.sql import conexion_a_base_de_datos
from funciones.funciones_del_sistema import *
from datetime import datetime

router = APIRouter()

@router.post('/añadir/empleado')
async def empleado(empleado:Empleado,auth_admin = Depends(token_auth)):
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
     
     