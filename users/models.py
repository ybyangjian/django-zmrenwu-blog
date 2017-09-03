from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class User(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    email_bound = models.BooleanField(default=False)

    def social_avatar(self):
        if self.socialaccount_set.exists():
            return self.socialaccount_set.first().get_avatar_url()
        return ''
