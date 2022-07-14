from django.db import models


class ServerWord(models.Model):
    word = models.CharField(max_length=50, unique=True)
    translate = models.CharField(max_length=50)
    word_example = models.TextField(max_length=300)

    def __str__(self):
        return self.word
