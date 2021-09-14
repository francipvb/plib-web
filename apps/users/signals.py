from typing import Any, Type

from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import User


@receiver(pre_save, sender=User)
def _create_superuser(sender: Type[User], instance: User, *args: Any, **kwargs: Any) -> None:
    if kwargs["raw"]:
        return

    if not User.objects.all().exists():
        instance.is_superuser = True
        instance.is_staff = True
