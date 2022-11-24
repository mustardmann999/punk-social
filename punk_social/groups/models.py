from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.utils import timezone
# link embedding, markdown inside of posts
import misaka

from django.contrib.auth import get_user_model
User = get_user_model()

### Groups models ###

# Group model
class Group(models.Model):
    # unique name and slug that don't overlap
    created_by = models.ForeignKey(User, related_name='groups_created')
    name = models.CharField(max_length=128,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    description = models.TextField(blank=True,default='')
    # For html of group description with misaka
    description_html = models.TextField(editable=False,default='',blank=True)
    # members belonging to group
    members = models.ManyToManyField(User,through='GroupMember')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('groups:detail',kwargs={'slug':self.slug})

    class Meta:
        ordering = ['name']

# Membership model relating user to groups
class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memberships')
    user = models.ForeignKey(User, related_name='user_groups')

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group','user')

# Groups models
