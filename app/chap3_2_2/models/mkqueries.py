from django.db import models

__all__ = (
    'Blog',
    'Author',
    'Entry',
)

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    """
    ## ManyToMany의 경우 add 이용해서 업데이트 (p.105)
    joe = Author.objects.create(name='Joe')
    entry.authors.all()
    entry.authors.add(joe)
    """
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Entry(models.Model):
    """
    ## ForeignKey 업데이트 경우 그냥 할당 (p.105)
    b = Blog(name='Beatles Blog', tagline='All the latest Beatles news')
    b.save()
    entry = Entry.objects.create(blog=b, headline='Test entry')
    entry.blog
    entry.blog.pk
    b2 = Blog.objects.create(name='Cheddar Talk')
    entry.blog = b2

    ## filters 이용해서 특정 objects retrieve하는 경우 (p.106)
    Entry.objects.create(blog=b, headline='2006 test entry', pub_date=date(2006, 1, 1))
    Entry.objects.filter(pub_date__year=2006)

    ## chaining filters 예시 (p.107)
    b = Blog.objects.create(name='lhy Blog')
    Entry.objects.create(blog=b, headline='What\'s up', pub_date=date(2020, 1, 1))
    Entry.objects.create(blog=b, headline='What 123', pub_date=date(2000, 1, 1))
    Entry.objects.create(blog=b, headline='Whattttttt', pub_date=date(2005, 2, 1))

    ## Everything inside a single filter() call vs. Successive filter() (p.111)
    b1 = Blog.objects.create(name='Lennon and 2008')
    b2 = Blog.objects.create(name='Lennon 2008 separate')

    Entry.objects.create(blog=b1, headline='Lennon', pub_date=date(2008, 1, 1))
    Entry.objects.create(blog=b2, headline='Fastcampus', pub_date=date(2008, 1, 1))
    Entry.objects.create(blog=b2, headline='Lennon', pub_date=date(2018, 2, 19))

    Blog.objects.filter(entry__headline__contains='Lennon', entry__pub_date__year=2008)
    Blog.objects.filter(entry__headline__contains='Lennon').filter(entry__pub_date__year=2008)

    ## 다른 fields간 values 비교 (p.112)
    b = Blog.objects.create(name='F blog')
    e1 = Entry.objects.create(blog=b, headline='F entry', n_comments=10, n_pingbacks=5)
    e1.n_comments = 10
    e1.n_pingbacks = 5
    e1.save()
    e2 = Entry.objects.create(blog=b, headline='F entry2', n_comments=5, n_pingbacks=10)
    Entry.objects.filter(n_comments__gt=F('n_pingbacks'))

    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    pub_date = models.DateField(blank=True, null=True)
    mod_date = models.DateField(auto_now=True)
    authors = models.ManyToManyField(Author, blank=True)
    n_comments = models.IntegerField(default=0)
    n_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.headline