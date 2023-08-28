from sqlite3 import Connection
import bcrypt
from seguridad.administrador_data import administrador_1
from seguridad.pw import contraseña
from modelos.modelo_administrador import Administrador,AdministradorDB, session_admin
from datetime import datetime,date

def crear_administrador():
    administrador = administrador_1
    salt = bcrypt.gensalt()
    contraseña_codificada = bcrypt.hashpw(contraseña.encode('utf-8'),salt)
    administrador['contraseña'] = contraseña_codificada
    nuevo_administrador = AdministradorDB(**administrador)
    
    nuevo_administrador.fecha_de_creacion = datetime.now()
    session_admin.add(nuevo_administrador)
    session_admin.commit()
    session_admin.close()
    
    return 'creado'

def buscar_administrador(nombre:str,conn:Connection,retorno:int) -> Administrador | bool:
    cursor = conn.cursor()
    
    query = cursor.execute(f"SELECT * FROM administrador WHERE administrador.nombre = '{nombre}'")
    if not query:
        return False
    
    try:
        fields = [descripcion[0] for descripcion in cursor.description]
        records = cursor.fetchall()
        for record in records: # bucle for en valores de los campos
            result = {} # inicializamos un dict
            for field,value in zip(fields,record): # cremos un bucle for que itere las dos varibles que tenemos: los campos(fields) y los valores (records)
                result[field] = value
            admnistrador = Administrador(**result)
            if retorno == 1:
                return admnistrador
            if retorno == 2:
                if type(admnistrador) == Administrador:
                    return True
                else:
                    return False 
    except Exception as e:
        return e


def chek_credenciales_admin(nombre, contrasena_plana, conn:Connection) -> bool:
    cursor = conn.cursor()

    cursor.execute('SELECT contraseña FROM administrador WHERE administrador.nombre = ?', (nombre,))
    resultado = cursor.fetchone()

    if resultado:
        hash_contrasena = resultado[0]
        conn.close()
        return bcrypt.checkpw(contrasena_plana.encode('utf-8'), hash_contrasena)

    conn.close()
    return False