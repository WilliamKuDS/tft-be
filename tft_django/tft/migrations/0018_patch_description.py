# Generated by Django 5.0.2 on 2024-05-22 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tft', '0017_alter_patch_date_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='patch',
            name='description',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
