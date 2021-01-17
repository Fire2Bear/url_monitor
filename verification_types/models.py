from django.db import models

# Create your models here.
from users.models import BaseModel


class VerificationType(BaseModel):
    name = models.CharField(
        verbose_name="Nom du type de vérification",
        max_length=255,
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
