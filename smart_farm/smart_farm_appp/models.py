from django.db import models

class Sistem(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

class Aktuator(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
