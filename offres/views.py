#myapp/views.py
import json
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .models import Offre, Sport, Evenement, Panier, TypeOffre
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
import qrcode
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile
from PIL import Image



#Vue pour l'inscription
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
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
    types_offres = TypeOffre.objects.all()
    evenements = Evenement.objects.select_related('offre').all()
    return render(request, 'evenements.html', {
        'offres': offres, 
        'sports': sports,
        'types_offres': types_offres,
        'evenements': evenements,
        })
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
            panier_items.append({'offre': offre, 'quantite': quantite})
    return render(request, 'panier.html', {'panier_items': panier_items, 'total': total})


@require_POST # Assure que la requête est de type POST
def ajouter_au_panier(request):
    try:
        # Extraire les données du formulaire POST
        offre_id = request.POST.get('offre_id')
        evenement_id = request.POST.get('evenement_id')
        type_offre_id = request.POST.get('type_offre')

        # Vérification que tous les champs sont présents
        if not (offre_id and evenement_id and type_offre_id):
            messages.error(request, "Informations manquantes pour ajouter au panier.")
            return HttpResponseRedirect(reverse('evenement'))

        # Vérifier les objets liés aux IDs
        offre = get_object_or_404(Offre, id=offre_id)
        evenement = get_object_or_404(Evenement, id=evenement_id)
        type_offre = get_object_or_404(TypeOffre, id=type_offre_id)

        # Vérifie si l'utilisateur est authentifié
        if request.user.is_authenticated:
            # Utilisateur connecté est associer au panier de l'utilisateur
            panier_item, created = Panier.objects.get_or_create(
                user=request.user, 
                offre=offre, 
                evenement=evenement,
                defaults={'quantite': 1, 'prix': type_offre.prix}
            )
            if not created:
                panier_item.quantite += 1
                panier_item.save()
        else:
            # Utilisateur non conecté - utiliser le session ID comme identifiant unique
            panier = request.session.get('panier', {})

            if str(offre_id) in panier:
                panier[str(offre_id)]['quantite'] += 1
            else:
                panier[str(offre_id)] = {
                    'offre_id': offre_id,
                    'evenement_id': evenement_id,
                    'quantite': 1,
                    'prix': float(type_offre.prix)
                }
            
            #Mettre à jour la session
            request.session['panier'] = panier

        # Ajout du message de confirmation
        messages.success(request, "L'offre a été ajoutée au panier !")
        return HttpResponseRedirect(reverse('evenement'))
    
    except Exception as e:
        # Capture d'erreur plus spécifique et retour à la page événements
        messages.error(request, f"Erreur lors de l'ajout au panier : {str(e)}")
        return HttpResponseRedirect(reverse('evenement'))

@login_required
def supprimer_du_panier(request, panier_item_id):
    panier_item = get_object_or_404(Panier, id=panier_item_id)
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

@login_required
@require_POST
def proceder_paiement(request):
    panier_items = Panier.objects.filter(user=request.user)

    if not panier_items.exists():
        return JsonResponse({'success': False, 'message': 'Votre panier est vide.'})
    
    #Simulation du paiement
    try:
        #Marquer les articles comme réservés ou payés
        for item in panier_items:
            item.payé = True
            item.save()

        #Générer un e-ticket et envoyer par mail
        generate_and_send_etickets(request.user, panier_items)

        # Vider le panier après paiement
        panier_items.delete()

        return JsonResponse({'success': True, 'redirect_url': reverse('confirmation')})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Erreur lors du paiement : {str(e)}"})
    

def generate_and_send_etickets(user, panier_items):
    for item in panier_items:
        #Créer un QR Code pour l'e-ticket
        qr = qrcode.make(f"{item.id}-{item.user.id}-{item.offre.titre}")
        qr_bytes = BytesIO()
        qr.save(qr_bytes, format='PNG')

        # Sauvegarder le QR Code comme fichier image
        qr_code = ContentFile(qr_bytes.getvalue())
        filename = f"eticket-{item.id}.png"

        #Envoyer l'e-ticket par email (en pièce jointe)
        subject = 'Votre E-ticket pour les Jeux Olympiques'
        message = f"Merci pour votre achat {user.username}. Voici votre e-ticket pour {item.offre.titre}."
        send_mail(
            subject,
            message,
            'votre-email@example.com',
            [user.email],
            fail_silently=False,
            html_message=message,
        )

@login_required
def scanner_ticket(request):
    if request.method == 'POST':
        qr_code_data = request.POST.get('qr_code_data')
        try:
            # Vérifier l'authenticité du QR code en le comparant à la base de données
            item_id, user_id, offre_titre = qr_code_data.split('-')
            item = Panier.objects.get(id=item_id, user__id=user_id)
            if item and item.payé:
                return JsonResponse({'success': True, 'message': 'E-ticket valide !'})
            else: 
                return JsonResponse({'success': False, 'message': 'E-ticket invalide ou non payé!'})
        except Exception:
            return JsonResponse({'success': False, 'message': 'Erreur lors de la vérification du ticket.'})
        