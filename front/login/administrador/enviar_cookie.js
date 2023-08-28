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

function enviarCookie(cookieValue) {
  console.log(cookieValue)
  const url = `http://127.0.0.1:8000/menuPrincipal/admin/${encodeURIComponent(cookieValue)}`;
  
  fetch(url, {
      method: 'GET',
      headers: {
          'Content-Type': 'application/json'
      }
  })
  
  .catch(error => {
      console.error('Error:', error);
  });
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

document.addEventListener("DOMContentLoaded", function() {
  const botonInicio = document.getElementById("boton_inicio");
  botonInicio.addEventListener("click", async function() {
      await delay(2500);
      const valorCookie = obtenerValorDeCookie("nombre");
      if (valorCookie !== null) {
          enviarCookie(valorCookie);
          window.location.href = `http://127.0.0.1:8000/menuPrincipal/admin/${encodeURIComponent(valorCookie)}`
      }
  });
});
