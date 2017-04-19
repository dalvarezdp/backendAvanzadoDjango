from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Post(models.Model):

    owner = models.ForeignKey(User)
    image = models.FileField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.image
