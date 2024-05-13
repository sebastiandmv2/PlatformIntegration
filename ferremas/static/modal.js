// Función para mostrar un modal con un mensaje dado
function showModal(message) {
    var modal = document.getElementById("message-modal");
    var messageText = document.querySelector("#message-text");
    messageText.innerHTML = message;
    modal.style.display = "block";
}

// Función para cerrar el modal cuando se haga clic en el botón de cerrar
function closeModal() {
    var modal = document.getElementById("message-modal");
    modal.style.display = "none";
}