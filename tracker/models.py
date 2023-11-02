from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Media(models.Model):
    TYPE_CHOICES = [
        ("Movie", "Movie"),
        ("TV", "TV"),
        ("Book", "Book")
    ]
    obj_id = models.IntegerField()
    media_type = models.CharField(max_length=5, choices=TYPE_CHOICES, default='')
    data = models.JSONField()

    class Meta:
        verbose_name_plural = "Media"

    def __str__(self):
        return f"{ self.id }: [{ self.obj_id }] { self.media_type }"
    
    def serialize(self):
        return {
            "id": self.id,
            "obj_id": self.obj_id,
            "media_type": self.media_type,
            "data": self.data
        }

class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='all_lists')
    title = models.CharField(max_length=50, blank=True)
    description = models.TextField(max_length=500, blank=True)
    media = models.ManyToManyField(Media, related_name='all_appearances')
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-time"]

    def __str__(self):
        return f"{ self.id }: { self.title }"
    
    def serialize(self):
        media = []
        for i in self.media.all():
            item = {
                "type": i.media_type,
                "data": i.data
            }
            media.append(item)
        return {
            "id": self.id,
            "user": self.user.username,
            "title": self.title,
            "description": self.description,
            "media": media
        }
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='all_user_reviews')
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    text = models.TextField(max_length=1000, blank=True)
    media = models.ForeignKey(Media, on_delete=models.PROTECT, related_name='all_media_reviews')
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.text == '':
            return f"{ self.id }: { self.user } wrote ({self.rating}) [no text provided]"
        return f"{ self.id }: { self.user } wrote ({self.rating}) { self.text }"
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "rating": self.rating,
            "text": self.text,
            "type": self.media.media_type,
            "media": self.media
        }


