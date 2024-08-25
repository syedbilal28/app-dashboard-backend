from django.db import models


class Plan(models.Model):
    FREE = 'Free'
    STANDARD = 'Standard'
    PRO = 'Pro'

    PLAN_CHOICES = [
        (FREE, 'Free Plan'),
        (STANDARD, 'Standard Plan'),
        (PRO, 'Pro Plan'),
    ]
    name = models.CharField(
        max_length=20, choices=PLAN_CHOICES, unique=True
    )
    price = models.PositiveIntegerField(default=0)

    def __str__ (self):
        return f"{self.name}: {self.price}"