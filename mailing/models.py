from django.db import models

# Create your models here.
from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, blank=True)
    is_subscribed = models.BooleanField(default=True)

    def __str__(self):
        return self.email