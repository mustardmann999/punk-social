from django.contrib import admin
from django.conf.urls import url
from accounts import views as user_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

### Accounts URLs ###
# Password reset still in development 

app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^signup/$', user_views.register, name='register'),
    url('^profile/(?P<slug>[-\w]+)/$', user_views.profile_view, name='profile_view'),
    url('^edit-profile/$', user_views.edit_profile, name='edit_profile'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^password-reset/$', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    url(r'^password-reset/done/', auth_views.PasswordResetView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    url(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
