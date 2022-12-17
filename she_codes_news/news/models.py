from email.mime import image
from django.contrib.auth import get_user_model
from django.db import models

USER = get_user_model()


class NewsStory(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        USER, on_delete=models.CASCADE, related_name='stories'
    )
    pub_date = models.DateTimeField()
    content = models.TextField()
    image = models.URLField(max_length=250, default="https://picsum.photos/600")
