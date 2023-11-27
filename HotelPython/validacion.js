// --------------------------------------------------------
// El evento "submit" del formulario desencadena esta validación.
// Este código JavaScript se encarga de validar un formulario
// HTML antes de enviarlo. Cada función de validación verifica
// si ciertos campos o elementos están completos o
// seleccionados correctamente. Si alguna validación falla,
// se muestra una alerta al usuario y se evita que el
// formulario se envíe mediante e.preventDefault().
// La función validar se ejecuta cuando se presiona el botón
// "Enviar" y llama a las tres validaciones.
// --------------------------------------------------------


// --------------------------------------------------------
// Obtenemos el formulario y elementos del mismo
// --------------------------------------------------------

// Obtenemos el primer formulario del documento por su nombre
let formulario = document.getElementsByName('formulario')[0];

// Obtenemos los elementos dentro del formulario
let elementos = formulario.elements;

// Obtenemos el botón por su id
let boton = document.getElementById('b1');

// --------------------------------------------------------
// Validación del campo Nombre
// --------------------------------------------------------
let validarNombre = function (e) {
    // Verificamos si el campo de nombre está vacío
    if (formulario.nombre.value == '') {
        // Mostramos una alerta al usuario
        alert("Completa el campo nombre");

        // Evitamos el comportamiento por defecto del formulario
        e.preventDefault();
    }
};

// --------------------------------------------------------
// Validación de los radios de Sistema Operativo
// --------------------------------------------------------
let validarRadio = function (e) {
    // Verificamos si al menos uno de los radios está marcado
    if (
        formulario.so[0].checked == false &&
        formulario.so[1].checked == false &&
        formulario.so[2].checked == false
    ) {
        // Mostramos una alerta al usuario
        alert("Selecciona un Sistema Operativo");

        // Evitamos el comportamiento por defecto del formulario
        e.preventDefault();
    }
};

// --------------------------------------------------------
// Validación del checkbox de Términos y Condiciones
// --------------------------------------------------------
let validarCheckbox = function (e) {
    // Verificamos si el checkbox de términos y condiciones no está marcado
    if (formulario.terminos.checked == false) {
        // Mostramos una alerta al usuario
        alert("Acepta los términos y condiciones");

        // Evitamos el comportamiento por defecto del formulario
        e.preventDefault();
    }
};

// --------------------------------------------------------
// Función principal de validación
// --------------------------------------------------------
let validar = function (e) {
    // Esta función se ejecuta al presionar el botón "Enviar"
    // y llama a las tres validaciones anteriores
    validarNombre(e);
    validarRadio(e);
    validarCheckbox(e);
};

// --------------------------------------------------------
// Esperamos el evento "submit" del formulario y llamamos a
//la función de validación
// --------------------------------------------------------
formulario.addEventListener("submit", validar);
