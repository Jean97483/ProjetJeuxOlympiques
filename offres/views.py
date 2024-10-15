#myapp/views.py
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .models import Offre, Sport, Evenement, Panier
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse

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
    return render(request, 'register.html', {'form': form})

#Vue pour la connexion personnalisée
class CustomLoginView(LoginView):
    template_name = 'login.html'

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
    panier_items = Panier.objects.filter(user=request.user)
    total = sum(item.offre.prix * item.quantite for item in panier_items)
    return render(request, 'panier.html', {'panier_item': panier_items, 'total': total})

@login_required
def ajouter_au_panier(request, offre_id, evenement_id):
    offre = Offre.objects.get(id=offre_id)
    evenement = Evenement.objects.get(id=evenement_id)
    panier_item, created = Panier.objects.get_or_create(user=request.user, offre=offre, evenement=evenement)
    if not created:
        panier_item.quantite += 1
        panier_item.save()
    return redirect('panier')

@login_required
def supprimer_du_panier(request, panier_item_id):
    panier_item = Panier.objects.get(id=panier_item_id)
    if panier_item.user == request.user:
        panier_item.delete()
    return redirect('panier')