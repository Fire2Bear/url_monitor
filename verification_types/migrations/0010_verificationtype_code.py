# Generated by Django 3.1.3 on 2021-01-17 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verification_types', '0009_remove_verificationtype_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationtype',
            name='code',
            field=models.CharField(default=None, max_length=4, unique=True, verbose_name='Identifiant unique du type de vérification'),
        ),
    ]
