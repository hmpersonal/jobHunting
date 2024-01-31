from django.db import models

# Create your models here.
class AiAnalysisLog(models.Model):
    autoIncId = models.IntegerField()
    imagePath = models.CharField(max_length=255)
    success = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    cls = models.IntegerField()
    confidence = models.DecimalField(max_digits=5, decimal_places=4)
    requestTimestamp = models.IntegerField()
    responseTimeStamp = models.IntegerField()

