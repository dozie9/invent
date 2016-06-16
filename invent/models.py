from django.db import models
from django.contrib.auth.models import User

# Create your models here.
type = (('U','User'), ('S', 'Super User'))
htype = (('D','D'), ('S', 'S'))

class Location(models.Model):
    state = models.CharField(max_length=25)
    local_govt = models.CharField(max_length=25)
    user = models.OneToOneField(User)

class History(models.Model):
    total_volume = models.IntegerField(max_length=20)
    sold_volume = models.IntegerField(max_length=20)
    total_amount = models.FloatField()
    amount = models.FloatField()
    types = models.CharField(max_length=2,choices=htype)

    date = models.DateTimeField(auto_created=True, auto_now=True)

    locale = models.ForeignKey(Location)

class MemberType(models.Model):
    profile = models.CharField(max_length=20, choices=type)
    user = models.ForeignKey(User)

class Invent(models.Model):
    invent = models.IntegerField()
    amount = models.IntegerField()
    date = models.DateTimeField(auto_created=True, auto_now=True)
    user = models.ForeignKey(User)

class PerLitre(models.Model):
    perLitre = models.FloatField()
    date = models.DateTimeField(auto_created=True, auto_now=True)
    user = models.ForeignKey(User)
