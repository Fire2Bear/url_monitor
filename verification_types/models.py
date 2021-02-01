from django.db import models

# Create your models here.
from users.models import BaseModel


class VerificationType(BaseModel):
    name = models.CharField(
        verbose_name="Type de vérification",
        max_length=255,
        blank=False,
        null=False,
    )

    description = models.TextField(
        verbose_name="Description du type de vérification",
        max_length=1000,
        default=None,
        blank=True,
        null=True,
    )

    identifiant = models.CharField(
        verbose_name="Identifiant unique",
        unique=True,
        max_length=10,
        default=None,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Type de vérification"
        verbose_name_plural = "Types de vérification"
        ordering = ("name",)
