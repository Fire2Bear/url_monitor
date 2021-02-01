from django.db import models

# Create your models here.
from users.models import BaseModel, UserProfile


class Page(BaseModel):

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        verbose_name="Utilisateur",
        db_index=True,
        null=False,
        blank=False,
    )

    title = models.CharField(
        verbose_name="Nom de la page",
        max_length=255,
        blank=False,
        null=False,
    )

    url = models.CharField(
        verbose_name="Url à vérifier",
        max_length=255,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"
        ordering = ("title",)
