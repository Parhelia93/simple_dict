from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.shortcuts import reverse


class ServerWord(models.Model):
    word = models.CharField(max_length=50, unique=True)
    translate = models.CharField(max_length=50)
    word_example = models.TextField(max_length=300)

    def __str__(self):
        return self.word


class UserWord(models.Model):
    word = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    date_add = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        value = str(self.user) + '-' + str(self.word)
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.word)

    def get_absolute_url(self):
        return reverse('user_word_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('user_word_detail_update_url', kwargs={'slug': self.slug})


class UserWordDetail(models.Model):
    translate = models.CharField(max_length=50)
    word_example = models.TextField(max_length=300)
    user_word = models.ForeignKey(UserWord, models.CASCADE)

    def __str__(self):
        return '{}'.format(self.translate)


