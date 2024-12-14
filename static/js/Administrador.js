console.log("Archivo Administrador.js cargado correctamente");

$(document).ready(function () {
    $('#productosTable').DataTable({
        "pageLength": 10,
        "ordering": true,
        "searching": false,
        "lengthChange": false,
        "pagingType": "simple",
        "info": false,
        "language": {
            "search": "Buscar:",
            "paginate": {
                "next": '<i class="fas fa-arrow-right"></i>',
                "previous": '<i class="fas fa-arrow-left"></i>'
            }
        }
    });
});


// Función para mostrar u ocultar el menú desplegable
function toggleDropdown() {
    var dropdown = document.querySelector('.user-menu .dropdown-menu');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

// Cerrar el menú si se hace clic fuera de él
window.onclick = function (event) {
    if (!event.target.matches('.user-menu, .user-menu *')) {
        var dropdown = document.querySelector('.user-menu .dropdown-menu');
        if (dropdown) dropdown.style.display = 'none';
    }
}

// Establecer el ID del producto a eliminar en el modal de confirmación
function setDeleteProductId(id) {
    document.getElementById('productToDelete').value = id;
}

// Configurar el modal de eliminación para mostrar el ID del producto
document.addEventListener('DOMContentLoaded', () => {
    const deleteModal = document.getElementById('confirmDeleteModal');
    deleteModal.addEventListener('show.bs.modal', (event) => {
        const button = event.relatedTarget;
        const productId = button.getAttribute('data-id');
        document.getElementById('productToDelete').value = productId;
    });
});

// Vista previa de la imagen en el formulario de registro
function previewImage(event) {
    const input = event.target;
    const reader = new FileReader();
    reader.onload = function () {
        const preview = document.getElementById('imagePreview');
        preview.src = reader.result;
        preview.style.display = 'block';
    };
    reader.readAsDataURL(input.files[0]);
}

// Vista previa de la imagen en el formulario de edición
function previewImageEdit(event) {
    const imagePreview = document.getElementById('editar_imagePreview');
    imagePreview.src = URL.createObjectURL(event.target.files[0]);
    imagePreview.style.display = 'block';
}

// Función para cargar los datos del producto en el formulario de edición
function editProduct(button) {
    const productId = button.getAttribute("data-id");
    fetch(`/obtener_producto/${productId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                Swal.fire("Error", "Producto no encontrado", "error");
            } else {
                document.getElementById("editarForm").action = `/editar_producto/${productId}`;
                document.getElementById("editar_nombre_producto").value = data.nombre_producto;
                document.getElementById("editar_descripcion_producto").value = data.descripcion_producto;
                document.getElementById("editar_precio_producto").value = data.precio_producto;
                document.getElementById("editar_codigo_producto").value = data.codigo_producto;
                document.getElementById("editar_stock_producto").value = data.stock_producto;
                document.getElementById("editar_informacion_adicional").value = data.informacion_adicional;
                document.getElementById("editar_id_categoria").value = data.id_categoria;
                document.getElementById("editar_oferta_producto").checked = data.oferta_producto;

                if (data.imagen_producto) {
                    document.getElementById("editar_imagePreview").src = `data:image/jpeg;base64,${data.imagen_producto}`;
                    document.getElementById("editar_imagePreview").style.display = "block";
                } else {
                    document.getElementById("editar_imagePreview").style.display = "none";
                }
            }
        })
        .catch(error => console.error("Error al cargar el producto:", error));
}

// Función para cerrar sesión
function logout() {
    fetch("/logout", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        }
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url; 
        }
    }).catch(error => console.error("Error al cerrar sesión:", error));
}
