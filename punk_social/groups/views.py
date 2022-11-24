from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import get_object_or_404

from groups.models import Group,GroupMember
from . import models
from .forms import GroupUpdateForm

from django.views import generic

### Group Views ###

# Create group uses generic CreateView
class CreateGroup(LoginRequiredMixin,generic.CreateView):
    # fields able to create
    fields = ['name','description']
    model = Group

    # Sets group description as required
    def get_form(self, form_class=None):
        form = super(CreateGroup, self).get_form(form_class)
        form.fields['description'].required = True
        return form

    # Adds author to list of group members
    def form_valid(self,form):
        form.instance.created_by = self.request.user
        result = super().form_valid(form)
        GroupMember.objects.create(user=self.request.user, group=self.object)
        return result

# Group detail uses generic DetailView
class GroupDetail(generic.DetailView):
    model = Group

# Group list uses generic ListView
class ListGroups(generic.ListView):
    model = Group

    # Add the list of joined groups for user to context dict
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_groups = Group.objects.filter(members=self.request.user)
        context['user_groups'] = user_groups
        return context

# Join group view uses generic RedirectView
class JoinGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:detail',kwargs={'slug':self.kwargs.get('slug')})

    # Get group object and add user as member following try/except
    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except:
            messages.warning(self.request,'Warning, already a member!')
        else:
            messages.success(self.request,'You are now a member!')

        return super().get(request,*args,**kwargs)

# Leave group uses generic RedirectView
class LeaveGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:detail',kwargs={'slug':self.kwargs.get('slug')})

    # Get group object and remove user as member following try/except
    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            membership = models.GroupMember.objects.filter(
                user = self.request.user,
                group__slug = self.kwargs.get('slug')
            ).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,'Sorry you are not a member in this group')
        else:
            membership.delete()
            messages.success(self.request,'You have left the group!')

        return super().get(request,*args,**kwargs)

# Delete group uses generic DeleteView following confirmation by form
class DeleteGroup(LoginRequiredMixin,generic.DeleteView):
    model = models.Group

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Group Deleted!')
        return super().delete(*args)

    def get_success_url(self):
        return reverse_lazy('groups:list')

# Group update uses generic UpdateView
class GroupUpdateView(generic.UpdateView):
    model = models.Group
    fields = ['name','description']
