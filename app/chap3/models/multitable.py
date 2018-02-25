from django.db import models

__all__ = (
    'Other',
    'Place',
    'Restaurant',
)

class Other(models.Model):
    """
    o = Other.objects.create()
    p1 = Place.objects.create(name='제노', address='신사역')
    r1 = Restaurant.objects.create(name='맥도날드', address='신사역')

    p1.other = o
    p1.save()

    r1.other = o
    r1.save()

    # Place와 Restaurant 할당된 객체 목록 모두 보여줘
    o.places.all()
    """
    pass


class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)
    other = models.ForeignKey(
        Other,
        on_delete=models.SET_NULL,
        related_name='places',
        related_query_name='place',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.name} | {self.address}'


class Restaurant(Place):
    """
    Restaurant.objects.create(name='롯데리아', address='신사역')
    처럼 Restaurant에 바로 Place의 field를 써줄 수 있음
    """
    serves_hot_dog = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    nearby_places = models.ManyToManyField(
        Place,
        # related_name은 restaurant_set으로 default 지정
        # related_query_name이 default로는 restaurant이기 때문에 중복 발생
        related_query_name='near_restaurant',
    )

    def __str__(self):
        return f'Restaurant {self.name} | {self.address}'