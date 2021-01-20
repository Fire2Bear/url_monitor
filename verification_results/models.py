from django.db import models

from users.models import BaseModel
from verifications.models import Verification


class VerificationResult(BaseModel):
    verification = models.ForeignKey(
        Verification,
        on_delete=models.CASCADE,
        verbose_name="Vérification",
        db_index=True,
        null=False,
        blank=False,
        default=None
    )

    success = models.BooleanField(
        verbose_name="Succès",
        default=None,
        blank=False,
        null=False,
    )

    date = models.DateTimeField(
        verbose_name="Date et heure de la vérification",
        default=None,
        blank=False,
        null=False,
    )

    description = models.TextField(
        verbose_name="Description",
        default=None,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.date) \
               + ", " \
               + str(self.verification) \
               + " ===> " \
               + ("ERROR ❌" if not self.success else " SUCCESS ✅")

    class Meta:
        verbose_name = "Résultat de vérification"
        verbose_name_plural = "Résultat des vérifications"
        ordering = ("date", "verification__verification_type")
