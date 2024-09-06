from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Posts(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    date_time = models.DateTimeField()
