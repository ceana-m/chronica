from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

# class Book(models.Model):
#     pass

class Movie(models.Model):
    data = models.JSONField()

# class TVShow(models.Model):
#     pass

class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='all_lists')
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-time"]

    def __str__(self):
        return f"{ self.id }: { self.title }"

