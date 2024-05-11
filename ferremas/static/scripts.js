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

function addToCart(productId) {
    const quantityInput = document.getElementById(`quantity_${productId}`);
    const quantity = parseInt(quantityInput.value) || 1; // Set default quantity to 1 if not provided
    console.log('Producto ID:', productId, 'Cantidad:', quantity); // Add this line to print productId and quantity

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
        console.log('Producto agregado al carrito', data.product);
        // Show additional product details in the UI
        document.getElementById('productName').innerText = data.product.name;
        document.getElementById('productPrice').innerText = `$${data.product.price}`;
        // Show the modal
        var modal = new bootstrap.Modal(document.getElementById('addToCartModal'));
        modal.show();
    }).catch(error => {
        console.error('Error al agregar el producto al carrito:', error);
    });
}
