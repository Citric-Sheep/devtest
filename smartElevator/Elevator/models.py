from django.db import models

# Create your models here.
class Data(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    time = models.TimeField(auto_now=False, auto_now_add=False)
    demandFloor = models.IntegerField()
    endFloor = models.IntegerField()
    people = models.IntegerField()
    active = models.BooleanField()

    def __str__(self) -> str:
        text = '{0} | {1} | {2} | {3} | {4} | {5} | {6} '
        return text.format(
            self.id, self.date, self.time, self.demandFloor,
            self.endFloor, self.people, self.active
        )
