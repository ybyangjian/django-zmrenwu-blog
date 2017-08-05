from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^category/(?P<slug>[-_\w]+)/$', views.CategoryView.as_view(), name='category_slug'),
    url(r'^notifications/$', views.AllNotificationsListView.as_view(), name='notification_all'),
    url(r'^notifications/unread/$', views.UnreadNotificationsListView.as_view(), name='notification_unread'),
]
