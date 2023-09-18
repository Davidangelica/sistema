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


const cookie = obtenerValorDeCookie('nombre')
const boton_empleados = document.getElementById('boton_empleados_a')

boton_empleados.addEventListener('click',()=>{
    const url = `http://127.0.0.1:8000/menuPrincipal/admin/empleados/${encodeURIComponent(cookie)}`
    window.location.href = url
}
)