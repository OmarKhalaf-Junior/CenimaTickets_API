from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token

# Create your models here.
class Movie(models.Model):
    hall = models.CharField(max_length=5)
    movie = models.CharField(max_length=50)
    date = models.DateField(blank= True, null= True)


class Guest(models.Model):
    guest_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=11)


class Reservation(models.Model):
    guest = models.ForeignKey(Guest, related_name='reservation', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='reservation', on_delete=models.CASCADE)



## After The User is Created ... Generate His/Her Token.
@receiver(post_save, sender= settings.AUTH_USER_MODEL)
def Create_Token(created, instance, sender, **kwargs):
    if created:
        Token.objects.create(user= instance)

