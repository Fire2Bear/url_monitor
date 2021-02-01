# Generated by Django 3.1.3 on 2021-02-01 10:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifications', '0003_auto_20210201_1103'),
        ('verification_results', '0003_auto_20210120_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationresult',
            name='verification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='verifications.verification', verbose_name='Vérification'),
        ),
    ]