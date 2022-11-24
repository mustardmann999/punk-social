from django.conf.urls import url
from . import views

### Group URLs ###

app_name = 'groups'

urlpatterns = [
    url(r'^$',views.ListGroups.as_view(template_name='group_list.html'),name='list'),
    url(r'^new/$',views.CreateGroup.as_view(template_name='group_form.html'),name='create'),
    url(r'^posts/in/(?P<slug>[-\w]+)/$',views.GroupDetail.as_view(template_name='group_detail.html'),name='detail'),
    url(r'^join/(?P<slug>[-\w]+)/$',views.JoinGroup.as_view(),name='join'),
    url(r'^leave/(?P<slug>[-\w]+)/$',views.LeaveGroup.as_view(),name='leave'),
    url(r'^delete/(?P<slug>[-\w]+)/$',views.DeleteGroup.as_view(template_name='group_confirm_delete.html'),name='delete'),
    url(r'^edit/(?P<slug>[-\w]+)/$',views.GroupUpdateView.as_view(template_name='group_update_form.html'),name='edit_group'),
]
