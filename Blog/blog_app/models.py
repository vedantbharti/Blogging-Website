from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
import misaka
from django.contrib.auth import get_user_model
User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    publish_date = models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    def approveComment(self):
        return self.comments.filter(approve_comment=True)

    def get_absolute_url(self):
        return reverse("blog_app:post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

    def snippet(self):
        return self.text[:300] + '...'

class Comment(models.Model):
    post = models.ForeignKey('blog_app.Post',related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=150)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    approve_comment = models.BooleanField(default=False)

    def approve(self):
        self.approve_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("blog_app:post_list")

    def __str__(self):
        return self.text
