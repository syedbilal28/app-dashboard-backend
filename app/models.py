from django.db import models
from django.contrib.auth.models import User

class App(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__ (self):
        return self.name