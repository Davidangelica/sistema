const botonInicio = document.getElementById('boton_inicio_e');

botonInicio.addEventListener('click', () => {
  const nombre = document.getElementById('nombre_e').value;
  const contraseña = document.getElementById('contraseña_e').value;

  // Verificar si los campos están vacíos
  if (nombre === '' || contraseña === '') {
    console.log('Ingresa nombre de usuario y contraseña.');
    return; // Detener la función si los campos están vacíos
  }

  const datos = {
    nombre_de_usuario: nombre,
    contraseña: contraseña
  };

  const datosJSON = JSON.stringify(datos);

  // Crea una función para realizar la petición
  function hacerPeticion() {
    return new Promise((resolve, reject) => {

      const url = "http://127.0.0.1:8000/login/empleado";

      const headers = {
        "Content-Type": "application/json"
      };

      fetch(url, {
        method: "POST",
        headers: headers,
        body: datosJSON 
      })

        .then(response => {

          if (response.ok) {
            return response.json();

          } else {
            reject(new Error("Error en la petición"));
          }
        })

        .then(data => {
          resolve(data);
        })
        .catch(error => {
          reject(error);
        });
    });
  }

  // Llama a la función para hacer la petición y maneja la respuesta
  hacerPeticion()
    .then(respuesta => {
      console.log('Respuesta:', respuesta);
      // guardamos el token
      localStorage.setItem("token", respuesta);

      generarCookie();

      //history.replaceState({}, "Menu Principal", "/menuPrincipal");
    })
    .catch(error => {
    
      console.error('Error:', error);
    });
});
