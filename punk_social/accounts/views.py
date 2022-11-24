from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404

from posts.models import Post, Like
from groups.models import Group
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import get_user_model
User = get_user_model()

### Accounts views ###

# p will represent the profile
# u will represent the user

# Profile view fetches user related model content from profile model using profile slug for ID
# View is based on profile slug NOT user
# If profile is for user, this is distinguished at template level
@login_required
def profile_view(request, slug):
	p = Profile.objects.filter(slug=slug).first()
	u = p.user
	user_posts = Post.objects.filter(user_id=u)
	user_groups = Group.objects.filter(members=u)

	context = {
		'u': u,
		'post_count': user_posts.count,
		'posts': user_posts,
		'groups': user_groups,
		}

	# Post likes still in development
	if request.user.is_authenticated:
		liked = [i for i in Post.objects.all() if Like.objects.filter(user = request.user, post=i)]
		context['liked_post'] = liked

	return render(request, "profile.html", context)

# Registration view creates user model instance
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'Your account has been created! You can now login!')
			return redirect('accounts:login')
	else:
		form = UserRegisterForm()
	return render(request, 'register.html', {'form':form})

# Edit profile view shows user model and profile model info simultaneously
# This gives the user and profile models a uniform identity to the user
@login_required
def edit_profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, 'Your account has been updated!')
			return redirect('accounts:profile_view', slug=request.user.profile.slug)
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	context ={
		'u_form': u_form,
		'p_form': p_form,
	}
	return render(request, 'edit_profile.html', context)
