# Generated by Django 5.0.6 on 2024-10-19 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offres', '0006_offre_evenement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offre',
            name='prix',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
