import datetime
from django.db import models

__all__ = (
    'Person',
)


class Person(models.Model):
    """
    3.2.1.3.2 Field options에서 choices 관련 (p.86-87)
    """
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    # p = Person(first_name='Sangwon', last_name='Han', birth_date=date(1981, 11, 17), shirt_size='L')
    # p.save()
    # p.shirt_size
    # p.get_shirt_size_display()
    shift_size = models.CharField(max_length=1, choices=SHIRT_SIZES)


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