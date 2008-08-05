from django.db import models
from django.contrib.auth.models import User

class Lie(models.Model):
    lie = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return "/lies/%i/" % self.id

class Vote(models.Model):
    lie = models.ForeignKey(Lie)
    value = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Tag(models.Model):
    name = models.CharField(max_length=20)

