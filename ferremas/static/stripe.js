var stripe = Stripe('pk_test_51PIEHJFngB2pMcgs3B2Pks8vye4gKHR9aMB59U1SHM950y7BA3UkaAqAxry5TAGE7HBIfsN7uBDctIeFovFvBXQW00KzTVO9zS');

document.getElementById('checkout-button').addEventListener('click', function () {
    fetch('/create-checkout-session', {
        method: 'POST',
        // headers: {
        //     'Content-Type': 'application/json'
        // },
        // body: JSON.stringify({
        //     products: {{ products|tojson }},
        //     total_clp: {{ total_clp }}
        // })
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (sessionId) {
        return stripe.redirectToCheckout({ sessionId: sessionId.id });
    })
    .then(function (result) {
        if (result.error) {
            alert(result.error.message);
        }
    })
    .catch(function (error) {
        console.error('Error:', error);
    });
});

