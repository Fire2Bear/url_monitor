# Generated by Django 3.1.3 on 2021-01-17 23:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('verification_types', '0012_verificationtype_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='verificationtype',
            old_name='code',
            new_name='identifiant',
        ),
    ]
