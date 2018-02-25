from django.db import models

__all__ = (
    'Blog',
)


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()