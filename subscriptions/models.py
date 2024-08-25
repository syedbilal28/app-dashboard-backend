from django.db import models
from django.utils import timezone

from app.models import App
from plans.models import Plan


class Subscription(models.Model):
    app = models.OneToOneField(App, null=True, blank=True, on_delete=models.SET_NULL)
    plan = models.ForeignKey(Plan, null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Subscription for {self.app.name} - {self.plan.name}"

    def cancel_subscription(self):
        self.is_active = False
        self.end_date = timezone.now()
        self.save()
