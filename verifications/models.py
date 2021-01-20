from django.db import models

# Create your models here.
from pages.models import Page
from users.models import BaseModel
from verification_types.models import VerificationType


class Verification(BaseModel):
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        verbose_name="Page à vérifier",
        db_index=True,
        null=False,
        blank=False,
        default=None
    )

    verification_type = models.ForeignKey(
        VerificationType,
        on_delete=models.CASCADE,
        verbose_name="Type de vérification",
        db_index=True,
        null=False,
        blank=False,
        default=None
    )

    verification_option = models.CharField(
        verbose_name="Option de vérification",
        max_length=255,
        default=None,
        blank=True,
        null=True,
    )

    description = models.TextField(
        verbose_name="Description",
        default=None,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.page.title + " " + str(self.verification_type)

    class Meta:
        verbose_name = "Vérification"
        verbose_name_plural = "Vérifications"
        ordering = ("page", "verification_type")
