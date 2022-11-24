from django import forms
from .models import Comments

### Post forms ###

class NewCommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ['comment']
