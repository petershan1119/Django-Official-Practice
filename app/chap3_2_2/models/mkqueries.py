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
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    headline = models.CharField(max_length=255)
    pub_date = models.DateField(blank=True, null=True)
    mod_date = models.DateField(auto_now=True)
    authors = models.ManyToManyField(Author, blank=True)
    n_comments = models.IntegerField(default=0)
    n_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.headline