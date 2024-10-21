document.addEventListener('DOMContentLoaded', function() {
    function procederAuPaiement() {
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
    }

    // écouteur d'évènement pour le boutton
    document.getElementById('proceder-paiement').addEventListener('click', procederAuPaiement);
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}