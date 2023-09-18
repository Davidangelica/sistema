import bcrypt
from sqlite3 import Connection
from modelos.modelo_producto import Productos
from funciones.funciones_del_sistema import *

def buscar_producto (busqueda:str | int | None , atributo:str, conn:Connection) -> Productos | list[Productos]:
    cursor = conn.cursor()
    # todos
    if atributo == 'total':
        query = cursor.execute(f"SELECT * FROM productos")
        if not query:
            return 'no se encontraron resultados'
    #id
    if atributo == 'id':
         query = cursor.execute(f"SELECT * FROM productos WHERE productos.id =  '{busqueda}'")
         if not query:
            return 'no se encontraron resultados'
    #nombre
    if atributo == 'nombre':
        query = cursor.execute(f"SELECT * FROM productos WHERE productos.nombre =  '{busqueda}'") # realizamos la consulta a la base de datos
        if not query:
            return 'no se encontraron resultados'
    # precio
    if atributo == 'precio':
         query = cursor.execute(f"SELECT * FROM productos WHERE productos.precio =  {busqueda}")
         if not query:
            return 'no se encontraron resultados'
    # stock
    if atributo == 'stock':
         query = cursor.execute(f"SELECT * FROM productos WHERE productos.cantidad_en_stock =  '{busqueda}'")
         if not query:
            return 'no se encontraron resultados'
    
    if atributo == 'fecha':
         query = cursor.execute(f"SELECT * FROM productos WHERE productos.fecha_de_actualizacion =  '{busqueda}'")
         if not query:
            return 'no se encontraron resultados'
  
        
    registros = cursor.fetchall()
    productos = []

    campos = [descripcion[0] for descripcion in cursor.description]

    for registro in registros:
        producto_dict = dict(zip(campos, registro))
        producto = Productos(**producto_dict)
        productos.append(producto)

    return productos
       


def actualizar_producto(producto:Productos,conn:Connection):
    cursor = conn.cursor()
    id = producto.id
    
    productodb = buscar_producto(id,'id',conn)
    producto_db = productodb[0]
    
    if producto_db.nombre != producto.nombre:
        try:
            cursor.execute(f"UPDATE productos SET nombre = '{producto.nombre}' WHERE productos.id = {id}")
            
        
        except Exception as e:
            return e
    
    if producto_db.precio != producto.precio:
        try:
            cursor.execute(f"UPDATE productos SET precio = {producto.precio} WHERE productos.id = {id}")
            
        
        except Exception as e:
            return e
    
    if producto_db.cantidad_en_stock != producto.cantidad_en_stock:
        try:
            cursor.execute(f"UPDATE productos SET cantidad_en_stock = {producto.cantidad_en_stock} WHERE productos.id = {id}")
            
        
        except Exception as e:
            return e
    
    conn.commit()
    
    return 'el producto a sido actualizado con exito'


def elimiar_productos(id:str,conn:Connection):
    cursor = conn.cursor()
    query = f'DELETE FROM productos WHERE productos.id = {id}'
    try:
        cursor.execute(query)

    except Exception as e:
        conn.rollback()
        return e
    
    conn.commit()