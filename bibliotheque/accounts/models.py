from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    ROLE_LECTEUR = 'lecteur'
    ROLE_BIBLIOTHECAIRE = 'bibliothecaire'
    ROLE_CHOICES = [
        (ROLE_LECTEUR, 'Lecteur'),
        (ROLE_BIBLIOTHECAIRE, 'Bibliothécaire'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_LECTEUR)

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'
