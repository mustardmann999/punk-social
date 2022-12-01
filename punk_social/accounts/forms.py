from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

### Accounts forms ###

def validate_email(value):
    if User.objects.filter(email = value).exists():
        raise forms.ValidationError(
            ("An account exists with this email. Please enter a unique email."),
            params = {'value':value}
        )

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(validators = [validate_email])

	class Meta:
		model = User
		fields = ['username','email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['bio', 'image', 'portfolio_site']
