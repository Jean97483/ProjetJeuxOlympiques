document.addEventListener('DOMContentLoaded', function () {
    // Filtre des sports
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

    //Gestion du type d'offre
    let selectedTypeOffre = null;

    document.querySelectorAll('#type-offre-select').forEach(function(selectElement) {
        selectElement.addEventListener('change', function() {
            selectedTypeOffre = this.value;
        });
    });

    // Fonction pour ajouter un article au panier
    function ajouterAuPanier(offreId) {
        // Récupérer le type d'offre sélectionné
        var typeOffreSelect = document.getElementById('type-offre-select-' + offreId);
        var selectedTypeOffre = typeOffreSelect ? typeOffreSelect.value : null;

        //Vérifier si un type d'offre est sélectionné
        if (!selectedTypeOffre) {
            alert('Veuillez sélectionner un type d\'offre.');
            return;
        }

        //Récuperer la date sélectionné
        var dateSelect = document.getElementById('date-select-' + offreId);
        if (!dateSelect) {
            alert('Veuillez sélectionner une date valide.');
            return;
        }
        var selectedDate = dateSelect.value;
        //Vérification des données
        console.log(`Offfre ID: ${offreId}, Date sélectionnée: ${selectedDate}, Type Offre ID: ${selectedTypeOffre}`);

        if (selectedDate) {
            //Envoyer une requête AJAX au serveur pour ajouter l'élément au panier
            fetch(`/ajouter_au_panier/${offreId}/${selectedDate}/${selectedTypeOffre}/`, {
                method: 'POST', //Utilisation de la methode post pour plus de sécurité
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ offreId: offreId, evenementId: selectedDate, typeOffreId: selectedTypeOffre })
            })
                .then(response => response.json())
                .then(data => {
                    console.log("réponse du serveur:", data);
                    if (data.success) {
                        alert("L'offre a été ajoutée au panier.");
                        //Mettre à jour l'interface utilisateur si nécessaire
                        ajouterAuPanierClient(offreId, selectedTypeOffre);
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
