from django.db import models

# Create your models here.
from users.models import BaseModel


class Page(BaseModel):
    title = models.CharField(
        verbose_name="Titre de la vérification",
        max_length=255,
        default=None,
        blank=False,
        null=False,
    )

    url = models.CharField(
        verbose_name="Url à vérifier",
        max_length=255,
        default=None,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"
        ordering = ("title",)
