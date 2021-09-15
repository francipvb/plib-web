from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Represents an user."""

    avatar = models.ImageField(_("user avatar"), upload_to="photos")

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
