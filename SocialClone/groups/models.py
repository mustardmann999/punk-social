from django.db import models
from django.core.urlresolvers import reverse
# clean inputs for urls
from django.utils.text import slugify
# link embedding, markdown inside of posts
import misaka

from django.contrib.auth import get_user_model
User = get_user_model()
# Call for user session
from django import template
register = template.Library()

### GROUPS models ###

class Group(models.Model):
    # unique name and slug that don't overlap
    name = models.CharField(max_length=128,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    description = models.TextField(blank=True,default='')
    # For html of group description with misaka
    description_html = models.TextField(editable=False,default='',blank=True)
    # members belonging to group
    members = models.ManyToManyField(User,through='GroupMember')

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})

    class Meta:
        ordering = ['name']

class GroupMember(models.Model):
    # Link member to group
    group = models.ForeignKey(Group, related_name='memberships')
    # Link to member (can belong to several groups)
    user = models.ForeignKey(User, related_name='user_groups')

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group','user')

# Groups models
