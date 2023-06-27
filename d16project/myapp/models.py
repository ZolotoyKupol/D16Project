from django.db import models
from django.contrib.auth.models import AbstractUser


class Person(AbstractUser):
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Ad(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Response(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'Response by {self.user.username} on {self.ad.title}'


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

