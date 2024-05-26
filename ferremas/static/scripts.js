function incrementQuantity(productId) {
    const quantityInput = document.getElementById(`quantity_${productId}`);
    let quantity = parseInt(quantityInput.value) || 0;
    quantityInput.value = quantity + 1;
}

function decrementQuantity(productId) {
    const quantityInput = document.getElementById(`quantity_${productId}`);
    let quantity = parseInt(quantityInput.value) || 0;
    if (quantity > 1) {
        quantityInput.value = quantity - 1;
    }
}

function addToCart(productId, priceClp, priceUsd) {
    const quantityInput = document.getElementById(`quantity_${productId}`);
    const quantity = parseInt(quantityInput.value) || 1; // Set default quantity to 1 if not provided

    fetch('/add_to_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ productId: productId, quantity: quantity })
    }).then(response => {
        if (response.ok) {
            return response.json(); // Return the JSON response
        } else {
            throw new Error('Error al agregar el producto al carrito');
        }
    }).then(data => {
        // Show additional product details in the UI
        document.getElementById('productName').innerText = data.product.name;
        document.getElementById('productPrice').innerText = `$${priceClp}`;
        document.getElementById('price_usd').innerText = `$${priceUsd}`; // Show the price in USD
        document.getElementById('productQuantity').innerText = quantity;
        // Show the modal
        var modal = new bootstrap.Modal(document.getElementById('addToCartModal'));
        modal.show();
    }).catch(error => {
        console.error('Error al agregar el producto al carrito:', error);
    });
}

function updateQuantity(productId, quantity) {
    fetch('/update_quantity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ productId: productId, quantity: parseInt(quantity) })
    }).then(response => {
        if (!response.ok) {
            throw new Error('Error al actualizar la cantidad del producto');
        } else {
            // Si la actualización es exitosa, puedes recargar la página para reflejar los cambios
            window.location.reload();
        }
    }).catch(error => {
        console.error('Error al actualizar la cantidad del producto:', error);
    });
}

function removeFromCart(productId) {
    fetch('/remove_from_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ productId: productId })
    }).then(response => {
        if (!response.ok) {
            throw new Error('Error al eliminar el producto del carrito');
        }
        // Recargar la página para reflejar los cambios
        location.reload();
    }).catch(error => {
        console.error('Error al eliminar el producto del carrito:', error);
    });
}


function showHideShippingForm() {
    var shippingForm = document.getElementById("shipping-form");
    var shippingMethodDescription = document.getElementById("shipping-method").options[document.getElementById("shipping-method").selectedIndex].text;
    if (shippingMethodDescription === "despacho") {
        shippingForm.style.display = "block";
    } else {
        shippingForm.style.display = "none";
    }
}

function showHidePaymentOptions() {
    var bankdetails = document.getElementById("bank-details");
    var checkoutButton = document.getElementById("checkout-button"); // Botón para pago con tarjeta
    var proceedPaymentButton = document.getElementById("proceed-payment-button"); // Botón para transferencia
    var paymentMethodDescription = document.getElementById("payment-method").options[document.getElementById("payment-method").selectedIndex].text;
    if (paymentMethodDescription === "transferencia") {
        bankdetails.style.display = "block";
        checkoutButton.style.display = "none"; // Ocultar el botón para pago con tarjeta
        proceedPaymentButton.style.display = "block"; // Mostrar el botón para transferencia
    } else {
        bankdetails.style.display = "none";
        checkoutButton.style.display = "block"; // Mostrar el botón para pago con tarjeta
        proceedPaymentButton.style.display = "none"; // Ocultar el botón para transferencia
    }
}
function proceedToSuccess() {
    // Realizar cualquier acción adicional si es necesario

    // Redirigir a la ruta success
    window.location.href = "/success";
}


