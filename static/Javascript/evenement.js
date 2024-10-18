document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('sport-select').addEventListener('change', function () {
        var selectedSport = this.value;
        document.querySelectorAll('.carte').forEach(function (carte) {
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

        //Vérif 
        console.log(`Offfre ID: ${offreId}, Date sélectionnée: ${selectedDate}`);

        if (selectedDate) {
            //Vérif
            const url = `/ajouter_au_panier/${offreId}/${selectedDate}/`;
            console.log(`URL générée: ${url}`);

            //Envoyer une requête AJAX au serveur pour ajouter l'élément au panier
            fetch(url, {
                method: 'POST', //Utilisation de la methode post pour plus de sécurité
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ offreId: offreId, evenementId: selectedDate })
            })
                .then(response => {
                    console.log(response);
                    if (response.redirected) {
                        window.location.href = response.url;
                        return;
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        alert("L'offre a été ajoutée au panier.");
                        //Mettre à jour l'interface utilisateur si nécessaire
                        ajouterAuPanierClient(offreId, offreId, sportNom, selectedDate);
                    } else {
                        alert(data.message || "Erreur lors de l'ajout au panier.");
                    }
                })
                .catch(error => console.error('Erreur lors de la reqête AJAX :', error));
        } else {
            alert('Veuillez sélectionner une date.');
        }
    }

    //Fonction pour gérer l'ajout coté client
    function ajouterAuPanierClient(offreId, offreTitre, sportNom) {
        var dateSelect = document.getElementById('date-select-' + offreId);    
        var panierList = document.getElementById('panier-liste');
            if (panierList) {
                var li = document.createElement('li');
                li.setAttribute('data-offre-id', offreId);
                li.setAttribute('data-date-id', selectedDate);
                li.textContent = offreTitre + ' - ' + sportNom + ' - ' + dateSelect.options[dateSelect.selectedIndex].text;

                var removeButton = document.createElement('button');
                removeButton.textContent = 'Supprimer';
                removeButton.style.marginLeft = '10px';
                removeButton.onclick = function () {
                    supprimerDuPanier(li);
                };

                li.appendChild(removeButton);
                panierList.appendChild(li);
                updateTotal();
            } else {
                console.error('Panier non trouvé.');
            }
    }

    //Fonction pour obtenir le CSRF Token
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
    window.validerCommande = function () {
        fetch('/valider_commande/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => {
                if (response.redirected) {
                    //L'utilisateur n'est pas connecté, redirige vers la page de connexion
                    window.location.href = response.url;
                } else {
                    return response.json();
                }
            })
            .then(data => {
                if (data && data.success) {
                    //SI la commande est validée, redirige vers la page panier
                    window.location.href = data.redirect_url;
                } else if (data && data.message) {
                    //Si le panier est vide ou un autre problème est survenu
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Erreur lors de la validation de la commande :', error);
            });
    };
});
