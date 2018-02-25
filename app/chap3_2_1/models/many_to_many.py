from django.db import models

__all__ = (
    'PersonB',
    'Group',
    'Membership',
    'FacebookUser',
)


class PersonB(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(PersonB, through='Membership')

    def __str__(self):
        return self.name


class Membership(models.Model):
    personb = models.ForeignKey(PersonB, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)


class FacebookUser(models.Model):
    """
    (p.90)
    """
    name = models.CharField(max_length=50)
    friends = models.ManyToManyField('self')

    def __str__(self):
        return self.name