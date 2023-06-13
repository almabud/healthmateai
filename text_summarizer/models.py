from django.db import models

from healthmateai.models import DateModel
from patient.models import Patient


class SummarizeRequest(DateModel):
    conversation = models.JSONField()
    summarize = models.TextField()
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, blank=True
    )
