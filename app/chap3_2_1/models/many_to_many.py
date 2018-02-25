from django.db import models

__all__ = (
    'PersonB',
    'Group',
    'Membership',
    'FacebookUser',
    'InstagramUser',
    'TwitterUser',
    'Relation',
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

    ## A가 B의 소식을 받고 싶다
        -> A가 B를 'follow'한다
        -> A의 'following'  목록에 B가 추가
        -> B의 'follower' 목록에 A가 추가
        -> A는 B의 follower
        -> A -> B

    u1, u2, u3  = [InstagramUser.objects.create(name=name) for name in ['이한영', '박보영', '아이유']]
    u1.following.add(u2)
    u1.following.add(u3)

    u1.following.all() # u2, u3 모두
    u2.following.all() # 아무도 없음
   """
    name = models.CharField(max_length=50)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        # 역방향 참조시 그냥 편한 related_name 지정해주는게 나
        # def followers(self):
        #     return self.instagramuser_set.all()
    )

    def __str__(self):
        return self.name


class TwitterUser(models.Model):
    """
    (p.91)
    u1, u2, u3, u4 = [TwitterUser.objects.create(name=name) for name in ['이한영', '박보영', '아이유', '수지']]
    ## add, create, set을 이용해 relationships 만들 수 없음
    ## 대신 instance 만들어야

    Relation.objects.create(from_user=u1, to_user=u2, type='f')
    Relation.objects.create(from_user=u1, to_user=u4, type='b')

    # u1에서의 relations에서 type이 'f'인 관
    u1.relations_by_from_user.filter(type='f')
    Relation.objects.all().filter(from_user=u1, type='f')

    u1.relations_by_from_user.create(to_user=u3, type='f')
    u1.following()
    """
    name = models.CharField(max_length=50)
    relations = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Relation',
        related_name='+',
    )

    def __str__(self):
        return self.name

    @property
    def following(self):
        """
        내가 follow하고 있는 TwitterUser목록을 가져옴
        """
        # 내가 from_user이며, type이 팔로잉인 Relation의 쿼리
        following_relations = self.relations_by_from_user.filter(
            type=Relation.RELATION_TYPE_FOLLOWING,
        )
        # 위에서 정제한 쿼리셋에서 'to_user'값만 리스트로 가져옴 (내가 팔로잉하는 유저의 pk리스트)
        following_pk_list = following_relations.values_list('to_user', flat=True)
        # TwitterUser테이블에서 pk가
        # 바로 윗줄에서 만든 following_pk_list (내가 팔로잉하는 유저의 pk리스트)
        #   에 포함되는 User목록을 following_users변수로 할당
        following_users = TwitterUser.objects.filter(pk__in=following_pk_list)
        return following_users

    @property
    def followers(self):
        pk_list = self.relations_by_to_user.filter(
            type=Relation.RELATION_TYPE_FOLLOWING).values_list('from_user', flat=True)
        return TwitterUser.objects.filter(pk__in=pk_list)

    @property
    def block_users(self):
        """
        내가 block하고 있는 TwitterUser목록을 가져옴
        """
        pk_list = self.relations_by_from_user.filter(
            type=Relation.RELATION_TYPE_BLOCK).values_list('to_user', flat=True)
        return TwitterUser.objects.filter(pk__in=pk_list)

    def follow(self, to_user):
        """
        to_user에 주어진 TwitterUser를 follow함
        """
        # self.relations_by_from_user.filter(to_user=to_user).delete()
        self.relations_by_from_user.create(
            to_user=to_user,
            type=Relation.RELATION_TYPE_FOLLOWING,
        )

    def block(self, to_user):
        """
        to_user에 주어진 TwitterUser를 block함
        """
        # self.relations_by_from_user.filter(to_user=to_user).delete()
        self.relations_by_from_user.create(
            to_user=to_user,
            type=Relation.RELATION_TYPE_BLOCK,
        )


class Relation(models.Model):
    RELATION_TYPE_FOLLOWING = 'f'
    RELATION_TYPE_BLOCK = 'b'
    CHOICES_TYPE = (
        (RELATION_TYPE_FOLLOWING, '팔로잉'),
        (RELATION_TYPE_BLOCK, '차단'),
    )
    from_user = models.ForeignKey(
        TwitterUser,
        on_delete=models.CASCADE,
        # 여기서 related_name 없으면 에러
        # t1.relation_set
        # t2.relation_set이기 때문에 related_name 있어
        # r1.from_user
        related_name='relations_by_from_user',
    )
    to_user = models.ForeignKey(
        TwitterUser,
        on_delete=models.CASCADE,
        related_name='relations_by_to_user',
    )
    type = models.CharField(max_length=1, choices=CHOICES_TYPE)
    # 만들어지는 순간 vs. auto_now는 수정할 때마
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            # from_user와 to_user의 값이 이미 있을 경우
            # DB에 중복 데이터 저장을 막음
            # ex) from_user가 1, to_user가 3인 데이터가 이미 있다면
            #       두 항목의 값이 모두 같은 또 다른 데이터가 존재할 수 없음
            ('from_user', 'to_user'),
        )