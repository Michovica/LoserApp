from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime    


# Create your models here.
class Task(models.Model):
    
    owner = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=250)
    compleated = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    public = models.BooleanField(default=True)


class LoserValue(models.Model):
    
    owner = models.CharField(max_length=50, null=True)
    value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    updatesCount = models.IntegerField(default=0)
    lastFill = models.BooleanField(default=True)
    
