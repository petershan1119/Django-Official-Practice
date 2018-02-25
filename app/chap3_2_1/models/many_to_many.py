from django.db import models

__all__ = (
    'PersonB',
    'Group',
    'Membership',
    'FacebookUser',
    'InstagramUser',
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
    "two foreign keys to the same model are permitted, but they will be treated
    as the two (different) sides of the many-to-many relationship" (p.90)

    f1, f2, f3  = [FacebookUser.objects.create(name=name) for name in ['이한영', '박보영', '아이유']]
    f1.friends.add(f2)
    f1.friends.all()
    f2.friends.all()

    """
    name = models.CharField(max_length=50)
    friends = models.ManyToManyField('self')

    # list comprehension 대신 query set이용해서
    def __str__(self):
        friends_string = ', '.join(self.friends.values_list('name', flat=True))
        return '{name} (친구: {friends})'.format(
            name=self.name,
            friends=friends_string,
        )



class InstagramUser(models.Model):
    """
    "When defining a many-to-many relationship from a model to itself, using an intermediary model,
    you must use 'symmetrical=False'. (p. 90)
    """
    name = models.CharField(max_length=50)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
    )

    def __str__(self):
        return self.name