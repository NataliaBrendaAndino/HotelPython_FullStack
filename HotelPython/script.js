document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("contactanos");

    form.addEventListener("submit", function (event) {
        const nombre = document.getElementById("firstname").value;
        const apellido = document.getElementById("lastname").value;
    
        console.log("Nombre:", nombre);
        console.log("Apellido:", apellido);
    
        if (!validarNombreApellido(nombre) || !validarNombreApellido(apellido)) {
            alert("El nombre y el apellido deben tener al menos tres letras.");
            event.preventDefault(); // Detener el envío del formulario
        } else {
            console.log("Formulario enviado exitosamente.");
        }
    });

    function validarNombreApellido(texto) {
        return texto.length >= 3;
    }
});

// Función para realizar la solicitud a la API
async function obtenerComentarios() {
    try {
        const response = await fetch('https://jsonplaceholder.typicode.com/comments');
        const comentarios = await response.json();

        mostrarComentarios(comentarios);
    } catch (error) {
        console.error('Error al obtener los comentarios:', error);
    }
}

// Función para mostrar los comentarios en el elemento HTML
function mostrarComentarios(comentarios) {
    const comentariosDiv = document.getElementById('comentarios');

    // Obtener los primeros 27 comentarios
    const primerosComentarios = comentarios.slice(0, 27);

    primerosComentarios.forEach((comentario, index) => {
        const comentarioDiv = document.createElement('div');
        comentarioDiv.classList.add('comentario');
        comentarioDiv.innerHTML = `
            <h3>${comentario.name}</h3>
            <p>${comentario.body}</p>
            <span>Por: ${comentario.email}</span>
        `;
        comentariosDiv.appendChild(comentarioDiv);
    });
}

// Llama a la función para obtener los comentarios cuando se carga la página
window.addEventListener('load', obtenerComentarios);



