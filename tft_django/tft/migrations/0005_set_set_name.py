# Generated by Django 5.0.2 on 2024-03-06 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tft', '0004_patch_revival_set_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='set_name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
