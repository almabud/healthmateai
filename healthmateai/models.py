"""
This file contains the global abstract models.
"""
import uuid

from django.db import models


class DateModel(models.Model):
    """
    Abstract model that stores a created and updated date for each object.
    """

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.created_at)
