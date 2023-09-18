import bcrypt
from sqlite3 import Connection
from funciones.funciones_del_sistema import *
from modelos.modelo_empleado import Empleado,session_empleado,EmpleadoDB
from datetime import datetime,date



def buscar_empleado (nombre:str, conn:Connection, retorno:int) -> Empleado | bool:
    cursor = conn.cursor()
    query = cursor.execute(f"SELECT * FROM empleados WHERE empleados.nombre_de_usuario = '{nombre}'") # realizamos la consulta a la base de datos
    if not query:
        return False
    try:
        campos = [descripcion[0] for descripcion in cursor.description] #cremos una variable con un bucle for para recolectar los campos del empleado en la base de datos
        registros = cursor.fetchall() # obtenemos el valor de los campos
        for registro in registros: # bucle for en valores de los campos
            resultado = {} # inicializamos un dict
            for campo,valor in zip(campos,registro): # cremos un bucle for que itere las dos varibles que tenemos: los campos(fields) y los valores (records)
                resultado[campo] = valor # indicamos que el campo es igual al valor
            empleado = Empleado(**resultado)
            if retorno == 1:
                return empleado
            if retorno == 2:
                if type (empleado) == Empleado:
                    return True
                else:
                    return False
                
    except Exception as e:
        return e
    
def total_empleados(conn:Connection) -> list[Empleado]:
    cursor = conn.cursor()
    query = cursor.execute("SELECT * FROM empleados")
    
    registros = cursor.fetchall()
    empleados = []

    campos = [descripcion[0] for descripcion in cursor.description]

    for registro in registros:
        empleado_dict = dict(zip(campos, registro))
        del empleado_dict['contraseña']
        #empleado = Empleado(**empleado_dict)
        empleados.append(empleado_dict)

    return empleados
    
    
    
    
    
    
def chek_credenciales_empleado(nombre, contrasena_plana, conn:Connection):
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT contraseña FROM empleados WHERE empleados.nombre_de_usuario = '{nombre}'")
        resultado = cursor.fetchone()
        if not resultado:
            return False
           
    except Exception as e:
        return e

    if resultado:
        hash_contrasena = resultado[0]
        conn.close()
        return bcrypt.checkpw(contrasena_plana.encode('utf-8'), hash_contrasena)

    conn.close()
    return False
    

def elimiar_empleado (id, conn:Connection):
    cursor = conn.cursor()
    query = f"DELETE FROM empleados WHERE empleados.id = {id}"
    try:
        cursor.execute(query)
    except Exception as e:
        return e

def añadir_empleados(empleado:Empleado):
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
        return 
          
          
    except Exception as e:
        return e
               
def actualizar_empleados(empleado:Empleado,conn:Connection):
    cursor = conn.cursor()
    
    #empleado que queremos actualizar
    empleado_db = buscar_empleado(empleado.nombre_de_usuario,conn)
    
    #si los mail no coinciden los actualizamos
    if empleado_db.email != empleado.email:
        try:
            cursor.execute(f"UPDATE empleados set email = '{empleado.email}' WHERE empleados.nombre_de_usuario = '{empleado_db.nombre_de_usuario}'")
            conn.commit() 
                    
        except Exception as e:
            return e

        salt = bcrypt.gensalt()
        
        #codiifcamos las contraseñas
        encode_contraseña_empleado = bcrypt.hashpw(empleado.contraseña.encode('utf-8'),salt) 
        encode_contraseña_empleado_db = bcrypt.hashpw(empleado_db.contraseña.encode('utf-8'),salt)
        
        # si las contraseñas no coinciden la actulizamos
        if not bcrypt.checkpw(encode_contraseña_empleado,encode_contraseña_empleado_db):
            try:
                query = "UPDATE empleados set contraseña = ? WHERE empleados.nombre_de_usuario = ?"
                cursor.execute(query,(encode_contraseña_empleado,empleado_db.nombre_de_usuario))
                conn.commit()
            except Exception as e:
                return e
               