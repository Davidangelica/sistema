function crearCookie(nombre, valor, expiracionEnDias) {
    const fechaExpiracion = new Date();
    fechaExpiracion.setDate(fechaExpiracion.getDate() + expiracionEnDias);
  
    const cookieValor = encodeURIComponent(valor) + (expiracionEnDias ? `; expires=${fechaExpiracion.toUTCString()}` : "");
  
    document.cookie = `${nombre}=${cookieValor}; path=/`;
  }

  function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


function generarCookie() {
    const boton = document.getElementById('boton_inicio_e')

    boton.addEventListener('click',async function(){ 
        await delay(2000);
    const token = localStorage.getItem('token');
    const tokenObj = {"token":token }; // Crear el objeto JSON con la estructura {"token": "valor del token"}

    fetch('http://127.0.0.1:8000/nombre/empleado/verificacion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(tokenObj) // Enviar el objeto JSON con el token
   

    })
    .then(respuesta => respuesta.json())
    .then(data => {
        const nombreEmpleado = data.nombre;
        console.log(nombreEmpleado)
        crearCookie("nombre", nombreEmpleado,1)

    })
    .catch(error => {
        console.error('Error:', error);
    });
}
    )}

generarCookie();