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
