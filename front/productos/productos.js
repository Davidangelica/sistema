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


const Cookie = obtenerValorDeCookie("nombre");
const boton = document.getElementById('boton_producto_a');


function obtenerProductos() {
  return fetch(`http://127.0.0.1:8000/productos/admin/total/${encodeURIComponent(Cookie)}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }

  })

  .then(respuesta => {
    if (!respuesta.ok) {
      throw new Error('Network response was not ok');
    }
    return respuesta.json();

  })
  .then(data => {
    console.log(data)
    let tabla = $('#tabla_productos').DataTable({
      data: data,
      columns: [
        { data: 'id' },
        { data: 'nombre' },
        { data: 'precio' },
        { data: 'cantidad_en_stock' },
        { data: 'fecha_de_actualizacion' },
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
  })
      
    $('#tabla_productos tbody').on('click', 'button.btn-edit', function () {
      const productoId = $(this).data('id');
      const id = {'id':productoId};
      const url = 'http://127.0.0.1:8000/productos/admin/actualizar'
      // Lógica para editar empleado con el ID empleadoId
      console.log(`Editar empleado con ID: ${productoId}`);
    });
    
    $('#tabla_productos tbody').on('click', 'button.btn-delete', function () {
      const productoId = $(this).data('id');
      const id = {'id':productoId};
      const url = 'http://127.0.0.1:8000/productos/admin/eliminar'
      const token = localStorage.getItem('token')
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
    console.error('Error:', error);
  }); 
  
}
obtenerProductos();



document.addEventListener("DOMContentLoaded", function() {
  const btnAgregarProductos = document.getElementById("btnAgregarProductos");
  const formularioAgregar = document.getElementById("formularioAgregar");
  const overlay = document.createElement("div");
  overlay.className = "overlay";
  document.body.appendChild(overlay);

  overlay.style.display = "none";
  formularioAgregar.style.display = "none";

  btnAgregarProductos.addEventListener("click", function() {
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
    const nombre = document.getElementById("nombre");
    const precio = document.getElementById("precio");
    const stock = document.getElementById("stock");

    nombre.value = ""; // Borra el valor del campo nombre
    precio.value = ""; // Borra el valor del campo precio
    stock.value = "";  // Borra el valor del campo stock
  }

  const formulario = document.getElementById("formulario");
  formulario.addEventListener("submit", function(event) {
    event.preventDefault();
    // Procesa el formulario y agrega el producto si es necesario
    cancelarAgregar();
  });
});


const btnGuardar = document.getElementById("btnGuardar");
btnGuardar.addEventListener('click',()=>{
  const token = localStorage.getItem('token')
  const url = 'http://127.0.0.1:8000/productos/admin/añadir'
 

  const nombre = document.getElementById("nombre").value;
  const precio = document.getElementById("precio").value;
  const stock = document.getElementById("stock").value;

  const producto = {
    'nombre':nombre,
    'precio':precio,
    'cantidad_en_stock':stock
  }

  fetch(url,{

    method:'POST',
    headers:{
    'Content-Type': 'application/json', 
    'Authorization': `Bearer ${token}`,
    },
    body:JSON.stringify(producto),

})

.then(response => {
  if (!response.ok) {
    return response.json().then(data => {
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