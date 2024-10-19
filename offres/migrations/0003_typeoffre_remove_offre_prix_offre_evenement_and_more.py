# Generated by Django 5.0.6 on 2024-10-19 16:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offres', '0002_offre_prix'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeOffre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('Prix', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='offre',
            name='prix',
        ),
        migrations.AddField(
            model_name='offre',
            name='evenement',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='offres', to='offres.evenement'),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='offre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evenements', to='offres.offre'),
        ),
        migrations.AddField(
            model_name='offre',
            name='types_offre',
            field=models.ManyToManyField(to='offres.typeoffre'),
        ),
    ]