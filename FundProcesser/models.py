from django.db import models

# Create your models here.


class CSV_FILE(models.Model):
    RawFile = models.FileField(upload_to= 'RawFiles')