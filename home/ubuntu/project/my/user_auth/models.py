from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add any extra fields here. For now, we'll keep it simple.
    # The previous task context mentioned a CustomUser, so we'll define it.
    pass

    def __str__(self):
        return self.email
