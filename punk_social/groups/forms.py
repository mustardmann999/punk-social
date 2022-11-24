from django import forms
from django.contrib.auth.models import User
from .models import Group

### Group forms ###

class GroupUpdateForm(forms.ModelForm):

	class Meta:
		model = Group
		fields = ['name', 'description']
