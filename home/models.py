from django.db import models

# Create your models here.

class registro(models.Model):
    nombre = models.CharField(max_length=64)
    apellidop = models.CharField(max_length=64)
    apellidom = models.CharField(max_length=64)
    correo = models.EmailField(max_length=64)
    mensaje = models.CharField(max_length=1000)
