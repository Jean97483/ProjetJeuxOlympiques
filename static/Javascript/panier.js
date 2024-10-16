function validerCommande() {
    fetch('/valider_commande/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            //Redirige vers la page de paiement
            window.location.href = '/paiement/';
        } else {
            alert(data.message); //Message si le panier est vide
        }
    })
    .catch(error => {
        console.error('Erreur lors de la validation de la commande :', error);
    });
}