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
   
  
const Cookie2 = obtenerValorDeCookie("nombre");



function obtenerEmpleados() {
  return fetch(`http://127.0.0.1:8000/empleados/total/administrador/${encodeURIComponent(Cookie2)}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(respuesta => {
    if (!respuesta.ok) {
      throw new Error('error en la red');
    }
    return respuesta.json();
  })
  .then(data => {
    console.log(data);
    let tabla = $('#tabla_empleados').DataTable({
      data: data,
      columns: [
        { data: 'id' },
        { data: 'nombre_de_usuario' },
        { data: 'nombre' },
        { data: 'apellido' },
        { data: 'email' }, 
        {data: 'dni' },
        { data: 'fecha_de_creacion' },
        {data: null,
          render: function (data, type, row) {
            return `
              <button class="btn-edit" data-id="${row.id}">Editar</button>
              <button class="btn-delete" data-id="${row.id}">Eliminar</button>
            `;
          }}
      ],
      
      lengthChange: false,
      info: false,
      dom: 'lrtip', // Controla qué elementos se muestran en la tabla
      columnDefs: [
        { className: 'dt-center', targets: '_all' } // Agrega la clase 'dt-center' a todas las celdas
      ]
    });

    $('#tabla_empleados tbody').on('click', 'button.btn-edit', function () {
      const empleadoId = $(this).data('id');
      // Lógica para editar empleado con el ID empleadoId
      console.log(`Editar empleado con ID: ${empleadoId}`);
    });
  
    $('#tabla_empleados tbody').on('click', 'button.btn-delete', function () {
      const empleadoId = $(this).data('id');
      const url = 'http://127.0.0.1:8000/empleados/admin/eliminar/empleado'
      const token = localStorage.getItem('token')

      id = {'id':empleadoId}

      fetch(url,{
        method:'DELETE',
        headers:{
          'Content-Type': 'application/json', 
          'Authorization': `Bearer ${token}`,
          },
        body:JSON.stringify(id)
      })      
    });


    $('#search').on('keyup', function() {
      let valorBusqueda = $(this).val(); // Obtiene el valor del campo de búsqueda
      tabla.search(valorBusqueda).draw(); // Realiza la búsqueda en la tabla y actualiza los resultados
    });
  })
  .catch(error => {
    // Manejar el error si es necesario
    console.error('Error:', error); 
  });
}

obtenerEmpleados();

document.addEventListener("DOMContentLoaded", function() {
  const btnAgregarEmpleado = document.getElementById("btnAgregarEmpleado");
  const formularioAgregar = document.getElementById("formulario-agregar-empleados");
  const overlay = document.createElement("div");
  overlay.className = "overlay";
  document.body.appendChild(overlay);

  overlay.style.display = "none";
  formularioAgregar.style.display = "none";

  btnAgregarEmpleado.addEventListener("click", function() {
    overlay.style.display = "block";
    formularioAgregar.style.display = "block";
  });

  // Agrega un evento de clic al botón "Cancelar" para cerrar el formulario y borrar datos
  const btnCancelar = document.getElementById("btnCancelar");
  btnCancelar.addEventListener("click", function() {
    cancelarAgregar();
  });

  function cancelarAgregar() {
    overlay.style.display = "none";
    formularioAgregar.style.display = "none";

    // Restablecer los valores de los campos del formulario
    const nombreDeUsuario = document.getElementById("nombre_de_usuario");
    const nombre = document.getElementById("nombre");
    const email = document.getElementById("email");
    const dni = document.getElementById("dni");
    const apellido = document.getElementById("apellido");
    const contraseña = document.getElementById("contraseña")



    nombreDeUsuario.value = ""; // Borra el valor del campo nombre
    nombre.value = ""; // Borra el valor del campo precio
    email.value = "";  // Borra el valor del campo stock
    dni.value = ""; 
    apellido.value = ""; 
    contraseña.value = ""; 
  }

  const formulario = document.getElementById("formulario");
  formulario.addEventListener("submit", function(event) {
    event.preventDefault();
    // Procesa el formulario y agrega el producto si es necesario
    cancelarAgregar();
  });
});


const btnGuardar = document.getElementById("btnGuardar");

btnGuardar.addEventListener('click',() => {
const token = localStorage.getItem('token')
const url = 'http://127.0.0.1:8000/empleados/admin/añadir/empleado'

const nombreDeUsuario = document.getElementById("nombre_de_usuario").value;
const nombre = document.getElementById("nombre").value;
const email = document.getElementById("email").value;
const dni = document.getElementById("dni").value;
const apellido = document.getElementById("apellido").value;
const contraseña = document.getElementById("contraseña").value

empleado = {
'nombre_de_usuario':nombreDeUsuario,
'nombre':nombre,
'email':email,
'dni':dni,
'apellido':apellido,
'contraseña':contraseña                                        
} 

fetch(url,{
  method:'POST',
  headers:{
    'Content-Type': 'application/json', 
    'Authorization': `Bearer ${token}`,
    },
  body:JSON.stringify(empleado)
})

.then(response => {
  if (!response.ok) {
    return response.json()
    .then(data => {
      console.error('Error en la solicitud:', data.detail); // Muestra el mensaje de error en la consola
      throw new Error('Error en la solicitud');
    });
  }
  return response.json();
})
.then(data =>{
  console.log(data)
})

})


