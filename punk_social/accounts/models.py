from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings
from autoslug import AutoSlugField

### Accounts models ###

# Profile model created upon base user registration
# Dependent on base user model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='images/punk.jpg', upload_to='profile_pics')
    slug = AutoSlugField(populate_from='user',unique=True)
    bio = models.CharField(max_length=255, blank=True)
    portfolio_site = models.URLField(blank=True)

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return "/accounts/{}".format(self.slug)

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)
