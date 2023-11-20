from django.db import models
from django.utils.text import slugify
from datetime import datetime
# Create your models here.

class Blog (models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    picture = models.ImageField(upload_to='post_images/', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    def save(self, *args, **kwargs):
        # Automatically generate the slug from the title if not provided
        if not self.slug:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            self.slug = f"{slugify(self.title)}-{timestamp}"
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.title} - {self.date_created}"

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.author}'s comment on {self.blog.title}"

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.email