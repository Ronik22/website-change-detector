from django.db import models

# Create your models here.

class Tasks(models.Model):
    DETECTION_TYPES = ((1,'Image'),(2,'HTML'),(3,'Text'))

    web_url = models.CharField(max_length=1000)
    partOf = models.CharField(max_length=1000, null=True, blank=True)
    detection_type = models.IntegerField(choices=DETECTION_TYPES)
    hasChanged = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.web_url}'