from django.db import models

__all__ = (
    'PersonA',
    'Item',
    'Fruit',
    'Food',
)

class PersonA(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Item(models.Model):
    """
    3.2.1.7.1. Abstract base classes (p.96-98)

    Person에서 Fruit나 Food로 갈때 related_name이 겹치기 때문에 error

    pby = PersonA.objects.create(name='박보영')
    iu = PersonA.objects.create(name='아이유')
    apple = Fruit.objects.create(name='사과', persona=iu)
    banana = Fruit.objects.create(name='바나나', persona=iu)
    banana_cake = Food.objects.create(name='바나나 팬케이크', persona=iu)
    banana_bread = Food.objects.create(name='바나나 빵', persona=iu)
    banana_juice = Food.objects.create(name='바나나 주스', persona=iu)
    dragon = Food.objects.create(name='용과', persona=iu)

    Fruit.objects.values_list('name', flat=True)
    Food.objects.values_list('name', flat=True)

    apple.persona


    # class여부 알 수 있는
    # 지금 실행되고 있는 모듈 안에서 속성 찾기
    sys.modules['__name__']

    # getattr은 동적으로 객체의 속성 가져올 수 있는
    for attr in dir():
        if inspect.isclass(getattr(sys.modules['__name__'], attr):
            print(f'{attr} is class')
        else:
            print(f'{attr} is not class')

    """
    persona = models.ForeignKey(
        PersonA,
        on_delete=models.CASCADE,
        # iu.chap3_fruit_related
        # related_name='%(app_label)s_%(class)s_related',
        # related_query_name='%(app_label)s_%(class)ss',

        # PersonA.objects.filter(items__name__contains='바나나')
        # Fruit과 Food 구분 안하고 모두 일치 결과 반환
        # related_query_name='items',

        # related_name='items',
        # related_query_name='item',
    )

    class Meta:
        abstract = True


class Fruit(Item):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Food(Item):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name