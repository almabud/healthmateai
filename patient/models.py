from django.db import models

from healthmateai.models import DateModel


class Patient(DateModel):
    name = models.CharField(max_length=50)
