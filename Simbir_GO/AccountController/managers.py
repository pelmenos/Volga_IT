from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_("The username must be set"))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("isAdmin", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("isAdmin") is not True:
            raise ValueError(_("Admin must have isAdmin=True."))
        return self.create(username, password, **extra_fields)
