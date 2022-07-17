from django.db import models
from django.conf import settings


class ServerWord(models.Model):
    word = models.CharField(max_length=50, unique=True)
    translate = models.CharField(max_length=50)
    word_example = models.TextField(max_length=300)

    def __str__(self):
        return self.word


class UserServerWord(models.Model):
    word = models.ForeignKey(ServerWord, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_add = models.DateField(auto_now_add=True)



