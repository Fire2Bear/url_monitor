# Generated by Django 3.1.3 on 2021-01-17 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_page_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(default=None, max_length=255, verbose_name='Nom de la page'),
        ),
    ]
