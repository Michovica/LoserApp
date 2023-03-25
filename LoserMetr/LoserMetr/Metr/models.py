from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=30)
    compleated = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])


class LoserValue(models.Model):
    
    
    value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    updatesCount = models.IntegerField(default=0)

    def save(self):
        # count will have all of the objects from the Aboutus model
        count = LoserValue.objects.all().count()
        # this will check if the variable exist so we can update the existing ones
        save_permission = LoserValue.has_add_permission(self)

        # if there's more than two objects it will not save them in the database
        if count < 2:
            super(LoserValue, self).save()
        elif save_permission:
            super(LoserValue, self).save()
            

    def has_add_permission(self):
        return LoserValue.objects.filter(id=self.id).exists()