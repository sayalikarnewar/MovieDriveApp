# movies/models.py

from django.db import models
from django.contrib.auth.models import User
import uuid

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.title

class Collection(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    movies = models.ManyToManyField(Movie, related_name='collections')

    def __str__(self):
        return self.title