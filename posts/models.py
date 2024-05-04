from django.db import models
from django.contrib.auth.models import User

from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post_image = models.ImageField(upload_to="images/", null=True, blank=True)
    # categories = models.ManyToManyField(Category, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title.replace(" ", "-"))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
