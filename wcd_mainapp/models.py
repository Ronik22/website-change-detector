from django.db import models
from accounts.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Tasks(models.Model):
    DETECTION_TYPES = ((1,'Image'),(2,'HTML'),(3,'Text'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    web_url = models.CharField(max_length=1000)
    partOf = models.CharField(max_length=1000, default="full")
    detection_type = models.IntegerField(choices=DETECTION_TYPES, default=3)
    threshold = models.FloatField(default=1.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'web_url'], name="%(app_label)s_%(class)s_unique")
        ]

    def __str__(self):
        return f'{self.id} - {self.web_url}'