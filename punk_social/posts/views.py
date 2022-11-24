from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views import generic
from django.shortcuts import get_object_or_404, render, redirect

from . import models
from groups.models import Group
from .forms import NewCommentForm

from braces.views import SelectRelatedMixin

from django.contrib.auth import get_user_model
User = get_user_model()

### Posts views ###

# Create post uses generic CreateView
class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    fields = ['content','group']
    model = models.Post

    # Filter so user can only post in group with membership
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.group_choices = Group.objects.filter(members = self.request.user)
        context['form'].fields['group'].queryset = self.group_choices
        return context

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

# Post detail view built with function view to implement likes
# Like post still in development
@login_required
def post_detail(request, username, pk):
    post = get_object_or_404(models.Post, pk=pk)
    user = request.user
    is_liked =  models.Like.objects.filter(user=user, post=post)
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.post = post
            data.username = user
            data.save()
            return redirect('posts:detail', username=username, pk=pk)
    else:
        form = NewCommentForm()
    return render(request, 'post_detail.html', {'post':post, 'is_liked':is_liked, 'form':form})

# Post detail view built with generic DetailView
# NOT in use currently
class PostDetail(SelectRelatedMixin,generic.DetailView):
    model = models.Post
    select_related = ('user','group')

    def get_queryset(self):
        # Get query set for post and filter where username matches
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

# Post delete uses generic DeleteView
class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = models.Post
    select_related = ('user','group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted!')
        return super().delete(*args)

    def get_success_url(self):
        return reverse_lazy('accounts:profile_view', kwargs={'slug':self.request.user.profile.slug})

# Remove comment
@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(models.Comments,pk=pk)
    # Save pk before delete so it can still be referenced
    username = comment.post.user.profile.slug
    post_pk = comment.post.pk
    comment.delete()
    return redirect('posts:detail',pk=post_pk, username=username)

# Like use still in development
@login_required
def like(request):
    post_id = request.GET.get("likeId", "")
    user = request.user
    post = Post.objects.get(pk=post_id)
    liked = False
    like = Like.objects.filter(user=user, post=post)
    if like:
        like.delete()
    else:
        liked = True
        Like.objects.create(user=user, post=post)
    resp = {
        'liked':liked
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type = "application/json")
