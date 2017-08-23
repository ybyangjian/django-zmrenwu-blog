from django.conf.urls import url

from . import views

app_name = 'notify'
urlpatterns = [
    url(r'^$', views.AllNotificationsListView.as_view(), name='notification_all'),
    url(r'^unread/$', views.UnreadNotificationsListView.as_view(), name='notification_unread'),
]
