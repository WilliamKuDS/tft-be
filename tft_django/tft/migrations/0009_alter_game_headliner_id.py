# Generated by Django 5.0.2 on 2024-03-06 03:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tft', '0008_alter_game_headliner_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='headliner_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='headliner', to='tft.trait'),
        ),
    ]
