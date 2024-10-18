#myapp/models.py
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Sport(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Offre(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)

    def __str__(self):
        return self.titre

class Evenement(models.Model):
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.offre.titre} - {self.date}"   
    
class Panier(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__ (self):
        return f"{self.offre.titre} - {self.evenement.date} - {self.quantite}"