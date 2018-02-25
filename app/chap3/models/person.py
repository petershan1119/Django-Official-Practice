import datetime
from django.db import models

__all__ = (
    'Person',
)


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()

    def baby_boomer_status(self):
        if self.birth_date < datetime.date(1945, 8, 1):
            return 'Pre-Boomer'
        elif self.birth_date < datetime.date(1965, 1, 1):
            return 'Baby Boomer'
        else:
            return 'Post-Boomer'

    @property
    def full_name(self):
        return '%s %s' % {self.first_name, self.last_name}