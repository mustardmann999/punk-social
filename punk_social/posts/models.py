from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
import misaka

from groups.models import Group

# Connect post to current user
User = get_user_model()

### Post models ###

class Post(models.Model):
    user = models.ForeignKey(User,related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    content_html = models.TextField(editable=False)
    date_posted = models.DateTimeField(default=timezone.now)
    group = models.ForeignKey(Group,related_name='posts',null=True,blank=True)

    def __str__(self):
        return self.content

    def save(self,*args,**kwargs):
        self.content_html = misaka.html(self.content)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('posts:detail',kwargs={'username':self.user.username,
                                                'pk':self.pk})

    class Meta:
        # Ordered by descending time posted
        ordering = ['-date_posted']
        # Every message uniquely linked to a user
        unique_together = ['user','content']


class Comments(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    username = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    comment_html = models.TextField(editable=False)
    comment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment

    def save(self,*args,**kwargs):
        self.comment_html = misaka.html(self.comment)
        super().save(*args,**kwargs)

# Like use still in development
class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
