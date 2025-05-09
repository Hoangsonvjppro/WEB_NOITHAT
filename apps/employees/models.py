from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    position = models.CharField(max_length=50)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.name
