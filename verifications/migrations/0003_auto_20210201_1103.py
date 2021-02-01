# Generated by Django 3.1.3 on 2021-02-01 10:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20210201_1103'),
        ('verification_types', '0014_auto_20210201_1103'),
        ('verifications', '0002_verification_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.page', verbose_name='Page à vérifier'),
        ),
        migrations.AlterField(
            model_name='verification',
            name='verification_option',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Option de vérification'),
        ),
        migrations.AlterField(
            model_name='verification',
            name='verification_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='verification_types.verificationtype', verbose_name='Type de vérification'),
        ),
    ]