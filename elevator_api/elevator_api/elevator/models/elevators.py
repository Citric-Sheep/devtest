"""Elevator model."""

# Django
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Elevator(models.Model):
    """A Django model for representing an elevator."""

    name = models.CharField(max_length=50)
    current_floor = models.IntegerField(default=0)
    max_floors = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(163)])

    def __str__(self):
        """Returns a string representation of the elevator object."""
        return self.name
