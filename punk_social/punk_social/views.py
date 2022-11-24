from django.views.generic import TemplateView
from groups.models import Group
from django.views.generic import ListView

class HomePage(ListView):
    model = Group
    template_name = 'home.html'
