from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from django.contrib.auth.models import AbstractUser


@python_2_unicode_compatible
class User(AbstractUser):
    name = models.CharField(blank=True, max_length=255)

    def social_avatar(self):
        return self.socialaccount_set.first().get_avatar_url()
