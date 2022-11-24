from django.conf.urls import url
from . import views

### Posts URLs ###

app_name = 'posts'

urlpatterns = [
    url(r'^new/$',views.CreatePost.as_view(template_name='post_form.html'),name='create'),
    url(r'^by/(?P<username>[-\w]+)/(?P<pk>\d+)/$',views.post_detail,name='detail'),
    url(r'^delete/(?P<pk>\d+)/$',views.DeletePost.as_view(template_name='post_confirm_delete.html'),name='delete'),
    url(r'^comment/(?P<pk>\d+)/remove/$',views.comment_remove,name='comment_remove'),
]
