# Generated by Django 5.0.6 on 2024-10-21 22:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offres', '0010_panier_prix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offre',
            name='evenement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offres', to='offres.evenement'),
        ),
    ]
