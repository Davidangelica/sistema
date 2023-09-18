function obtenerValorDeCookie(nombre) {
    const cookies = document.cookie.split(";");
    
    for (const cookie of cookies) {
        const [cookieNombre, cookieValor] = cookie.split("=");
  
        if (cookieNombre.trim() === nombre) {
            return decodeURIComponent(cookieValor);
        }
    }
  
    return null;
  }

const cookie_producto = obtenerValorDeCookie('nombre')
const boton_productos = document.getElementById('boton_producto_a')

boton_productos.addEventListener('click',() =>{
    const url = `http://127.0.0.1:8000/menuPrincipal/admin/productos/${encodeURIComponent(cookie_producto)}`
    window.location.href = url
})