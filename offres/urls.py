#offres/urls.py
from django.urls import path
from . import views
from .views import panier, ajouter_au_panier, supprimer_du_panier, register, CustomLoginView, custom_logout_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('evenement/', views.evenement, name='evenement'),
    path('panier/', panier, name='panier'),
    path('ajouter_au_panier/<int:offre_id>/<int:evenement_id>/', ajouter_au_panier, name='ajouter_au_panier'),
    path('supprimer_du_panier/<int:panier_item_id>/', supprimer_du_panier, name='supprimer_du_panier'),
    path('inscription/', register, name='inscription'),
    path('connexion/', CustomLoginView.as_view(), name='connexion'),
    path('deconnexion/', custom_logout_view, name='deconnexion'),

]

