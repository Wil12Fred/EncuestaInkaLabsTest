from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models

class CustomUserManager(UserManager):

    def get_by_natural_key(self, username):
        return self.get(
            models.Q(**{self.model.USERNAME_FIELD: username}) |
            models.Q(**{self.model.EMAIL_FIELD: username})
        )

class User(AbstractUser):
    objects = CustomUserManager()
