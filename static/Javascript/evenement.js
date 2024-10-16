document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('sport-select').addEventListener('change', function() {
        var selectedSport = this.value;
        document.querySelectorAll('.carte').forEach(function(carte) {
            if (selectedSport === '' || carte.getAttribute('data-sport-id') === selectedSport) {
                carte.style.display = 'block';
            } else {
                carte.style.display = 'none';
            }
        });
    });

    function ajouterAuPanier(offreId, offreTitre, sportNom) {
        var dateSelect = document.getElementById('date-select-' + offreId);
        var selectedDate = dateSelect.value;
        if (selectedDate) {
            var panierList = document.getElementById('panier-liste');
            if (panierList) {
                var li = document.createElement('li');
                li.setAttribute('data-offre-id', offreId);
                li.setAttribute('data-date-id', selectedDate);
                li.textContent = offreTitre + ' - ' + sportNom + ' - ' + dateSelect.options[dateSelect.selectedIndex].text;
                
                var removeButton = document.createElement('button');
                removeButton.textContent = 'Supprimer';
                removeButton.style.marginLeft = '10px';
                removeButton.onclick = function() {
                    supprimerDuPanier(li);
                };

                li.appendChild(removeButton);
                panierList.appendChild(li);
                updateTotal();
            } else {
                console.error('Panier non trouvé.');
            }
        } else {
            alert('Veuillez sélectionner une date.');
        }
    }

    function supprimerDuPanier(element) {
        element.remove();
        updateTotal();
    }

    function updateTotal() {
        var total = 0;
        var panierList = document.getElementById('panier-liste');
        if (panierList) {
            var items = panierList.getElementsByTagName('li');
            total = items.length;
            document.getElementById('panier-total').textContent = total;
        } else {
            console.error('Panier non trouvé.')
        }
    }

    window.ajouterAuPanier = ajouterAuPanier;
    window.validerCommande = function() {
        fetch('/valider_commande/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.status === 403) {
                //L'utilisateur n'est pas connecté, redirige vers la page de connexion
                window.location.href = '/connexion/';
            } else {
                return response.json();
            }
        })
        .then(data => {
            if (data.success) {
                //SI la commande est validée, redirige vers la page panier
                window.location.href = '/panier/';
            } else {
                //Si le panier est vide ou un autre problème est survenu
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Erreur lors de la validation de la commande :', error);
        });
    };
});
