from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
import secrets
import hashlib

class CustomUser(AbstractUser):
    unique_key = models.CharField(max_length=64, unique=True, default=uuid.uuid4().hex, editable=False)
    purchase_key = models.CharField(max_length=64, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    final_key = models.CharField(max_length=255, null=True, blank=True)
   
    def generate_purchase_key(self):
        self.purchase_key = uuid.uuid4()
        self.save()

    def get_final_key(self):
        if self.purchase_key:
            return hashlib.sha256(f'{self.unique_key}{self.purchase_key}'.encode()).hexdigest()
        return str(self.unique.key)

    def save(self, *args, **kwargs):
        if not self.unique_key:
            self.unique_key= secrets.token_urlsafe(16)
        if self.purchase_key:
            self.final_key = self.get_final_key()
        super().save(*args, **kwargs)

    def generate_unique_key(self):
        return str(uuid.uuid4())
