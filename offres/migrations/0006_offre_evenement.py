# Generated by Django 5.0.6 on 2024-10-19 18:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offres', '0005_offre_prix'),
    ]

    operations = [
        migrations.AddField(
            model_name='offre',
            name='evenement',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='offres', to='offres.evenement'),
        ),
    ]
