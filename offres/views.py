#myapp/views.py
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .models import Offre, Sport, Evenement, Panier
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404


#Vue pour l'inscription
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accueil')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

#Vue pour la connexion personnalisée
class CustomLoginView(LoginView):
    template_name = 'users/login.html'

def custom_logout_view(request):
    logout(request)
    return redirect(reverse('connexion'))

def accueil(request):
    return render(request, 'accueil.html')

def evenement(request):
    offres = Offre.objects.all()
    sports = Sport.objects.all()
    return render(request, 'evenements.html', {'offres': offres, 'sports': sports})
# Autres vues
@login_required
def panier(request):
    if request.user.is_authenticated:
        #Pour les utilisateurs connectés
        panier_items = Panier.objects.filter(user=request.user)
        total = sum(item.offre.prix * item.quantite for item in panier_items)
    else:
        #Pour les utilisateurs non connectés
        session_panier = request.session.get('panier', {})
        panier_items = []
        total = 0
        for key, value in session_panier.items():
            offre = get_object_or_404(Offre, id=value['offre_id'])
            evenement = get_object_or_404(Evenement, id=value['evenement_id'])
            quantite = value['quantite']
            total += offre.prix * quantite
            panier_items.append({'offre': offre, 'evenement': evenement, 'quantite': quantite})
    return render(request, 'panier.html', {'panier_items': panier_items, 'total': total})


@require_POST # Assure que la requête est de type POST
def ajouter_au_panier(request, offre_id, evenement_id):
    try:
        offre = get_object_or_404(Offre, id=offre_id)
        evenement = get_object_or_404(Evenement, id=evenement_id)

        # Vérifie si l'utilisateur est authentifié
        if request.user.is_authenticated:
            # Utilisateur connecté est associer au panier de l'utilisateur
            panier_item, created = Panier.objects.get_or_create(user=request.user, offre=offre, evenement=evenement)
            if not created:
                panier_item.quantite += 1
                panier_item.save()
        else:
            # Utilisateur non conecté - utiliser le session ID comme identifiant unique
            panier = request.session.get('panier', {})
            key = f"{offre_id}-{evenement_id}"

            if key in panier:
                panier[key]['quantite'] += 1
            else:
                panier[key] = {
                    'offre_id': offre_id,
                    'evenement_id': evenement_id,
                    'quantite': 1
                }
            
            #Mettre à jour la session
            request.session['panier'] = panier

        return JsonResponse({'success': True, 'message': 'Ajoute au panier'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def supprimer_du_panier(request, panier_item_id):
    panier_item = Panier.objects.get(id=panier_item_id)
    if panier_item.user == request.user:
        panier_item.delete()
    return redirect('panier')

@login_required(login_url='/users/login/')
def valider_commande(request):
    #Vérifie que le panier n'est pas vide
    panier_items = Panier.objects.filter(user=request.user)
    if not panier_items.exists():
        return JsonResponse({'success': False, 'message': 'Votre panier est vide.'})
    
    #Si le panier n'est pas vide, rediriger vers la page panier
    return JsonResponse({'success': True, 'redirect_url': reverse('panier')})
