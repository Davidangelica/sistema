// Código JavaScript para funcionalidad de añadir productos y búsqueda

document.addEventListener("DOMContentLoaded", () => {
    const addButton = document.querySelector(".add-button");
    const searchButton = document.querySelector(".search-box button");
    const searchInput = document.querySelector(".search-box input[type='text']");
    const productTableBody = document.querySelector(".product-table tbody");
  
    // Función para agregar un producto a la tabla
    const addProduct = (product) => {
      const newRow = document.createElement("tr");
      newRow.innerHTML = `
        <td>${product.id}</td>
        <td>${product.nombre}</td>
        <td>${product.precio}</td>
        <td>${product.cantidad_en_stock}</td>
        <td>${product.fecha_de_Actualizacion}</td>
        <td>
          <button class="edit-button"><i class="ri-pencil-line"></i></button>
          <button class="delete-button"><i class="ri-delete-bin-line"></i></button>
        </td>
      `;
      productTableBody.appendChild(newRow);
    };
  
    // Evento para el botón de añadir producto
    addButton.addEventListener("click", () => {
      const product = {
        id: "N/A",
        nombre: "Nuevo Producto",
        precio: "$0.00",
        cantidad_en_stock: "0",
        fecha_de_Actualizacion: "N/A"
      };
      addProduct(product);
    });
  
    // Evento para el botón de búsqueda
    searchButton.addEventListener("click", () => {
      const searchTerm = searchInput.value.toLowerCase();
      const rows = productTableBody.querySelectorAll("tr");
      rows.forEach(row => {
        const cells = row.querySelectorAll("td");
        let found = false;
        cells.forEach(cell => {
          if (cell.textContent.toLowerCase().includes(searchTerm)) {
            found = true;
          }
        });
        row.style.display = found ? "table-row" : "none";
      });
    });
  
    // ... (otras funcionalidades y eventos) ...
  });
  