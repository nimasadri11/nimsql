from django.db import models
from django.contrib.auth.models import User

class Creator(User):
    page_name = models.CharField(max_length=30)
    url_name = models.CharField(max_length=30)
    profile_image = models.CharField(max_length=200)
    banner_image = models.CharField(max_length=200)


    def __str__(self):
        return self.first_name + " " + self.last_name




class Video(models.Model):
    title = models.CharField(max_length=200)
    creator = models.ManyToManyField(Creator)
    uploadtime = models.DateTimeField()
    url = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.title