"""Demand model."""

# Django
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Validation parameters
validators = {'validators': [MinValueValidator(0), MaxValueValidator(163)],
              'blank': False}


class Demand(models.Model):
    """A Django model for representing an elevator demand."""

    moment = models.DateTimeField()
    source_floor = models.IntegerField(**validators)
    destination_floor = models.IntegerField(**validators)
    elevator = models.ForeignKey('elevator.Elevator', on_delete=models.CASCADE, null=True)
    rest_floor = models.IntegerField(**validators)
