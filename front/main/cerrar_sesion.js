function eliminarCookie(nombre) {
    const fechaExpiracionPasada = new Date(0); // Establecer una fecha en el pasado
    document.cookie = `${nombre}=; expires=${fechaExpiracionPasada.toUTCString()}; path=/`;
}




function cerrarSesion (){
    const botonCerrar = document.getElementById('boton_cerrar')

    botonCerrar.addEventListener('click',() =>{
        localStorage.removeItem('token')
        window.location.replace("http://127.0.0.1:8000/index");
        eliminarCookie('nombre')
    } 
    
    )
}
cerrarSesion()