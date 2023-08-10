import bcrypt
from sqlite3 import Connection
from funciones.funciones_del_sistema import *
from modelos.modelo_empleado import Empleado
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
    