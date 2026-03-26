from django.db import models
from django.contrib.auth.models import AbstractUser

USER_ROLES = [
    ('admin', 'Admin User'),
    ('technician', 'Technician'),
    ('regular', 'Regular User'),
]

class User(AbstractUser):
    role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
        default='regular',
    )



def __str__(self):
    return self.username





