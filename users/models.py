from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    modified = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    class Meta:
        abstract = True
        ordering = ("-created",)


class UserProfile(AbstractUser, BaseModel):

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ("created",)
