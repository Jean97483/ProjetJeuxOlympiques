document.getElementById('proceder-paiement').addEventListener('click', function() {
    fetch('/proceder_paiement/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Paiement réussi ! Votre e-ticket a été envoyé.");
            window.location.href = data.redirect_url;
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error("Erreur lors du paiement :, error");
        alert("Erreur lors du paiement. Veuillez réessayer.");
    });
});